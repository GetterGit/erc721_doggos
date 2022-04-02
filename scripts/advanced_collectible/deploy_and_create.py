from brownie import AdvancedCollectible, config, network
from scripts.helpful_scripts import (
    get_account,
    get_contract,
    fund_with_link,
    OPENSEA_URL_TESTNET,
)

# deploying the contract and creating a collectible
def deploy_and_create():
    account = get_account()
    advanced_collectible = AdvancedCollectible.deploy(
        get_contract("vrf_coordinator"),
        get_contract("link_token"),
        config["networks"][network.show_active()]["key_hash"],
        config["networks"][network.show_active()]["fee"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    # now, we want to fund the contract with LINK to be able to get randomness for mintint a random pup
    fund_with_link(advanced_collectible.address)
    create_tx = advanced_collectible.createCollectible({"from": account})
    create_tx.wait(1)
    print("New token has been created!")
    # Returning create_tx to rest the callback with randomness. This way, we are getting requestId
    return advanced_collectible, create_tx


def main():
    deploy_and_create()
