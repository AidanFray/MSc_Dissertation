import React, { Component } from 'react';

export default class Demographics extends Component {

    constuctor() {
        this.routeChange = this.routeChange.bind(this);
    }
    
    routeChange() {
        let path = '/';
        this.props.history.push(path);
    }

    render() {
        return (
            <form action="https://getform.io/f/7b5dc57e-d431-418c-bf7c-6bbc583be69a" method="POST" enctype="multipart/form-data">
                <input type="text" name="name"/>
                <button type="submit">Send</button>
            </form>
        )
    }
}

