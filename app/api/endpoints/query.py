import os
from bson import json_util
from fastapi import APIRouter, Depends
from app.api.models.User import User, get_current_active_user
from db.mongo_client import Database
import json

router = APIRouter(responses={404: {"description": "Device Not found"}})


@router.get('/uni/{source}')
def list_all_credentials_from_data_source(source, current_user: User = Depends(get_current_active_user)):
    print("Current user: {}".format(current_user))
    Database.initialize()
    collection = 'DB_COLLECTION_EDUCATION_' + source.upper()
    collection = Database.DATABASE[os.environ.get(collection)]
    return json.loads(json_util.dumps(collection.find()))

