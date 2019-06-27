import React, { Component } from 'react';

import Device from "react-device-frame";
import SplitterLayout from 'react-splitter-layout';

import AudioButton from '../Experiment/AudioButton.jsx'

import 'react-splitter-layout/lib/index.css';


export default class LandingPage extends Component {

    constructor(props) {
        super(props);

        this.state = 
        {
            width: 0,
            height: 0,
            device_scale: 1,
            device_margin: 0
        };

        this.device_ref = React.createRef()
        this.deviceInitialMargin = 30

        this.updateWindowDimensions = this.updateWindowDimensions.bind(this);
      }

    componentDidMount() {
        this.updateWindowDimensions();
        window.addEventListener('resize', this.updateWindowDimensions);
    }
      
    componentWillUnmount() {
        window.removeEventListener('resize', this.updateWindowDimensions);
    }
    
    updateWindowDimensions() {

        var deviceMargin = 0
        var deviceScale = 1

        var deviceHeight = this.device_ref.current.clientHeight + (this.deviceInitialMargin * 2) 

        if (deviceHeight > window.innerHeight) {
            deviceScale = window.innerHeight / deviceHeight
            deviceMargin = (window.innerHeight - deviceHeight) / 2
        }

        this.setState({ 
            width: window.innerWidth, 
            height: window.innerHeight,
            device_scale: deviceScale,
            device_margin: deviceMargin
        });
    }

    routeChange(path) {
      this.props.history.push(path);
    }

    render() {

        return (
                <SplitterLayout percentage={true} primaryMinSize={70}>

                    <div ref={this.device_ref} style={{margin: this.deviceInitialMargin + "px"}}>
                        <style>
                        {`
                            .marvel-device
                            {
                                transform: scale(${this.state.device_scale});
                                margin: ${this.state.device_margin}px;
                            }
                        `}
                        </style>
                        <Device name="iphone-8" color='black' url="/bd65600d-8669-4903-8a14-af88203add38" />
                    </div>
                    
                    <div style={{
                        height: "100%",
                        width: "100%",
                        display: "flex",
                        justifyContent: 'center',
                        alignItems: 'center',
                        flexDirection: "column"
                    }}>
                        <div>
                            <AudioButton text="Authenticate with partner over the phone" color="#0000aa"/>
                        </div>
                    </div>
                    
                </SplitterLayout>
        );
    }
}