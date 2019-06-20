import React, { Component } from 'react';

import Device from "react-device-frame";
import SplitterLayout from 'react-splitter-layout';

import 'react-splitter-layout/lib/index.css';

import ExperimentDescription from './ExperimentDescription';


export default class LandingPage extends Component {

    render() {
        return (

            <SplitterLayout percentage={true} primaryMinSize={70}>

                <div>
                    <Device style={{height: 100}} name="iphone-8" color='black' url="http://localhost:3000/bd65600d-8669-4903-8a14-af88203add38" />
                </div>
                
                <div>
                    <ExperimentDescription/>
                </div>
            </SplitterLayout>
        );
    }
}