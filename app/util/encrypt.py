import hashlib
import io
# from PyPDF2 import PdfWriter, PdfReader
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from app.util.config import config


# def read_pdf_as_bytes(file):
#     reader = PdfReader(file)
#     writer = PdfWriter()
#     # Add all pages to the writer
#     for page in reader.pages:
#         writer.add_page(page)
#     response_bytes_stream = io.BytesIO()
#     writer.write(response_bytes_stream)
#     return response_bytes_stream.read()


def sk(issuer_name):
    h = hashlib.new('sha256')
    h.update(bytes(config.issuer[issuer_name], encoding='utf-8'))
    return Ed25519PrivateKey.from_private_bytes(h.digest())


if __name__ == '__main__':
    print("")
    # Issuer
    # 1. Read Pdf file as bytes
    # pdf_bytes = read_pdf_as_bytes("../../upload/20210825155000.pdf")
    # # 2. generate key pair / get key from private bytes
    # private_key = sk("monash")
    # print(private_key)
    # public_key = private_key.public_key().public_bytes(
    #     crypto_serialization.Encoding.Raw,
    #     crypto_serialization.PublicFormat.Raw
    # )
    # print("PK1[public_bytes]:{}".format(public_key))  # cc63538b71d3b80d7bae54adafd7fa747caa26a2684d11f1988ead6931763b0b
    # print("PK1[hex]:{}".format(public_key.hex()))  # cc63538b71d3b80d7bae54adafd7fa747caa26a2684d11f1988ead6931763b0b
    # public_key2 = private_key.public_key().public_bytes(
    #     crypto_serialization.Encoding.Raw,
    #     crypto_serialization.PublicFormat.Raw
    # )
    # print("PK2[public_bytes]:{}".format(public_key2))  # cc63538b71d3b80d7bae54adafd7fa747caa26a2684d11f1988ead6931763b0b
    # print("PK2[hex]:{}".format(public_key2.hex()))  # cc63538b71d3b80d7bae54adafd7fa747caa26a2684d11f1988ead6931763b0b
    #
    # print("private_key:{}".format(private_key))
    # # signature = '001005f2f7d15d0a275dea36f3c7b5396725fd618a5b02925d51c837c1ea41fe62362cc5faad5d3073c6ab586c50e3d19ec062185f67fc0c272d725a82525002'
    # # 3. using private key sign document
    # signature = private_key.sign(pdf_bytes)
    # print("signature[hex]:{}".format(signature.hex()))
    # # print("signature:{}".format(signature.hex()))
    # # print(b''.fromhex(signature.hex()))
    # # 4. derive public key
    # # 5. Publish DID Proof (public key & signature)
    # pk = Ed25519PublicKey.from_public_bytes(
    #     b''.fromhex("cc63538b71d3b80d7bae54adafd7fa747caa26a2684d11f1988ead6931763b0b"))
    # print("public_key_:{}".format(pk.public_bytes(crypto_serialization.Encoding.Raw,
    #                                              crypto_serialization.PublicFormat.Raw).hex()))
    # # Verifier
    # # 1. get pdf file
    # pub_data = {"signature": b''.fromhex(signature), "pk": pk}
    # print(pub_data)
    # print(signature)
    # pdf_bytes_verify = read_pdf_as_bytes("../../download/20210825155000_download.pdf")
    # # Raises InvalidSignature if verification fails
    # # 2. verify message using public key and signature