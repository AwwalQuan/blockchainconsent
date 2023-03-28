// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;

contract Consent {
    string public patientName;
    string public surgeryType;
    string public surgeryDate;
    string public risks;
    address public patientAddress;
    string public surgeonIdentity; // surgeon's Ethereum address or digital certificate
    uint public validityPeriod; // in seconds
    uint public consentTimestamp; // timestamp when consent was signed
    bool public isConsentSigned;
    
    constructor(string memory _patientName, string memory _surgeryType, string memory _surgeryDate, string memory _risks, address _patientAddress, string memory _surgeonIdentity, uint _validityPeriod) {
        patientName = _patientName;
        surgeryType = _surgeryType;
        surgeryDate = _surgeryDate;
        risks = _risks;
        patientAddress = _patientAddress;
        surgeonIdentity = _surgeonIdentity;
        validityPeriod = _validityPeriod;
        isConsentSigned = false;
    }
    
    function signConsent() public {
        require(msg.sender == patientAddress, "Only the patient can sign the consent");
        require(block.timestamp < consentTimestamp + validityPeriod, "Consent has expired");
        isConsentSigned = true;
        consentTimestamp = block.timestamp;
    }
    
    function revokeConsent() public {
        require(msg.sender == patientAddress, "Only the patient can revoke their consent");
        isConsentSigned = false;
    }
    
    function getConsentDetails() public view returns (string memory, string memory, string memory, string memory, string memory, uint, bool) {
        return (patientName, surgeryType, surgeryDate, risks, surgeonIdentity, consentTimestamp, isConsentSigned);
    }
}
