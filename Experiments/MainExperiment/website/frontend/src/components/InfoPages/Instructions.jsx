import React, { Component } from 'react';


import {Button, Paper, Typography} from '@material-ui/core/';
import {paper, text} from '../../stylesheets/material_style.jsx'
import {KeyboardArrowRight} from '@material-ui/icons';

var phone_image = require("../../images/phone.png");
var trustwords_image = require("../../images/trustwords.png")
var audio_button_image = require("../../images/audio_button.png")
var finish_images = require("../../images/finish.png")

class Instruction extends Component {

    constructor(props) {
        super(props);
        if (window.performance) {
            console.log(performance.navigation.type)
        }
    }

    routeChange() {
        let path = '/experiment';
        this.props.history.push(path);
    }

    render() {

        // Adds a dialog box checking if refresh is the desired action
        window.onbeforeunload = function() {return "X";}

        return (
            <div>
                
                <Typography variant="h4">
                    INSTRUCTIONS
                </Typography>

                <div>
                    <br />
                    <Paper style={paper}>
                        <Typography style={text}>
                            This experiment is investigating the handshake of secure email. Below are the steps required to complete the experiment.
                        </Typography>
                        <br/>
                        <Typography style={text}>
                            In order to make communication with a partner secure & trusted a handshake is required. This is to verify, that the 
                            communication between you and your communication 
                            partner happens between and only between the two of you. One way to achive this is the comparison of words. This is the process you'll be completing today. 
                        </Typography>
                        <br/>
                        <Typography style={text}>
                            You'll initially be provided with a virtual device like the one below that will allow you to interact with the experiment.
                        </Typography>
                        <br/>
                        <img 
                            alt="" 
                            height="400px" 
                            src={phone_image}
                        />
                        <br/>
                    </Paper>
                    <br/><br/>
                    <Paper style={paper}>
                        <Typography  style={text} variant="h6"> Step 1 </Typography>
                        <Typography style={text}>
                            Read the words displayed on the device. 
                        </Typography>
                        <br/>
                        <Typography style={text}>
                            An example of the words are shown below:
                        </Typography>
                        <br/>
                        <img height="30px" alt="" src={trustwords_image}/>
                    </Paper>
                    <br/><br/>
                    <Paper style={paper}>
                        <Typography style={text} variant="h6"> Step 2 </Typography>
                        <Typography style={text}>
                            After familiarization with the words clicking the button pictured below will produce spoken audio of the words (This can be pressed multiple times to repeat the audio).
                        </Typography>
                        <br/>
                            <img alt="" src={audio_button_image}/>
                        <br/>
                        <br/>
                        <Typography style={text}>
                            While listing to the audio, you need to decide if it matches the words displayed.
                        </Typography>
                        <br/>
                        <Typography style={{color: "#00aa00"}}>
                            ACCEPT - If they do match 
                        </Typography>
                        <br/>
                        <Typography style={{color: "#ff0000"}}>
                            DECLINE - If they do not match
                        </Typography>
                        <br/>
                    </Paper>
                    <br/><br/>
                    <Paper style={paper}>
                        <Typography style={text} variant="h6"> Step 3</Typography>
                        <Typography style={text}>
                            Finally, after a number of responses have been recorded you will be directed to the final page where the device will
                            display the final message.
                            <br/>
                            <br/>
                            The message will look like the image below:
                        </Typography>
                        <br/>
                        <img alt="" height="500px" src={finish_images}/>
                    </Paper>
                    <br />
                </div>

                <Typography variant="p">
                        When ready, please click the button below to start the experiment.
                </Typography>
                <br/>
                <br/>
                <Button 
                    style={{display: this.props.showNextButton}}
                    variant="contained" 
                    active={false}
                    color="primary" 
                    onClick={() => this.routeChange()}

                >
                    Next <KeyboardArrowRight/>
                </Button>
                <br/><br/>
            </div>
        )
    }
}

export default Instruction