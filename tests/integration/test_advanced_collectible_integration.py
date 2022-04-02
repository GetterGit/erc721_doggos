# the integration script will resemble the unit test for the creation of advanced collectible
# the only difference is a live chainlink node will be calling back with randomness so we don't need to simulate the process

from brownie import network
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.advanced_collectible.deploy_and_create import deploy_and_create
import pytest
import time


def test_can_create_advanced_collectible_integration():
    # Arrange
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for live testnet.")
    # Act
    # no need to return the creaton transaction as the second variable because we don't need to emulate the Chainlink node
    advanced_collectible, creation_transaction = deploy_and_create()
    print("Staring 3-min buffer time for successful callback...")
    time.sleep(180)
    # Assert
    assert advanced_collectible.tokenCounter() == 1
