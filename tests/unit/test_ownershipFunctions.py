from brownie import accounts, reverts, ZERO_ADDRESS


def test_constructor(etherWallet):
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
