import React, { Component } from 'react';
import Cookies from 'universal-cookie';

const cookies = new Cookies();

export default class PostExperiment extends Component {

    constuctor() {
        this.routeChange = this.routeChange.bind(this);
    }
    
    routeChange() {
        let path = '/';
        this.props.history.push(path);
    }


    render() {
        return (
            <div style={{backgroundColor: "#000000", color: "#ffffff", height: "100vh"}}>
                <br/>
                This is the end of the experiment. Thank you for your time and attention.
                <br/>
                <br/>
                Please submit your unique ID to MTurk for payment
                <br/>
                <br/>
                ID: <br/> <b>{cookies.get('ExperimentID')}</b>
                <br/>
                <br/>
                After submitting your ID you may close the window.
            </div>
        )
    }
}

