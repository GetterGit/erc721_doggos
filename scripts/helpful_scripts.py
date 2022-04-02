from brownie import (
    Contract,
    VRFCoordinatorMock,
    LinkToken,
    accounts,
    network,
    config,
    interface,
)
from web3 import Web3

FORKED_MAINNET_ENVIRONMENTS = ["mainnet-fork"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
# adding the token address and it after the static URL part
OPENSEA_URL_TESTNET = "https://testnets.opensea.io/assets/{}/{}"
# mapping for breeds and their respective integers to associte integer with its breed in create_metadata.py
BREED_MAPPING = {0: "PUG", 1: "SHIBA_INU", 2: "ST_BERNARD"}


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    elif id:
        return accounts.load(id)
    elif (
        network.show_active() in FORKED_MAINNET_ENVIRONMENTS
        or network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


contract_to_mock = {"vrf_coordinator": VRFCoordinatorMock, "link_token": LinkToken}


def get_contract(contract_name):
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
    return contract


def deploy_mocks():
    print(f"The active network is {network.show_active()}.")
    print("Deploying mocks ...")
    account = get_account()
    link_token = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(link_token, {"from": account})
    print("All mocks have been deployed!")


def fund_with_link(
    contract_address, account=None, link_token=None, amount=Web3.toWei(0.1, "ether")
):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    link_token_contract = interface.LinkTokenInterface(link_token.address)
    fund_tx = link_token_contract.transfer(contract_address, amount, {"from": account})
    fund_tx.wait(1)
    print("The contract has been funded with 0.1 LINK.")
    return fund_tx


def get_breed(breed_number):
    return BREED_MAPPING[breed_number]
