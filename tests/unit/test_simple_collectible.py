from brownie import network
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
from scripts.simple_collectible.deploy_and_create import deploy_and_create
import pytest

def test_can_create_simple_collectible():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    simple_collectible = deploy_and_create()
    # asserting deploy_and_create() executed right
    assert simple_collectible.ownerOf(0) == get_account()
    