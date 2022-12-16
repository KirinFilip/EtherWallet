from brownie import accounts

# --- Receive Function ---


def test_sendEtherToContract(etherWallet):
    accountInitBalance = accounts[0].balance()
    sendAmount = "1 ether"
    tx = accounts[0].transfer(etherWallet.address, sendAmount)

    assert accounts[0].balance() == accountInitBalance - sendAmount
    assert etherWallet.balance() and etherWallet.getBalance() == sendAmount
    assert "EtherReceived" in tx.events
