import Web3 from 'web3';

let web3;

if (typeof window !== "undefined" && typeof window.ethereum !== "undefined"){
    window.ethereum.request({method: "eth_requestAccounts"}); // Means we are in browser with metamask running
    web3 = new Web3(window.ethereum);
} else{
    const provider = new Web3.providers.HttpProvider(
        'https://rinkeby.infura.io/v3/293d042d9e8744eb8d7da6e0d1937c5f' // Either onserver or user does not have metamask
    );
    web3 = new Web3(provider);
}

export default web3;