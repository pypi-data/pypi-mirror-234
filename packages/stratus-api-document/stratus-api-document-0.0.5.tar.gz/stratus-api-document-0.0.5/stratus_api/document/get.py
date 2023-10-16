"""
get.py
====================================
The get module of of stratus_api document provides convenience functions to get objects from the firestore collections
"""


def get_objects(collection_name: str, active: bool = True, limit: int = 10, cursor_id: str = None,
                create_cursor: bool = False, sort_keys: list = None, page: int = None,
                full_collection_name: bool = False,
                **kwargs):
    """
    Convenience function to get list of objects under collection_name

    Args:
        collection_name (str): example_collection
        active (bool): True to get all the document that has active flag set to True
        limit (int): number of objects in a single call
        cursor_id (str): paginate queries by using cursors
        create_cursor (bool): True if needed to create a pagination for the query
        sort_keys (list): sort objects according to keys
        page (int): page_number
        full_collection_name (str): True if collection_name is an absolute name
        kwargs: eq_id for get object that equals to id
    Returns:
        list: list of dictionary of objects
    Examples:
        >>> objects = get_objects(collection_name='example_collection',active=True,
        >>>                       limit=2, full_collection_name=True)
        >>> print(objects)
        [{'active':True,'id':'example_id1', 'product_id':'example_product_id1',
            'audience_id':'example_audience_id1'},
        {'active':True,'id':'example_id2', 'product_id':'example_product_id2',
            'audience_id':'example_audience_id2'}]
        >>> print(len(objects))
        2
    """
    from stratus_api.document.base import create_db_client
    from stratus_api.core.settings import get_app_settings
    from stratus_api.document.utilities import generate_collection_firestore_name, manage_retries
    from google.cloud.exceptions import ServiceUnavailable
    app_settings = get_app_settings()
    db = create_db_client()
    doc_ref = db.collection(
        generate_collection_firestore_name(collection_name=collection_name, full_collection_name=full_collection_name))
    test_ref = None

    if app_settings['environment'] == 'test':
        test_ref = db.collection(
            generate_collection_firestore_name(collection_name=collection_name,
                                               full_collection_name=full_collection_name))
    doc_ref, test_ref, filters = apply_filters(doc_ref=doc_ref, test_ref=test_ref, filters=kwargs,
                                               active=active)
    doc_ref, test_ref, sort_keys = handle_sort(doc_ref=doc_ref, test_ref=test_ref, filters=filters,
                                               sort_keys=sort_keys,
                                               collection_name=collection_name)
    if isinstance(limit, int):
        doc_ref = doc_ref.limit(limit)

    if isinstance(cursor_id, str):
        cursor = get_cursor(cursor_id=cursor_id, active=active,
                            sort_keys=sort_keys, filters=filters)
        if cursor.get('object') is None:
            return [], None
        else:
            page = cursor['page']

    if isinstance(page, int):
        doc_ref = doc_ref.offset(limit * page)
    documents = [i for i in manage_retries(partial_function=doc_ref.get, handled_exceptions=[ServiceUnavailable],
                                           retries=3, propagate_exceptions=True)]
    if test_ref is not None:
        test_documents = [i for i in test_ref.get()]

    if isinstance(cursor_id, str) or create_cursor:
        if page is None:
            page = 0
        if documents:
            last_object = documents[-1]
        else:
            last_object = None
        cursor_id = update_cursor(collection_name=collection_name, active=active, last_object=last_object,
                                  page=page + 1, cursor_id=cursor_id, filters=filters, sort_keys=sort_keys)
        if limit is None or not documents or len(documents) < limit:
            cursor_id = None
        return [i.to_dict() for i in documents], cursor_id
    else:
        return [i.to_dict() for i in documents]


