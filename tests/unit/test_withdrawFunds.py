from brownie import accounts, reverts


# --- withdraw function ---


def test_withdrawHalf(etherWallet):
    accountInitBalance = accounts[0].balance()
    sendAmount = "1 ether"
    withdrawAmount = "0.5 ether"
    accounts[0].transfer(etherWallet.address, sendAmount)
    etherWallet.withdraw(withdrawAmount, {"from": etherWallet.owner()})

    assert accounts[0].balance() == accountInitBalance - withdrawAmount
    assert etherWallet.balance() == withdrawAmount


def test_notOwner(etherWallet):
    accountInitBalance = accounts[0].balance()
    sendAmount = "1 ether"
    accounts[0].transfer(etherWallet.address, sendAmount)
    with reverts():
        etherWallet.withdraw(sendAmount, {"from": accounts[1]})

    assert accounts[0].balance() == accountInitBalance - sendAmount
    assert etherWallet.balance() == sendAmount


def test_moreThanInContract(etherWallet):
    accountInitBalance = accounts[0].balance()
    sendAmount = "1 ether"
    accounts[0].transfer(etherWallet.address, sendAmount)
    with reverts():
        etherWallet.withdraw("2 ether", {"from": etherWallet.owner()})

    assert accounts[0].balance() == accountInitBalance - sendAmount
    assert etherWallet.balance() == sendAmount


def test_emptyContract(etherWallet):
    accountInitBalance = accounts[0].balance()
    sendAmount = "1 ether"
    with reverts():
        etherWallet.withdraw(sendAmount, {"from": etherWallet.owner()})

    assert accounts[0].balance() == accountInitBalance
    assert etherWallet.balance() == 0


def test_eventEmitted(etherWallet):
    sendAmount = "1 ether"
    accounts[0].transfer(etherWallet.address, sendAmount)
    tx = etherWallet.withdraw(sendAmount, {"from": etherWallet.owner()})

    assert "EtherWithdrawn" in tx.events


# --- withdrawAll function ---


def test_withdrawAll(etherWallet):
    accountInitBalance = accounts[0].balance()
    sendAmount = "1 ether"
    accounts[0].transfer(etherWallet.address, sendAmount)
    etherWallet.withdrawAll(etherWallet.owner())

    assert accounts[0].balance() == accountInitBalance
    assert etherWallet.balance() == 0


def test_notOwner_withdrawAll(etherWallet):
    accountInitBalance = accounts[0].balance()
    sendAmount = "1 ether"
    accounts[0].transfer(etherWallet.address, sendAmount)
    with reverts():
        etherWallet.withdrawAll(accounts[1], {"from": accounts[1]})

    assert accounts[0].balance() == accountInitBalance - sendAmount
    assert etherWallet.balance() == sendAmount


def test_emptyContract_withdrawAll(etherWallet):
    accountInitBalance = accounts[0].balance()
    withdrawAmount = "1 ether"
    with reverts():
        etherWallet.withdrawAll(etherWallet.owner())

    assert accounts[0].balance() == accountInitBalance
    assert etherWallet.balance() == 0
