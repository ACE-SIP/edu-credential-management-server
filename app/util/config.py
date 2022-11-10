from pydantic import BaseSettings


class Config(BaseSettings):
    service_name: str = 'education_credential_system'
    monash_secret_key: str = 'algorand_education_credential_system_monash_university'
    meluni_secret_key: str = 'algorand_education_credential_system_melbourne_university'
    issuer = {'monash@gmail.com': monash_secret_key,
              'meluni@gmail.com': meluni_secret_key,
              'issuer@gmail.com': service_name}


config = Config()
