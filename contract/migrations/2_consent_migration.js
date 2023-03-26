var Consent = artifacts.require("./Consent.sol");

module.exports = function(deployer) {
    // Consent is the contract's name
    var patientName='Awwal';
    var surgeryType='Elbow';
    var surgeryDate='24-March-2024';
    var risks='None';
    var patientAddress='0x52CfF12eae83154d665011E493B144265E0385BE';
    var surgeonIdentity='Rufai';
    var validityPeriod='60';
    deployer.deploy(Consent, patientName, surgeryType, surgeryDate, risks, patientAddress, surgeonIdentity, validityPeriod);
};
