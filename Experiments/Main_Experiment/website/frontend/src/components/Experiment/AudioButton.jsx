import React, { Component } from 'react'
import {Phone} from '@material-ui/icons';

import LoadingOverlay from 'react-loading-overlay';

import Sound from 'react-sound'

var URL_BASE = "http://localhost:5000" //DEBUG

export default class AudioButton extends Component {

    constructor(props) {
        super(props)

        this.state = {playing: false}
        this.unique_request_id = new Date().getTime()

    }

    _play_audio() {
        this.setState({
            playing: !this.state.playing,
            loading: true
        })
    }

    handleSongLoaded(sound) {
        if (sound.loaded) {
            this.setState({
                loading: false
            })
            this.unique_request_id = new Date().getTime()
        }
    }

    render() {
        return (
            <LoadingOverlay
                active={this.state.loading}
                text='Loading audio ...'
            >
                <button
                style={{
                    alignItems: "center",
                    width: "200px",
                    color: "#ffffff",
                    backgroundColor: this.props.color,
                }}
                onClick={() => this._play_audio()}>
                    <br/>
                    <Phone size={250} />
                    <br/>
                    <p style={{fontSize: "15px"}}>
                        {this.props.text}
                    </p>
                    <br/>
                </button>

                {/* // The `time` parameter isn't actually used, but it stops the browser from reusing
                // previous audio instead of requesting a new one. The browser sees the request is 
                // different and makes another call to `get_audio`.*/}
                {this.state.playing &&
                    <Sound
                        url={URL_BASE + "/get_audio?time=" + this.unique_request_id}
                        playStatus={Sound.status.PLAYING}
                        // onLoading={() => this.handleSongLoading()}
                        onLoad={(loaded) => this.handleSongLoaded(loaded)}
                        onPlaying={this.handleSongPlaying}
                        onFinishedPlaying={this.handleSongFinishedPlaying}
                    />
                }
            </LoadingOverlay>
        )
    }
}

