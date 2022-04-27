import React, {useState, useEffect} from 'react';
import {Card, Button} from 'semantic-ui-react';
import factory from '../ethereum/factory';

const campaignIndex =  (props) =>{ 

    const renderCampaigns = ()=> {
        const items = props.campaigns.map(address => {
            return{
                header: address,
                description: <a>View campaign</a>,
                fluid: true
            }
        });

        return <Card.Group items={items}/>
    }

    return (
        <div>
            <link
    async
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/npm/semantic-ui@2/dist/semantic.min.css"
  />
  <script src="https://cdn.jsdelivr.net/npm/semantic-ui-react/dist/umd/semantic-ui-react.min.js"></script>

            <h3>Open Campaigns</h3>

            {renderCampaigns()}
            <Button content="Create Campaign" 
                    icon="add circle"
                    primary  // Boolean props can be sent directly like this
                    />
        </div>
        
    )
};

campaignIndex.getInitialProps = async () => {
    const campaigns = await factory.methods.getDeployedCampaigns().call();

    return {campaigns};
};

export default campaignIndex;