from brownie import AdvancedCollectible, accounts, network
from scripts.helpful_scripts import (
    get_account,
    get_contract,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)
from scripts.advanced_collectible.deploy_and_create import deploy_and_create
from scripts.advanced_collectible.create_collectible import create_collectible
import pytest


def test_can_create_advanced_collectible():
    # deploy the contract
    # create an NFT
    # get the breed of this NFT back
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing.")
    # Act
    advanced_collectible, creation_transaction = deploy_and_create()
    # also checking we the randomness is returned correctly
    requestId = creation_transaction.events["requestedCollectible"]["requestId"]
    random_number = 777
    get_contract("vrf_coordinator").callBackWithRandomness(
        requestId, random_number, advanced_collectible.address, {"from": get_account()}
    )
    # Assert
    assert advanced_collectible.tokenCounter() == 1
    assert advanced_collectible.tokenIdToBreed(0) == random_number % 3
