# read offchain and create a metadata file
from brownie import AdvancedCollectible, network
from scripts.helpful_scripts import get_breed
from metadata.sample_metadata import metadata_template
import requests
import json
import os

# importing Path to check metadata files existence
from pathlib import Path

breed_to_image_uri = {
    "PUG": "https://ipfs.io/ipfs/QmSsYRx3LpDAb1GZQm7zZ1AuHZjfbPkD6J7s9r41xu1mf8?filename=pug.png",
    "SHIBA_INU": "https://ipfs.io/ipfs/QmYx6GsYAKnNzZ9A6NvEKV9nf1VaDzJrqDR23Y8YSkebLU?filename=shiba-inu.png",
    "ST_BERNARD": "https://ipfs.io/ipfs/QmUPjADFGEKmfohdTaNcWhp7VGk26h5jXDA7v3VtTnTLcW?filename=st-bernard.png",
}


def create_metadata():
    advanced_collectible = AdvancedCollectible[-1]
    # we can loop through each existing token and figure out metadata for it
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print(f"You have created {number_of_advanced_collectibles} collectibles.")
    for token_id in range(number_of_advanced_collectibles):
        # first, returning a breed based on token_id
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        # checking whether the metadata file for this tokenId for this network already exists
        metadata_file_name = (
            f"./metadata/{network.show_active()}/{token_id}-{breed}.json"
        )
        print(metadata_file_name)
        collectible_metadata = metadata_template
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already exists! Delete it to overwrite.")
        else:
            print(f"Creating a metadata file: {metadata_file_name}")
            collectible_metadata["name"] = breed
            collectible_metadata["description"] = f"An adorable {breed} pup!"
            # uploading the breed's pup's image to ipfs (unless already uploaded) before assigning a value to the "image" key
            image_path = "./img/" + breed.lower().replace("_", "-") + ".png"
            # checking if we have already uploaded to IPFS, and if True - skipping uploading it again
            image_uri = None
            if os.getenv("UPLOAD_IPFS") == "true":
                image_uri = upload_to_ipfs(image_path)
            # setting image_uri to image_uri if image_uri is not None, else: doing a breed mapping
            # if we've already uploaded the image to IPFS, we can take it from the 'breed_to_image' mapping
            image_uri = image_uri if image_uri else breed_to_image_uri[breed]
            collectible_metadata["image"] = image_uri
            # now, we need to dump 'collectible_metadata' into its own file ('metadata_file_name') and also upload to IPFS
            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file)
            # same as with the images: don't re-upload to IPFS if already uploaded
            if os.getenv("UPLOAD_IPFS") == "true":
                upload_to_ipfs(metadata_file_name)


def upload_to_ipfs(filepath):
    # 1. taking the filepath argument 2. openning the file in the filepath in binary (rb) 3. naming the openned file as fp
    with Path(filepath).open("rb") as fp:
        # reading the image in the binary format
        image_binary = fp.read()
        # upload the image binary to IPFS after launching our IPFS node by 'ipfs daemon'
        ipfs_url = "http://127.0.0.1:5001"
        # now , making post request to the endpoint. documentation: https://docs.ipfs.io/reference/http/api/#api-v0-add
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file": image_binary})
        # if succsessful, the response returns Bytes, Hash, Name, Size
        # .json() conversts the data type into a json string
        ipfs_hash = response.json()["Hash"]
        filename = filepath.split("/")[-1:][0]  # e.g. "./img/0-PUG.png" -> "0-PUG.png"
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(image_uri)
        return image_uri


def main():
    create_metadata()
