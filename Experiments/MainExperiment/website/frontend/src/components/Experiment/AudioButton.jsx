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
            id: this.randomNumber()
        }
    }

    randomNumber() {
        return Math.random()
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
        this.props.toggleButtonCallback()
    }

    handleSongFinishedPlaying() {
        this.setState({
            playing: false,
            loading: false,
            id: this.randomNumber()
        })
        this.props.toggleButtonCallback()
    }


    render() {

        var buttonTextColor = "#ffffff"

        if (this.props.disabled) {
            buttonTextColor = "#222222"
        }

        return (
            <LoadingOverlay
                active={this.state.loading}
                text={this.state.loadingText}
            >
                <button
                style={{
                    alignItems: "center",
                    width: "200px",
                    color: buttonTextColor,
                    backgroundColor: this.props.color,
                }}
                disabled={this.props.disabled}
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

