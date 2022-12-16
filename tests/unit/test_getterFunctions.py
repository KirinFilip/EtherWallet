from brownie import accounts


def test_getBalance(etherWallet):
    assert etherWallet.getBalance() == 0


def test_owner(etherWallet):
    assert etherWallet.owner() == accounts[0]
