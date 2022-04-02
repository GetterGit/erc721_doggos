// SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

// inheriting all ERC721 functions by declaring that our conract is ERC721
// This is gonna be a factory conract for all future owners of the Shiba NFT implied in this contract
// meaning that in will have the mint function to mint many NFTs contained in this one contract
contract SimpleCollectible is ERC721 {
    // adding a counter to keep track of token id's
    uint256 public tokenCounter;

    constructor() public ERC721("Shibanu", "SBN") {
        tokenCounter = 0;
    }

    // anybody can come and create a puppy
    // essentially, we are assigning a new tokenId to a new owner
    function createCollectible(string memory tokenURI)
        public
        returns (uint256)
    {
        // _safeMint() checks whether the tokenId already exists to make sure we don't override anything
        uint256 newTokenId = tokenCounter;
        _safeMint(msg.sender, newTokenId);
        // setting the URI for the newly minted token
        _setTokenURI(newTokenId, tokenURI);
        // updaring the token counter to be used as the id for the next NFT minted on this contract
        tokenCounter += 1;
        return newTokenId;
    }
}
