"""
create.py
====================================
The create module of stratus_api document provides function to create a document in firestore collection
"""


def create_object(collection_name: str, unique_keys: list, attributes: dict, hash_id: bool = False,
                  batch: object = None, message_formatter=None, user_id: str = None,
                  full_collection_name: bool = False):
    """
    creates a document object in firestore collection_name with also having optional functionality to batch create

    Args:
        collection_name: example_collection
        unique_keys: list of keys that needs to be unique for a collection
        attributes: dictionary attributes object
        hash_id: True if document id needs to be hash of unique_keys
        batch: firestore batch object to create objects in batch mode
        message_formatter:
        user_id:
        full_collection_name: True if collection_name is an absolute name
    Returns:
        attributes
    Raises:
        ValueError:
            object already exists
    Examples:
        >>> attributes = dict(active=True, id='example_id', product_id='example_product_id',
        >>>                   audience_id='example_audience_id')
        >>> print(create_object(collection_name='example_collection',unique_keys=['id','product_id'],
        >>>                     attributes=attributes, full_collection_name=True)
        >>> # creates object in the example_collection collection and returns attributes
        {'active':True,'id':'example_id', 'product_id':'example_product_id',
            'audience_id':'example_audience_id'}
        >>> # to use batch mode, create a firestore client and initiate batch mode
        >>> batch = create_db_client(refresh=False).batch()

    """

    from stratus_api.core.common import generate_random_id, generate_hash_id
    from stratus_api.document.utilities import generate_collection_firestore_name
    from stratus_api.document.base import create_db_client
    from stratus_api.document.get import get_objects
    from datetime import datetime
    from copy import deepcopy
    db = create_db_client()
    now = datetime.utcnow()
    attributes = deepcopy(attributes)
    if 'id' in attributes:
        other_unique_fields = [i for i in unique_keys if i != 'id']
        existing_objects = []
        if other_unique_fields:
            existing_objects += get_objects(
                collection_name=collection_name, active=False, full_collection_name=full_collection_name,
                **{"eq_{0}".format(i): attributes[i] for i in other_unique_fields}
            )
        existing_objects += get_objects(
            collection_name=collection_name, active=False, full_collection_name=full_collection_name,
            eq_id=attributes['id']
        )
        if existing_objects:
            raise ValueError("Conflict: object already exists")
        object_id = attributes['id']
    elif hash_id:
        object_id = generate_hash_id(data={i: attributes[i] for i in unique_keys})
    else:
        existing_objects = get_objects(
            collection_name=collection_name, full_collection_name=full_collection_name, active=True,
            **{"eq_{0}".format(i): attributes[i] for i in unique_keys}
        )
        if existing_objects:
            raise ValueError("Conflict: object already exists")
        object_id = generate_random_id()
    attributes['id'] = object_id
    attributes['created'] = now
    attributes['updated'] = now
    attributes['active'] = True
    collection_name = generate_collection_firestore_name(collection_name=collection_name,
                                                         full_collection_name=full_collection_name)
    doc_ref = db.collection(collection_name).document(attributes['id'])
    if batch is not None:
        batch.set(doc_ref, attributes, merge=True)
    else:
        doc_ref.set(attributes, merge=True)
    if batch is not None:
        return attributes, batch
    else:
        return attributes
