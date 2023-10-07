from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import os 

def snowflake_generate_rsa_keys(args:dict):
    
    private_key_password = args["PRIVATE_KEY_PASSWORD"]
    
    if private_key_password is None:
        print('Environment variable PRIVATE_KEY_PASSWORD not set.  Must set this variable before executing.')
    else:
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )

        print(private_key_password)
        print('&&&&&&&&&&&&&&&&&')
        private_key_pass = bytes(private_key_password, encoding='UTF-8')

        encrypted_pem_private_key = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.BestAvailableEncryption(private_key_pass)
        )

        pem_public_key = private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        print('###### PRIVATE KEY ######')
        print(encrypted_pem_private_key.decode())
        print('###### PUBLIC KEY ######')
        print(pem_public_key.decode())