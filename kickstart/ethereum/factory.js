import web3 from './web3';
import CampaignFactory from './build/CampaignFactory.json';

const instance  = new web3.eth.Contract(
    JSON.parse(CampaignFactory.interface),
    '0xD9bCd58bB4205FA77c35F422eF9af8DFFEC61Fa1'

);

export default instance;