"""
utilities.py
====================================
The utilities module of stratus_api document provides support functions for create, update, get modules
"""


def generate_collection_firestore_name(collection_name: str, prefix: str = '', full_collection_name: bool = False):
    """
    generates firestore collection name with respect to the service and environment
    Args:
        collection_name (str): example_collection
        prefix (str): random value if collection is a test collection
        full_collection_name (bool): True if collection_name is an absolute name
    Returns:
        string of collection name
    Examples:
        >>> print (generate_collection_firestore_name(collection_name='example_collection',full_collection_name=True))
        'example_service-test-example_collection'
    """
    from stratus_api.core.settings import get_app_settings
    app_settings = get_app_settings()
    if full_collection_name:
        return collection_name
    return "{0}-{1}-{2}{3}".format(app_settings['service_name'], app_settings['environment'], prefix, collection_name)


def manage_retries(partial_function, handled_exceptions: list, propagate_exceptions: bool, retries: int,
                   backoff: bool = True):
    """
    retry function to perform retries

    Args:
        partial_function (func): example: doc_ref.get
        handled_exceptions (list): [ServiceUnavailable]
        propagate_exceptions (boolean): boolean
        retries (int): number of retries
        backoff (bool): exponential backoff
    Returns:
         results (function output)
    Examples:
        >>> from stratus_api.document.base import create_db_client
        >>> from google.cloud.exceptions import ServiceUnavailable
        >>> db = create_db_client()
        >>> doc_ref = db.collection(collection_name='example_collection')
        >>> documents = [i for i in manage_retries(partial_function=doc_ref.get, handled_exceptions=[ServiceUnavailable],
        >>>                                  retries=3, propagate_exceptions=True)]
    """
    from logging import getLogger
    logger = getLogger()
    from time import sleep
    success = False
    attempts = 0
    results = None
    delay = 1
    while attempts < retries and not success:
        try:
            results = partial_function()
        except handled_exceptions as e:
            attempts += 1
            if retries == attempts and propagate_exceptions:
                raise e
            else:
                logger.warning(e)
                if backoff:
                    sleep(delay)
                    delay *= 2
        else:
            success = True
    return results


def delete_collection_documents(collection, full_collection_name=False):
    """
    function to delete all the documents under the collection and the collection

    Args:
        collection (str): example_collection
        full_collection_name (bool): True if collection_name is an absolute name
    Returns:
        None
    Examples:
        >>> delete_collection_documents(collection='example_collection', full_collection_name=True)
    """
    from stratus_api.document import create_db_client
    db = create_db_client()
    chunk_size = 10
    collection = generate_collection_firestore_name(collection_name=collection,
                                                    full_collection_name=full_collection_name)
    while chunk_size > 0:
        chunk_size = 0
        chunk = db.collection(collection).limit(100).get()
        for document in chunk:
            document.reference.delete()
            chunk_size += 1
    pass
