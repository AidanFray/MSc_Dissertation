import React from 'react';
import Device from "react-device-frame";
import SplitterLayout from 'react-splitter-layout';

import 'react-splitter-layout/lib/index.css';

import AudioComponent from './TrustwordAudio.jsx'

function LandingPage() {
    return (
        <SplitterLayout>
            <div style={{margin: "30px"}}>
                <Device name="iphone-8" color='black' url="http://localhost:3000/bd65600d-8669-4903-8a14-af88203add38" />
            </div>
            {/* <div style={{display: 'flex',  justifyContent:'center', alignItems:'center', height: '100vh'}}>
                <AudioComponent/>
            </div> */}
        </SplitterLayout>
    );
}
  
export default LandingPage;