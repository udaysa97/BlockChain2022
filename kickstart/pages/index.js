import React, {useState, useEffect} from 'react';
import factory from '../ethereum/factory';

const campaignIndex =  (props) =>{ 

    return (
        <h1>{props.campaigns[0]}</h1>
    )
};

campaignIndex.getInitialProps = async () => {
    const campaigns = await factory.methods.getDeployedCampaigns().call();

    return {campaigns};
};

export default campaignIndex;