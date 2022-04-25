const path = require('path');
const fs = require('fs');
const solc = require('solc');

const inboxPath = path.resolve(__dirname, 'contracts', 'Inbox.sol');  //good coding practice for cross platform compatilbilty 
const source = fs.readFileSync(inboxPath, 'utf8');

const input = {
    language: 'Solidity',
    sources: {
        'Inbox.sol': {
            content: source,
        },
    },
    settings:{
        outputSelection:{
            '*': {
                '*':['*'],
            }
        }
    }
}
console.log(JSON.parse(solc.compile(JSON.stringify(input))))

module.exports = JSON.parse(solc.compile(JSON.stringify(input))).contracts['Inbox.sol'].Inbox;



 