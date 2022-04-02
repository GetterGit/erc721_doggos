from brownie import SimpleCollectible
from scripts.helpful_scripts import get_account, OPENSEA_URL_TESTNET


sample_token_uri = "https://ipfs.io/ipfs/QmSmgbNJLVfUwZk6Bb431ndxggWd4VuGmF2EPUQpKaNJcu"

# deploying the contract and creating a collectible
def deploy_and_create():
    account = get_account()
    simple_collectible = SimpleCollectible.deploy({"from": account})
    create_tx = simple_collectible.createCollectible(
        sample_token_uri, {"from": account}
    )
    create_tx.wait(1)
    print(
        f"The NFT has been minted, you can view it at {OPENSEA_URL_TESTNET.format(simple_collectible.address, simple_collectible.tokenCounter() - 1)} if the deployment was on a live testnet."
    )
    return simple_collectible


def main():
    deploy_and_create()
