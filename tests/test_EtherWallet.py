from brownie import EtherWallet, accounts, reverts
import pytest

# Fixture to deploy the contract
@pytest.fixture
def etherWallet():
    ether_wallet = EtherWallet.deploy({"from": accounts[0]})
    return ether_wallet


def test_constructor(etherWallet):
    assert etherWallet.owner() == accounts[0]


def test_getBalance(etherWallet):
    assert etherWallet.getBalance() == 0


def test_sendEtherToContract(etherWallet):
    accountInitBalance = accounts[0].balance()
    sendAmount = "1 ether"
    tx = accounts[0].transfer(etherWallet.address, sendAmount)

    assert accounts[0].balance() == accountInitBalance - sendAmount
    assert etherWallet.balance() and etherWallet.getBalance() == sendAmount
    assert "EtherReceived" in tx.events


# --- WITHDRAW FUNCTION ---


def test_withdraw(etherWallet):
    accountInitBalance = accounts[0].balance()
    sendAmount = "1 ether"
    accounts[0].transfer(etherWallet.address, sendAmount)
    etherWallet.withdraw(sendAmount, {"from": etherWallet.owner()})

    assert accounts[0].balance() == accountInitBalance
    assert etherWallet.balance() == 0


def test_withdraw_notOwner(etherWallet):
    accountInitBalance = accounts[0].balance()
    sendAmount = "1 ether"
    accounts[0].transfer(etherWallet.address, sendAmount)
    with reverts():
        etherWallet.withdraw(sendAmount, {"from": accounts[1]})

    assert accounts[0].balance() == accountInitBalance - sendAmount
    assert etherWallet.balance() == sendAmount


def test_withdraw_moreThanInContract(etherWallet):
    accountInitBalance = accounts[0].balance()
    sendAmount = "1 ether"
    accounts[0].transfer(etherWallet.address, sendAmount)
    with reverts():
        etherWallet.withdraw("2 ether", {"from": etherWallet.owner()})

    assert accounts[0].balance() == accountInitBalance - sendAmount
    assert etherWallet.balance() == sendAmount


def test_withdraw_emptyContract(etherWallet):
    accountInitBalance = accounts[0].balance()
    sendAmount = "1 ether"
    with reverts():
        etherWallet.withdraw(sendAmount, {"from": etherWallet.owner()})

    assert accounts[0].balance() == accountInitBalance
    assert etherWallet.balance() == 0


def test_withdraw_eventEmitted(etherWallet):
    accountInitBalance = accounts[0].balance()
    sendAmount = "1 ether"
    accounts[0].transfer(etherWallet.address, sendAmount)
    tx = etherWallet.withdraw(sendAmount, {"from": etherWallet.owner()})

    assert "EtherWithdrawn" in tx.events
