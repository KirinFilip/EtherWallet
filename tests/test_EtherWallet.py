from brownie import EtherWallet, accounts, reverts, ZERO_ADDRESS
import pytest

# Fixture to deploy the contract
@pytest.fixture
def etherWallet():
    ether_wallet = EtherWallet.deploy({"from": accounts[0]})
    return ether_wallet


def test_constructor(etherWallet):
    assert etherWallet.owner() == accounts[0]


# --- Receive Function ---


def test_sendEtherToContract(etherWallet):
    accountInitBalance = accounts[0].balance()
    sendAmount = "1 ether"
    tx = accounts[0].transfer(etherWallet.address, sendAmount)

    assert accounts[0].balance() == accountInitBalance - sendAmount
    assert etherWallet.balance() and etherWallet.getBalance() == sendAmount
    assert "EtherReceived" in tx.events


# --- Withdraw Function ---


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


# --- Getter functions ---


def test_getBalance(etherWallet):
    assert etherWallet.getBalance() == 0


def test_owner(etherWallet):
    assert etherWallet.owner() == accounts[0]


# --- Ownership functions ---


def test_transferOwnership(etherWallet):
    etherWallet.transferOwnership(accounts[1], {"from": accounts[0]})

    assert etherWallet.owner() == accounts[1]


def test_transferOwnership_twoTimes(etherWallet):
    etherWallet.transferOwnership(accounts[1], {"from": accounts[0]})
    etherWallet.transferOwnership(accounts[2], {"from": accounts[1]})

    assert etherWallet.owner() == accounts[2]


def test_transferOwnership_callerNotOwner(etherWallet):
    with reverts():
        etherWallet.transferOwnership(accounts[1], {"from": accounts[1]})


def test_transferOwnership_toZeroAddress(etherWallet):
    with reverts():
        etherWallet.transferOwnership(ZERO_ADDRESS, {"from": accounts[0]})
