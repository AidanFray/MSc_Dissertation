import React, { Component } from 'react';

var BASE_URL = "http://localhost:5000/get_audio"

export default class TrustwordAudio extends Component {

    constructor(props) {
        super(props);
        this.audio = new Audio(BASE_URL);
    }

    render() {
        return (
            <div>
                <button onClick={() => this.audio.play()}>
                    AUDIO
                </button>
            </div>
        );
    }
}