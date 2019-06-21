import React, { Component } from 'react';

export default class ChangeMe extends Component {

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

            </div>
        )
    }
}

