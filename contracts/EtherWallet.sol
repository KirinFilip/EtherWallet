// SPDX-License-Identifier: MIT
pragma solidity 0.8.17;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/Pausable.sol";

contract EtherWallet is Ownable, Pausable {
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

    function getBalance() external view returns (uint256) {
        return address(this).balance;
    }
}
