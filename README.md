# blockchainconsent
![demo](https://user-images.githubusercontent.com/48957591/228177325-07306568-cc3a-4c0a-b8c4-3d93b7d3ac2a.gif)

## Requirements
- A local Ganache block chain.
- At least two accounts on the blockchain. One for the patient, and the second for the surgeon.

## Steps to simulate
1. Clone the repository `$ git clone https://github.com/AwwalQuan/blockchainconsent.git`
1. Navigate to the repository `$ cd blockchainconsent`
1. Create a smart contract. 
   - Modify the file `smartcontract/consent/migrations/2_consent_migration.js` and insert the patient and surgeon's Ethereum address.
   - In the `smartcontract/consent/` directory, run `$ truffle deploy` to deploy the contract
1. Run the slave robot `$ python3 slave_robot.py`. Enter the address and private key of the patient that created the contract.
1. Open another terminal and run the master console `$ python3 master_console.py`. Enter the surgeon's private key to authenticate the surgeon.

The following sequence diagram shows the authentication steps
![Sequence diagram](https://user-images.githubusercontent.com/48957591/228163581-68ba1536-055e-49b9-a507-d2e614016327.png)
