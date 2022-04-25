const HDWalletProvider = require('@truffle/hdwallet-provider');
const Web3 = require('web3');
const { abi, evm } = require('./compile');

const provider = new HDWalletProvider(  // In production or real wallets, this will be environment variable 
    'reopen sell parent kidney borrow grace myth clip energy chunk victory rescue',
    'https://rinkeby.infura.io/v3/293d042d9e8744eb8d7da6e0d1937c5f'
);
const web3 = new Web3(provider);

const deploy = async () => {
  const accounts = await web3.eth.getAccounts();

  console.log('Attempting to deploy from account', accounts[0]);

  const result = await new web3.eth.Contract(abi)
    .deploy({ data: evm.bytecode.object })
    .send({ gas: '1000000', from: accounts[0] });
    console.log(result)

    console.log(JSON.stringify(abi));

  console.log('Contract deployed to', result.options.address);
  provider.engine.stop();
};
deploy();
