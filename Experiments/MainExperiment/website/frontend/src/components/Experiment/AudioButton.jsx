import React, { Component } from 'react'
import {Phone} from '@material-ui/icons';

import LoadingOverlay from 'react-loading-overlay';
import Sound from 'react-sound'

var LOADING_TEXT = "Loading audio"
var PLAYING_TEXT = "Playing audio"

export default class AudioButton extends Component {

    constructor(props) {
        super(props)

        this.state = {
            loading: false,
            playing: false,
            loadingText: LOADING_TEXT,
            id: 0
        }
    }

    _play_audio() {

        var text = LOADING_TEXT
        if (this.state.playing) {
            text = PLAYING_TEXT
        }

        this.setState({
            playing: true,
            loading: true,
            loadingText: text
        })
    }

    handleSongLoaded(sound) {
        if (sound.loaded) {
            this.setState({
                loading: false
            })
        }
    }

    handleSongFinishedPlaying() {
        this.setState({
            playing: false,
            loading: false,
            id: this.state.id += 1
        })
    }


    render() {
        return (
            <LoadingOverlay
                active={this.state.loading}
                text={this.state.loadingText}
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

                {this.state.playing &&
                    <Sound
                        url={"/get_audio?id=" + this.state.id}
                        playStatus={Sound.status.PLAYING}
                        onLoad={(loaded) => this.handleSongLoaded(loaded)}
                        onFinishedPlaying={() => this.handleSongFinishedPlaying()}
                    />
                }
            </LoadingOverlay>
        )
    }
}