def update_cursor(collection_name: str, active: bool, sort_keys: list, filters: dict, last_object: dict = None,
                  cursor_id: str = None, page: int = 0):
    """
    function to create/update cursor

    Args:
        collection_name (str): example_collection
        active (bool): True to get all the document that has active flag set to True
        sort_keys (list): sort objects according to keys
        filters (dict): {'eq_active':True, 'eq_id':'example_id', 'gte_created':'05-27-2020'}
        last_object (dict): last fetched document object
        cursor_id (str): paginate queries by using cursor_id
        page (int): page number
    Returns:
        str: cursor_id
    Examples:
        >>> last_object = {'active':True,'id':'example_id1', 'product_id':'example_product_id1',
        >>>                'audience_id':'example_audience_id1'}
        >>> filters = {'eq_active':True, 'eq_id':'example_id'}
        >>> cursor_id = update_cursor(collection_name='example_collection', active=True,
        >>>                           last_object=None, cursor_id=None, filters=filters,
        >>>                           sort_keys=sort_keys)
        >>> print(cursor_id)
        '7d619685-e7a0-44ac-b635-random_id'
    """
    from stratus_api.document.base import create_db_client
    from stratus_api.core.common import generate_random_id
    from stratus_api.document.utilities import generate_collection_firestore_name
    cursor_collection_name = generate_collection_firestore_name(collection_name='cursors')
    if last_object is not None:
        attributes = dict(object=last_object.to_dict(), page=page)
    else:
        attributes = dict(object=last_object, page=page)
    if cursor_id is None:
        cursor_id = generate_random_id()
        attributes['collection_name'] = collection_name
        attributes['query_attributes'] = filters
        attributes['active'] = active
        attributes['sort_keys'] = sort_keys
    db = create_db_client()
    db.collection(cursor_collection_name).document(cursor_id).set(attributes, merge=True)
    return cursor_id


def get_cursor(cursor_id: str, active: bool, sort_keys: list, filters: dict):
    """
    returns cursor document from the cursors collection

    Args:
        cursor_id (str): document id under cursors collection
        active (bool): True to get all the document that has active flag set to True
        sort_keys (list): sort objects according to keys
        filters (dict): {'eq_active':True, 'eq_id':'example_id', 'gte_created':'05-27-2020'}
    Returns:
        dict: cursor firestore document
    Examples:
        >>> cursor_id = '7d619685-e7a0-44ac-b635-random_id'
        >>> filters = {'eq_active':True, 'eq_id':'example_id'}
        >>> cursor = get_cursor(cursor_id=cursor_id, active=True,
        >>>                     sort_keys=sort_keys, filters=filters)
        >>> print(cursor)
        {'active':True,'collection_name':'example_collection'}
    """
    from stratus_api.document.base import create_db_client
    from stratus_api.document.utilities import generate_collection_firestore_name
    cursor_collection_name = generate_collection_firestore_name(collection_name='cursors')
    db = create_db_client()
    cursor = db.collection(cursor_collection_name).document(cursor_id).get().to_dict()
    if not cursor:
        raise ValueError("Cursor does not exist")
    if cursor['query_attributes'] != filters or cursor['active'] != active or cursor['sort_keys'] != sort_keys:
        raise ValueError("Cursor does not match provided query")
    return cursor


def apply_filters(doc_ref, test_ref, filters: dict, active: bool):
    """
    function that applies firestore filters such as ==, <, >=, <=, in, array_contains, array_contains_any for the query

    Args:
        doc_ref (object): doc_ref object
        test_ref (object): test_ref object
        filters (dict): {'eq_active':True, 'eq_id':'example_id', 'gte_created':'05-27-2020'}
        active (bool): True to get all the document that has active flag set to True
    Returns:
        doc_ref(object), test_ref(object), filters(dict)
    Examples:
        >>> from stratus_api.document.base import create_db_client
        >>> from stratus_api.document.utilities import generate_collection_firestore_name
        >>> db = create_db_client()
        >>> doc_ref = db.collection(generate_collection_firestore_name(collection_name='example_collection',
        >>>                         full_collection_name=True))
        >>> test_ref = None
        >>> filters = {'eq_active':True, 'eq_id':'example_id'}
        >>> doc_ref, test_ref, filters = apply_filters(doc_ref=doc_ref, test_ref=test_ref,
        >>>                                            filters=filters, active=True)

    """
    operation_map = dict(
        contains='array_contains',
        contains_any='array_contains_any',
        eq_in='in',
        eq='==',
        lt='<',
        lte='<=',
        gt='>',
        gte='>=',
    )
    if active:
        filters['eq_active'] = True
    for k, v in {k: v for k, v in filters.items()}.items():
        key = '_'.join(k.split('_')[1:]) if 'eq_in' not in k else '_'.join(k.split('_')[2:])
        operation = operation_map[k.split('_')[0]] if 'eq_in' not in k else operation_map['_'.join(k.split('_')[:2])]

        if test_ref is not None:
            test_key = '_'.join(k.split('_')[1:]) if 'eq_in' not in k else '_'.join(k.split('_')[2:])
            test_ref = test_ref.where(test_key, operation, v)
            if not (k.startswith('gt') or k.startswith('lt')):
                doc_ref = doc_ref.where(key, operation, v)
        else:
            doc_ref = doc_ref.where(key, operation, v)

    return doc_ref, test_ref, filters


