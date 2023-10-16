import os
from storedict import create_store
from .request import Request

__version__ = "0.0.11"

store = create_store(os.getenv("__BOTFLEET__DATASTORE_PROXY_URL"))
request = Request()
