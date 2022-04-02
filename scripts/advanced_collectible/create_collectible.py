from venv import create


from brownie import AdvancedCollectible
from scripts.helpful_scripts import get_account, fund_with_link


def create_collectible():
    account = get_account()
    # getting the latest advanced collectible contract depending on the network
    advanced_collectible = AdvancedCollectible[-1]
    fund_with_link(advanced_collectible.address)
    create_tx = advanced_collectible.createCollectible({"from": account})
    create_tx.wait(1)
    print("The collectible has been created!")


def main():
    create_collectible()
