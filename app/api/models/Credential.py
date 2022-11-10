from pydantic import BaseModel


class Credential(BaseModel):
    issuer: str
    pk: str
    signature: str
