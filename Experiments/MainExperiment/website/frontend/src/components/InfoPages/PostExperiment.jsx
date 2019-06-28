import React, { Component } from 'react';

var URL_BASE = ""

export default class PostExperiment extends Component {

    constructor(props) {
        super(props)

        this.state = {
            id: ""
        }
    }

    componentDidMount() {
        this.request_id()
    }

    request_id() {
        fetch(URL_BASE + '/get_id')
          .then((r) => r.text())
          .then((t) => {
              console.log(t)
              this.setState({
                id: t
              })
          })
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
                ID: <br/> <b>{this.state.id}</b>
                <br/>
                <br/>
                After submitting your ID you may close the window.
            </div>
        )
    }
}

