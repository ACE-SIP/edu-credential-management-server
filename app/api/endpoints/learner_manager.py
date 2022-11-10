import os
from bson import json_util
from fastapi import APIRouter
from db.mongo_client import Database
import json

router = APIRouter(responses={404: {"description": "Device Not found"}})


@router.get('/all/{source}')
def list_all_learners_from_institution_source(source):
    Database.initialize()
    collection = Database.DATABASE[os.environ.get('DB_COLLECTION_USERS')]
    query_condition = {"role": "learner"}
    keep_fields = {"email": 1, "_id": 1, "username": 1}
    return json.loads(json_util.dumps(collection.find(query_condition, keep_fields)))
