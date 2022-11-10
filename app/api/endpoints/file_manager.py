import base64
import time
from datetime import date
import os
from bson import json_util, ObjectId
import json
import aiofiles
from bson import Binary
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from fastapi import APIRouter, Depends
from fastapi import File, UploadFile

from app.api.models.User import User, get_current_active_user
from app.util.encrypt import sk
from db.mongo_client import Database, download
import asyncio

router = APIRouter(responses={404: {"description": "Device Not found"}})


@router.post("/upload/")
async def upload_file(issuer: str, file: UploadFile = File(...)):
    if not file:
        return {"message": "No upload file sent"}
    out_file_path = "upload/" + file.filename
    start = time.time()
    Database.initialize()
    collection = Database.DATABASE[os.environ.get('DB_COLLECTION_CREDENTIALS')]
    async with aiofiles.open(out_file_path, 'wb') as out_file:
        # file bytes
        private_key = sk(issuer)
        contents = await file.read()
        user_collection = Database.DATABASE[os.environ.get('DB_COLLECTION_USERS')]
        issuer = user_collection.find_one({'email': issuer})
        data = {'filename': file.filename,
                'data': Binary(contents),
                'issuer': issuer['email'],
                'public_key': issuer['public_key'],
                'issuanceDate': date.today().strftime("%d/%m/%Y"),
                'signature': private_key.sign(contents)
                }
        collection.insert_one(data)
        await out_file.write(contents)
    end = time.time()
    print("cost", end-start)
    return {"filename": file.filename}


@router.get("/download/")
async def upload_file(fileId, savePath):
    Database.initialize()
    collection = Database.DATABASE[os.environ.get('DB_COLLECTION_CREDENTIALS')]
    file_data = collection.find_one({"_id": ObjectId(fileId)})
    file_name = file_data['filename']
    savePath = "/Users/wayne/Downloads/edu_download"
    save = savePath + "/download_" + str(round(time.time())) + "_" + file_name
    print(save)
    await download(save, file_data['data'])
    return {"saveStatus": True, "message": "Success"}


@router.get("/all/")
async def query_all_files(learner, current_user: User = Depends(get_current_active_user)):
    print("Current user: {}".format(current_user.email))
    Database.initialize()
    collection = Database.DATABASE[os.environ.get('DB_COLLECTION_CREDENTIALS')]
    return json.loads(json_util.dumps(collection.find({"learner": learner}, {"data": 0})))


@router.post("/sign")
async def file_sign(issuer: str, file: UploadFile = File(...)):
    private_key = sk(issuer)
    contents = await file.read()
    return base64.b64encode(private_key.sign(contents))


@router.post("/verify")
async def file_verify(fileId, file: UploadFile = File(...)):
    print("start-time", time.time())
    start = time.time()
    Database.initialize()
    collection = Database.DATABASE[os.environ.get('DB_COLLECTION_CREDENTIALS')]
    rst = collection.find_one({"_id": ObjectId(fileId)})
    if len(list(rst)) > 0:
        signature = rst['signature']
        pub_key = rst['public_key']
        print(pub_key)
        public_key = Ed25519PublicKey.from_public_bytes(b''.fromhex(pub_key.hex()))
        try:
            contents = await file.read()
            public_key.verify(signature, contents)
            end = time.time()
            print("end time", end)
            print(end - start)
            return {'verifyStatus': True, 'message': "Verify Success!"}
        except:
            return {'verifyStatus': False, 'message': "verify fail"}
    return {'verifyStatus': False, 'message': "Issuer Not Found"}


@router.post("/issuing/")
async def issuing_file(issuer: str, learner, file: UploadFile = File(...)):
    if not file:
        return {"message": "No upload file sent"}
    Database.initialize()
    collection = Database.DATABASE[os.environ.get('DB_COLLECTION_CREDENTIALS')]
    # file bytes
    private_key = sk(issuer)
    contents = await file.read()
    user_collection = Database.DATABASE[os.environ.get('DB_COLLECTION_USERS')]
    issuer = user_collection.find_one({'email': issuer})
    learner = user_collection.find_one({'_id': ObjectId(learner)}, {"email": 1})

    data = {'filename': file.filename,
            'data': Binary(contents),
            'issuer': issuer['email'],
            'learner': learner['email'],
            'public_key': issuer['public_key'],
            'issuanceDate': date.today().strftime("%d/%m/%Y"),
            'signature': private_key.sign(contents)
            }
    collection.insert_one(data)
    return {"filename": file.filename}
