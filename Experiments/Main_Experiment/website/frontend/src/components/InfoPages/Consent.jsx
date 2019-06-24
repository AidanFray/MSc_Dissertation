import React, { Component } from 'react';

import {Button, Paper, Typography} from '@material-ui/core/';
import {Print,  Cancel, CheckCircle} from '@material-ui/icons';

import {paper} from '../../stylesheets/material_style.jsx'

import { MuiThemeProvider, createMuiTheme } from '@material-ui/core/styles';

const theme = createMuiTheme({
    palette: {
      primary: { main: '#1e824c' }, // custom color in hex
      secondary: { main: '#cf000f' }
    }
  });

export default class Consent extends Component {

    constuctor() {
        this.routeChange = this.routeChange.bind(this);
    }
    
    routeChange() {
        let path = '/instructions';
        this.props.history.push(path);
    }

    render() {

        // Adds a dialog box checking if refresh is the desired action
        window.onbeforeunload = function() {return "X";}

        return (
            <MuiThemeProvider theme={theme}>
            <div id="container-consent">
                <div id="consent">
                    <Typography variant="h4">
                        We need your consent to proceed
                    </Typography>
                    <br />
                    <Paper style={paper}>
                        <Typography>
                            You have been invited to take part in a research study
                        </Typography>
                        <Typography component="p">
                            [CONSENT FORM GOES HERE]
                        </Typography>
                        <br/>

                        <Button variant="text" onClick={() => window.print()}>
                            Print
                            <Print/>
                        </Button>
                    </Paper>
                    <br />
                    <Typography variant="h7">
                        Do you understand and consent to these terms?
                    </Typography>
                    <br />
                    <center>
                        <Button style={{margin: "10px"}} variant="contained" color="primary" onClick={() => this.routeChange()}>
                            Agree <CheckCircle/>
                        </Button>
                        <Button style={{margin: "10px"}} variant="contained" color="secondary">
                            Disagree <Cancel/>
                        </Button>
                    </center>

                </div>
            </div>
            </MuiThemeProvider>
        )
    }
}

