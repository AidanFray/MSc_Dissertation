import React, { Component } from 'react';

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
                ID: <br/> <b>{window.expr_id}</b>
                <br/>
                <br/>
                After submitting your ID you may close the window.
            </div>
        )
    }
}

