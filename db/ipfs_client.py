# upload
import json
import aiofiles
import requests


def upload(files):
    response = requests.post('https://ipfs.infura.io:5001/api/v0/add', files=files)
    p = response.json()
    return p['Hash']


def get_file(params):
    response_two = requests.post('https://ipfs.infura.io:5001/api/v0/block/get', params=params)
    print(response_two)
    return response_two


if __name__ == "__main__":
    print("")
    # api = ipfsapi.connect('127.0.0.1', 5001)
    # print(api)
    # files = {
    #     'fileOne': open('../upload/Education credential system.pdf', 'rb'),
    # }
    # output = upload(files)
    # params = (
    #     ('arg', output),
    # )
    # down_load = get_file(params)
    # objInstance = ObjectId("6282054554f7fe55f048909c")
    # data = collection.find_one({"_id": objInstance})
    # with aiofiles.open("a.pdf", 'wb') as out_file:
    #     out_file.write(down_load.text)
    # dec = json.JSONDecoder()
    # print(dec.decode(down_load.text))
