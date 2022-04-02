from brownie import AdvancedCollectible, network
from scripts.advanced_collectible.create_metadata import create_metadata
from scripts.helpful_scripts import OPENSEA_URL_TESTNET, get_breed, get_account

# setting the dictionary to pull the metadata from
dog_metadata_dict = {
    "PUG": "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json",
    "SHIBA_INU": "https://ipfs.io/ipfs/QmdryoExpgEQQQgJPoruwGJyZmz6SqV4FRTX1i73CT3iXn?filename=1-SHIBA_INU.json",
    "ST_BERNARD": "https://ipfs.io/ipfs/QmbBnUjyHHN7Ytq9xDsYF9sucZdDJLRkWz7vnZfrjMXMxs?filename=2-ST_BERNARD.json",
}


def set_token_uri():
    print(f"Working on {network.show_active()}.")
    advanced_collectible = AdvancedCollectible[-1]
    # looping through all created tokens to set their token_uri
    number_of_collectibles = advanced_collectible.tokenCounter()
    for token_id in range(number_of_collectibles):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        # before setting token_uri, checking if this token_id already has a token_uri set
        if not advanced_collectible.tokenURI(token_id).startswith("https://"):
            print(f"Setting tokenURI of {token_id}...")
            set_tokenURI(token_id, advanced_collectible, dog_metadata_dict[breed])


def set_tokenURI(token_id, nft_contract, tokenURI):
    account = get_account()
    uri_tx = nft_contract.setTokenURI(token_id, tokenURI, {"from": account})
    uri_tx.wait(1)
    print(
        f"You can view your NFT at {OPENSEA_URL_TESTNET.format(nft_contract.address, token_id)}"
    )
    print(
        "If you cannot see your NFT now, please, wait for 10 minutes for Opensea to load it and then refresh the page."
    )


def main():
    set_token_uri()
