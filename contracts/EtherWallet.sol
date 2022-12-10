// SPDX-License-Identifier: MIT
pragma solidity 0.8.17;

contract EtherWallet {
    address public owner;

    event EtherWithdrawn(uint256 amount);
    event EtherReceived(address indexed sender, uint256 amount);

    constructor() {
        owner = payable(msg.sender);
    }

    receive() external payable {
        emit EtherReceived(msg.sender, msg.value);
    }

    function withdraw() external payable {
        require(msg.sender == owner, "Only owner can withdraw funds");
        require(msg.value <= address(this).balance, "Insufficient funds");
        require(address(this).balance > 0, "The contract is empty");
        (bool sent, ) = owner.call{value: msg.value}("");
        require(sent, "Failed to send Ether");
        emit EtherWithdrawn(msg.value);
    }

    function getBalance() external view returns (uint256) {
        return address(this).balance;
    }
}
