import React, { Component } from 'react'
import {Phone} from '@material-ui/icons';
import Cookies from 'universal-cookie';

const cookies = new Cookies();

export default class AudioButton extends Component {

    play_audio() {
        // The `time` parameter isn't actually used, but it stops the browser from reusing
        // previous audio instead of requesting a new one. The browser sees the request is 
        // different and makes another call to `get_audio`.
        var audio = new Audio("/get_audio?id=" + cookies.get('ExperimentID') + "&time=" + new Date().getTime());
        
        audio.play()
      }

    render() {
        return (
            <button
            style={{
                alignItems: "center",
                width: "200px",
                color: "#ffffff",
                backgroundColor: this.props.color,
            }}
            onClick={() => this.play_audio()}>
                <br/>
                <Phone size={250} />
                <br/>
                <p style={{fontSize: "15px"}}>
                    {this.props.text}
                </p>
                <br/>
            </button>
        )
    }
}

