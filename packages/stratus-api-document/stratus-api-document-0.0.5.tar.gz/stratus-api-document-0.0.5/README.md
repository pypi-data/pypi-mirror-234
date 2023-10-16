The Stratus API document is a python package that is built on top of Google Cloud Firestore API. Functionality includes  create, update, get, and delete objects in the firestore collections.

### Installation
Install this library using pip.

### Supported Python Versions
Python >= 3.5

### Example Usage
```
from stratus_api.document.base import create_db_client

client = create_db_client()
doc_ref = client.collection('example_collection').document('document_id')
document = doc_ref.get()
```
### Example Usage
```
from stratus_api.document.get import get_objects

objects = get_objects(collection_name='example_collection', active=True, limit=10, full_collection_name=True)

for object in objects:
    print(object)
```