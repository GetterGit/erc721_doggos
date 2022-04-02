# uploading to Pinata as well as to our own IPFS node, so that when our node goes does, the images don't follow
import os
from pathlib import Path
import requests

# using pinFileToIPFS endpoint: https://docs.pinata.cloud/api-pinning/pin-file
PINATA_BASE_URL = "https://api.pinata.cloud"
endpoint = "/pinning/pinFileToIPFS"
# Change this filepath as it's just an example and should be parametarized depending on a breed of each tokenId
filepath = "./img/pug.png"
filename = filepath.split("/")[-1][0]
# we need to use some headers for the pinata post request
headers = {
    "pinata_api_key": os.getenv("PINATA_API_KEY"),
    "pinata_secret_api_key": os.getenv("PINATA_SECRET_API_KEY"),
}


def main():
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        response = requests.post(
            PINATA_BASE_URL + endpoint,
            files={"file": (filename, image_binary)},
            headers=headers,
        )
        print(response.json())
