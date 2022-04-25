// contract test code will go here

const assert = require('assert');
const ganache = require('ganache-cli');
const Web3 = require('web3'); // Standard as whenever we use Web3 we are actually calling a constructor hence capital W in Web
const web3 = new Web3(ganache.provider());
const {interface, bytecode} = require('../compile');

let accounts;
let inbox;
const INITIAL_MESSAGE = 'Hi there!'
const NEW_MESSAGE = 'Trying To Change Message'

beforeEach( async ()=>{
    // Get a list of all accounts
    // web3.eth.getAccounts().then(fetchedAccounts => {
    //     console.log(fetchedAccounts)
    // } )

    accounts = await web3.eth.getAccounts();
    //use of of those accounts to deploy the contract
    inbox = await new web3.eth.Contract(JSON.parse(interface))
       .deploy({ data : bytecode, arguments : ['Hi there!'] })
       .send({ from:accounts[0], gas:'1000000' });
});

describe('Inbox', () => {
    it('deploys a contract', () => {
        assert.ok(inbox.options.address);
    });

    it('has a default message', async ()=>{
        const message = await inbox.methods.message().call(); // Call for non contract changing calls
        assert.equal(INITIAL_MESSAGE, message)
    });

    it('can change the message', async () => {
        await inbox.methods.setMessage(NEW_MESSAGE).send({ from : accounts[0] }); // send to send transactions for contract changing methods
        const message = await inbox.methods.message().call();
        assert.equal(message, NEW_MESSAGE);
    })
})

