from brownie import EtherWallet, accounts
import pytest

# Deploy the contract
@pytest.fixture
def etherWallet():
    ether_wallet = EtherWallet.deploy({"from": accounts[0]})
    return ether_wallet
