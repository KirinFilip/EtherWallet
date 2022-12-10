from brownie import EtherWallet, accounts
import pytest


@pytest.fixture
def etherWallet():
    ether_wallet = EtherWallet.deploy({"from": accounts[0]})
    return ether_wallet


def test_construction(etherWallet):
    assert etherWallet.owner() == accounts[0]


def test_sendEtherToContract(etherWallet):
    accountInitBalance = accounts[0].balance()
    sendAmount = "1 ether"
    accounts[0].transfer(etherWallet.address, sendAmount)
    assert accounts[0].balance() == accountInitBalance - sendAmount
    assert etherWallet.balance() == sendAmount
    assert etherWallet.getBalance() == sendAmount


def test_withdraw(etherWallet):
    accountInitBalance = accounts[0].balance()
    sendAmount = "1 ether"
    accounts[0].transfer(etherWallet.address, sendAmount)
    etherWallet.withdraw({"from": etherWallet.owner(), "value": sendAmount})
    assert etherWallet.balance() == 0
