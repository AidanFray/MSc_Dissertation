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
            <div>
                This is the end
            </div>
        )
    }
}