def handle_sort(doc_ref, test_ref, filters: dict, collection_name: str, sort_keys: list):
    """
    Performs order_by clause on the query

    Args:
        doc_ref (object): doc_ref object
        test_ref (object): test_ref object
        filters (dict): {'eq_active':True, 'eq_id':'example_id', 'gte_created':'05-27-2020'}
        collection_name (str): example_collection
        sort_keys (list): sort objects according to keys
    Returns:
        doc_ref(object), test_ref(object), filters(dict)
    Examples:
        >>> from stratus_api.document.base import create_db_client
        >>> from stratus_api.document.utilities import generate_collection_firestore_name
        >>> db = create_db_client()
        >>> doc_ref = db.collection(generate_collection_firestore_name(collection_name='example_collection',
        >>>                         full_collection_name=True))
        >>> test_ref = None
        >>> filters = {'eq_active':True, 'eq_id':'example_id'}
        >>> doc_ref, test_ref, sort_keys = handle_sort(doc_ref=doc_ref, test_ref=test_ref, filters=filters,
        >>>                                               collection_name='example_collection')
    """
    if sort_keys is None:
        sort_keys = []
    for i in sort_keys:
        key = '_'.join(i.split('_')[:-1])
        order = i.split('_')[-1].upper()
        if test_ref is None:
            doc_ref = doc_ref.order_by(field_path=key, direction=order)
        elif len(sort_keys) == 1 and len(filters) == 0:
            doc_ref = doc_ref.order_by(field_path=key, direction=order)
            test_ref = test_ref.order_by(field_path=key, direction=order)
        else:
            test_ref = test_ref.order_by(field_path=key, direction=order)
    return doc_ref, test_ref, sort_keys


def get_all_objects(collection_name: str, active: bool = True, limit: int = 1000, full_collection_name: bool = False,
                    **kwargs):
    """
    Convenience function to get list of all objects under collection_name

    Args:
        collection_name: example_collection
        active: True to get all the document that has active flag set to True
        limit: number of objects in a single call
        full_collection_name: True if collection_name is an absolute name
        kwargs: eq_id for get object that equals to id
    Returns:
        list: list of dictionary of objects
    Examples:
        >>> objects = get_all_objects(collection_name='example_collection',active=True,
        >>>                           limit=2, full_collection_name=True)
        >>> print(objects)
        [{'active':True,'id':'example_id1', 'product_id':'example_product_id1',
            'audience_id':'example_audience_id1'},
        {'active':True,'id':'example_id2', 'product_id':'example_product_id2',
            'audience_id':'example_audience_id2'}]
        >>> print(len(objects))
        2
    """
    all_objects = list()

    objects, cursor_id = get_objects(collection_name=collection_name, active=active, limit=limit, create_cursor=True,
                                     full_collection_name=full_collection_name, **kwargs)
    if objects:
        all_objects.extend(objects)
    while len(objects) == limit:
        objects, cursor_id = get_objects(collection_name=collection_name, active=active, limit=limit,
                                         full_collection_name=full_collection_name, create_cursor=True,
                                         cursor_id=cursor_id, **kwargs)
        if objects:
            all_objects.extend(objects)
    return all_objects
