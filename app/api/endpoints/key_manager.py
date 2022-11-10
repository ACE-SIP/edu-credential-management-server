import os
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from fastapi import APIRouter
from fastapi import File, UploadFile
from cryptography.hazmat.primitives import serialization as crypto_serialization
from app.util.encrypt import sk
from db.mongo_client import Database

router = APIRouter(responses={404: {"description": "Device Not found"}})


@router.get("/all/")
async def key_generator(issuer: str):
    private_key = sk(issuer)
    public_key = private_key.public_key().public_bytes(
        crypto_serialization.Encoding.Raw,
        crypto_serialization.PublicFormat.Raw
    )
    Database.initialize()
    add_public_key = {"$set": {"public_key": public_key}}
    collection = Database.DATABASE[os.environ.get('DB_COLLECTION_USERS')]
    rst = collection.update_one({"email": issuer}, add_public_key)
    return rst.modified_count


@router.post("/verify")
async def file_verify(issuer: str, file: UploadFile = File(...)):
    Database.initialize()
    collection = Database.DATABASE[os.environ.get('DB_COLLECTION_CREDENTIALS')]
    rst = collection.find({"issuer": issuer})
    signature = rst[0]['signature']
    pk = rst[0]['public_key']
    public_key = Ed25519PublicKey.from_public_bytes(b''.fromhex(pk.hex()))
    try:
        contents = await file.read()
        result = public_key.verify(signature, contents)
        return {'verifyStatus': True, 'message': result}
    except:
        return {'verifyStatus': False, 'message': "verify fail"}


if __name__ == '__main__':
    print("example")
