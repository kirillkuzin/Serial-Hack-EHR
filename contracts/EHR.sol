pragma solidity ^0.4.21;
pragma experimental ABIEncoderV2;


contract EHR {
    struct User {
        bytes firstNameCapsule;
        bytes lastNameCapsule;
        bytes dateOfBirthCapsule;
        bytes firstName;
        bytes lastName;
        bytes dateOfBirth;
        bytes32[] diseasesTimestamps;
    }
    mapping(address => User) public users;
    struct Disease {
        bytes diseaseTimestamp;
        address signature;
        bytes diseaseTimestampCapsule;
        bytes diagnosisCapsule;
        bytes therapyCapsule;
        bytes diagnosis;
        bytes therapy;
        bytes32[] historysTimestamps;
        bool closed;
        bytes result;
    }
    mapping(address => mapping(bytes32 => Disease)) public diseases;
    struct History {
        bytes historyTimestamp;
        bytes historyTimestampCapsule;
        bytes messageCapsule;
        address signature;
        bytes message;
    }
    mapping(address => mapping(bytes32 => mapping(bytes32 => History))) public historys;

    modifier diseaseIsOpen(address userAddress, bytes32 diseaseTimestamp) {
        Disease storage disease = diseases[userAddress][diseaseTimestamp];
        require(disease.closed == false);
        _;
    }

    function newUser(address userAddress, bytes firstNameCapsule, bytes lastNameCapsule, bytes dateOfBirthCapsule, bytes firstName, bytes lastName, bytes dateOfBirth) public {
        User storage user = users[userAddress];
        user.firstNameCapsule = firstNameCapsule;
        user.lastNameCapsule = lastNameCapsule;
        user.dateOfBirthCapsule = dateOfBirthCapsule;
        user.firstName = firstName;
        user.lastName = lastName;
        user.dateOfBirth = dateOfBirth;
    }

    function addDisease(address userAddress,bytes diseaseTimestampCapsule, bytes diagnosisCapsule, bytes therapyCapsule, bytes32 diseaseTimestamp, bytes timestamp, bytes diagnosis, bytes therapy) public diseaseIsOpen(userAddress, diseaseTimestamp) {
        Disease storage disease = diseases[msg.sender][diseaseTimestamp];
        disease.diseaseTimestamp = timestamp;
        disease.signature = msg.sender;
        disease.diseaseTimestampCapsule = diseaseTimestampCapsule;
        disease.diagnosisCapsule = diagnosisCapsule;
        disease.therapyCapsule = therapyCapsule;
        disease.diagnosis = diagnosis;
        disease.therapy = therapy;
        User storage user = users[userAddress];
        user.diseasesTimestamps.push(diseaseTimestamp);
    }

    function updateDisease(address userAddress, bytes historyTimestampCapsule, bytes messageCapsule, bytes32 diseaseTimestamp, bytes32 historyTimestamp, bytes timestamp, bytes message) public diseaseIsOpen(userAddress, diseaseTimestamp) {
        Disease storage disease = diseases[userAddress][diseaseTimestamp];
        disease.historysTimestamps.push(historyTimestamp);
        History storage history = historys[userAddress][diseaseTimestamp][historyTimestamp];
        history.historyTimestamp = timestamp;
        history.historyTimestampCapsule = historyTimestampCapsule;
        history.messageCapsule = messageCapsule;
        history.signature = msg.sender;
        history.message = message;
    }

    function closeDisease(address userAddress, bytes32 diseaseTimestamp, bytes result) public diseaseIsOpen(userAddress, diseaseTimestamp) {
        Disease storage disease = diseases[userAddress][diseaseTimestamp];
        disease.result = result;
        disease.closed = true;
    }

    function getDiseasesTimestamps(address userAddress) public constant returns(bytes32[]) {
        return users[userAddress].diseasesTimestamps;
    }

    function getHistorysTimestamps(address userAddress, bytes32 diseaseTimestamp) public constant returns(bytes32[]) {
        return diseases[userAddress][diseaseTimestamp].historysTimestamps;
    }
}
