import React, { Component } from 'react';


import {Button, Paper, Typography} from '@material-ui/core/';
import {paper, text} from '../../stylesheets/material_style.jsx'
import {KeyboardArrowRight} from '@material-ui/icons';

var phone_image = require("../../images/phone.png");
var trustwords_image = require("../../images/trustwords.png")
var audio_button_image = require("../../images/audio_button.png")

class Instruction extends Component {

    routeChange() {
        let path = '/experiment';
        this.props.history.push(path);
    }

    render() {

        return (
            <div>
                
                <Typography variant="h4">
                    Instructions
                </Typography>

                <div>
                    <br />
                    <Paper style={paper}>
                        <Typography style={text}>
                            This experiment is investigating authentication of secure email. Below are the steps required to complete the experiment.
                        </Typography>
                        <br/>
                        <Typography style={text}>
                        You'll initially be provided with a device that will allow you to interact with the experiment
                        </Typography>
                        <br/>
                        <img 
                            style={{ alignSelf: 'center', alignItems: 'center', justifyContent: 'center'}}
                            height="300px" 
                            src={phone_image}
                        />
                        <br/>
                        <Typography  style={text} variant="h6"> Step 1 </Typography>
                        <Typography style={text}>
                            Read the words displayed on the device. An example of the words are shown below:
                        </Typography>
                        <br/>
                            <img height="30px" src={trustwords_image}/>
                        <br/>
                        <br/>
                        <Typography style={text}>
                            These will be the elements you will need to verify to successfully authenticate.                        
                        </Typography>
                        <hr/>
                        <Typography style={text} variant="h6"> Step 2 </Typography>
                        <Typography style={text}>
                            After familiarization with the words you will need to initiate the authentication process. The image below shows this button. Clicking this will produce spoken audio of the words (This can be pressed multiple times to repeat the audio).
                        </Typography>
                        <br/>
                            <img src={audio_button_image}/>
                        <br/>
                        <br/>
                        <Typography style={text}>
                            While listing to the audio, you need to decide if it matches the words displayed previously.
                        </Typography>
                        <br/>
                        <Typography style={{color: "#00aa00"}}>
                            ACCEPT - If they do match 
                        </Typography>
                        <br/>
                        <Typography style={{color: "#ff0000"}}>
                            DECLINE - If they do not match
                        </Typography>
                        <br/><hr/>
                        <Typography style={text} variant="h6"> Step 3</Typography>
                        <Typography style={text}>
                            After submitting your choice, the experiment will move on and present some new words and recordings. This will need repeating for a number of sections
                        </Typography>
                        <br/><hr/>
                        <Typography style={text} variant="h6"> Step 4</Typography>
                        <Typography style={text}>
                            Finally, after a number of responses have been recorded you will be directed to the final page [...]
                        </Typography>
                    </Paper>
                    <br />
                </div>

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