// // contract test code will go here

// const assert = require('assert');
// const ganache = require('ganache-cli');
// const Web3 = require('web3'); // Standard as whenever we use Web3 we are actually calling a constructor hence capital W in Web
// const web3 = new Web3(ganache.provider());

// class Car {
//     park(){
//         return 'stopped';
//     }

//     drive() {
//         return 'vroom';
//     }
// }

// let car;

// beforeEach(() => {
//     car = new Car();
// })

// describe('Car', () =>{ //first argument is solely for us to know which output it is and not dependant on class
//     it('can park', () => {
//         assert.equal(car.park(), 'stopped');
//     });

//     it('can drive', () => {
//         assert.equal(car.drive(), 'vroom')
//     })

// })