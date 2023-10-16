"""
update.py
====================================
The update module of stratus_api document provides function to update/delete a document in firestore collection
"""


def format_update_message(attributes: dict):
    """
    formats attributes according to the firestore body format
    Args:
        attributes (dict): dicionary of attributes
    Returns:
        dict: firestore compatible request_body format
    Examples:
        >>> attributes = {'active':True,'id':'example_id1', 'segments':{'segment_id':'example_segment_id'}}
        >>> print(format_update_message(attributes=attributes))
        {'active':True,'id':'example_id1', 'segments.segment_id':'example_segment_id'}}
    """
    update = dict()
    for k, v in attributes.items():
        if isinstance(v, dict):
            for key, value in format_update_message(v).items():
                update['{0}.{1}'.format(k, key)] = value
        else:
            update[k] = v
    return update


def update_object(collection_name: str, object_id: str, attributes: dict, batch: object = None, message_formatter=None,
                  user_id: str = None, upsert: bool = False, override: bool = False, overwrite_updated: bool = False,
                  full_collection_name: bool = False):
    """
    updates the document in the collection

    Args:
        collection_name (str): example_collection
        object_id (str): document id
        attributes (dict): dictionary of attributes
        batch (object): firestore batch object to update objects in batch
        message_formatter ():
        user_id (str):
        upsert (bool): True for update/create a object
        override (bool): True if the document needs to be over written
        overwrite_updated (bool): True if updated flag does not need to be updated
        full_collection_name (bool): True if collection_name is an absolute name
    Returns:
         dict: attributes
    Examples:
        >>> from stratus_api.document import create_object
        >>> attributes = {'active':True,'id':'example_id', 'segments':{'segment_id':'example_segment_id'}}
        >>> obj = create_object(collection_name=collection_name, unique_keys=['name'], attributes=attributes,
        >>>                     full_collection_name=True)
        >>> update_attributes = dict(sub_object=dict(attributes_3='New attributes'))
        >>> updated_obj = update_object(collection_name=collection_name, full_collection_name=True,
        >>>                             object_id=obj['id'], attributes=update_attributes)
        >>> print(updated_obj)
        {'active':True,'id':'example_id', 'segments':{'segment_id':'example_segment_id'},
        'sub_object': {'attributes_3':'New attributes'}}

    """
    from stratus_api.document.base import create_db_client
    from stratus_api.document.utilities import generate_collection_firestore_name
    from datetime import datetime
    from copy import deepcopy
    collection_name = generate_collection_firestore_name(collection_name=collection_name,
                                                         full_collection_name=full_collection_name)
    db = create_db_client()
    doc_ref = db.collection(collection_name).document(object_id)
    now = datetime.utcnow()
    attributes = deepcopy(attributes)
    if not overwrite_updated:
        attributes['updated'] = now

    if not override:
        attributes = format_update_message(attributes=attributes)

    if batch is not None:
        if upsert:
            batch.set(doc_ref, attributes, merge=True)
        else:
            batch.update(doc_ref, attributes)
    else:
        if upsert:
            doc_ref.set(attributes, merge=True)
        else:
            doc_ref.update(attributes)
    if not batch:
        attributes = doc_ref.get().to_dict()
    else:
        return attributes, batch
    return attributes


def delete_object(collection_name: str, object_id: str, batch: object = None, user_id=None,
                  full_collection_name: bool = False):
    """
    deactivates the document under the collection
    :param collection_name: example_collection
    :param object_id: document id
    :param batch: firestore batch object to delete objects in batch
    :param user_id:
    :param full_collection_name: True if collection_name is an absolute name
    :return: results
    """
    attributes = dict(id=object_id, active=False)
    results = update_object(collection_name=collection_name, object_id=object_id, attributes=attributes, batch=batch,
                            full_collection_name=full_collection_name)
    return results
