# blockchainconsent
![demo](https://user-images.githubusercontent.com/48957591/228178655-4e9f086c-ec85-454c-ab1b-53c8c9b87b0c.gif)

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
![Sequence diagram](https://user-images.githubusercontent.com/48957591/228213352-954979d9-ad1e-4a07-b363-cafe49e45e3e.png)
