// SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract AdvancedCollectible is ERC721, VRFConsumerBase {
    // adding tokenCounter to count the token IDs a.k.a. the number of tokens minted at this contract's address
    uint256 public tokenCounter;
    // initializing keyHash and fee variables for VRFCoordinator
    bytes32 public keyHash;
    uint256 public fee;
    mapping(uint256 => Breed) public tokenIdToBreed;
    mapping(bytes32 => address) public requestIdToSender;

    // when we update a mapping, it's a good practice to emit a respective event
    event breedAssigned(uint256 indexed tokenId, Breed breed);
    event requestedCollectible(bytes32 indexed requestId, address requester);

    enum Breed {
        PUG,
        SHIBA_INU,
        ST_BERNARD
    }

    constructor(
        address _vrfCoordinator,
        address _linkToken,
        bytes32 _keyHash,
        uint256 _fee
    )
        public
        VRFConsumerBase(_vrfCoordinator, _linkToken)
        ERC721("Dogie", "DOG")
    {
        tokenCounter = 0;
        keyHash = _keyHash;
        fee = _fee;
    }

    // this function returns requestID which will be used in the fulfilRandomness callback
    function createCollectible() public returns (bytes32) {
        // facilitating getting a random dog breed
        bytes32 requestId = requestRandomness(keyHash, fee);
        // creating a mapping to store msg.senders and then use them as a _safeMint() argument in fulfilRandomness()
        requestIdToSender[requestId] = msg.sender;
        emit requestedCollectible(requestId, msg.sender);
    }

    // only VRFCoordinator can call this function
    function fulfillRandomness(bytes32 requestId, uint256 randomness)
        internal
        override
    {
        // getting a random breed out of 3 breeds available
        Breed breed = Breed(randomness % 3);
        // mapping a current tokenId to the chosen breed
        uint256 newTokenId = tokenCounter;
        tokenIdToBreed[newTokenId] = breed;
        emit breedAssigned(newTokenId, breed);
        // we cannot use msg.sender as a _safeMint argument because the msg.sender for this function is VRFCoordinator
        address owner = requestIdToSender[requestId];
        _safeMint(owner, newTokenId);
        tokenCounter += 1;
    }

    // we need a function which sets a tokenURI based on the breed of the current tokenId
    // future improvement: make setting the tokenURI a part of fulfilRandomness()
    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        // now, we have on-chain metadata and we wanna reciprocate it with off-chain metadata
        // we also want only the tokenId owner to be able to call this function
        // _isApprovedOrOwner and _msgSender() are the functions from OpenZeppelin ERC721
        require(
            _isApprovedOrOwner(_msgSender(), tokenId),
            "ERC721: The caller is not the owner and not approved."
        );
        _setTokenURI(tokenId, _tokenURI);
    }
}
