var Consent = artifacts.require("./Consent.sol");

module.exports = function(deployer) {
    // Consent is the contract's name
    var patientName='Awwal';
    var surgeryType='Elbow';
    var surgeryDate='24-March-2024';
    var risks='None';
    var patientAddress='0x52CfF12eae83154d665011E493B144265E0385BE';
    var surgeonIdentity='0x76f0961247eF40D4Ccc71aDC3F6ab3a56c36A44f';
    var validityPeriod='60000';
    deployer.deploy(Consent, patientName, surgeryType, surgeryDate, risks, patientAddress, surgeonIdentity, validityPeriod);
};
