// SPDX-License-Identifier: MIT
pragma solidity 0.8.17;

import "@openzeppelin/contracts/access/Ownable.sol";

contract EtherWallet is Ownable {
    event EtherWithdrawn(uint256 amount);
    event EtherReceived(address indexed sender, uint256 amount);

    constructor() {}

    receive() external payable {
        emit EtherReceived(msg.sender, msg.value);
    }

    function withdraw(uint256 amount) external payable onlyOwner {
        require(amount <= address(this).balance, "Insufficient funds");
        require(address(this).balance > 0, "The contract is empty");

        (bool sent, ) = msg.sender.call{value: amount}("");
        require(sent, "Failed to send Ether");
        emit EtherWithdrawn(amount);
    }

    function withdrawAll(address payable _to) external payable onlyOwner {
        require(msg.value <= address(this).balance, "Insufficient funds");
        require(address(this).balance > 0, "The contract is empty");

        (bool sent, ) = _to.call{value: address(this).balance}("");
        require(sent, "Failed to send Ether");
        emit EtherWithdrawn(msg.value);

        emit EtherWithdrawn(address(this).balance);
    }

    function getBalance() external view returns (uint256) {
        return address(this).balance;
    }
}
