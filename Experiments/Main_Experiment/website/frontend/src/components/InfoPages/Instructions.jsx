import React, { Component } from 'react';

import {Button, Paper, Typography} from '@material-ui/core/';
import {paper} from '../../stylesheets/material_style.jsx'
import {KeyboardArrowRight} from '@material-ui/icons';


export default class Instruction extends Component {

    constuctor() {
        this.routeChange = this.routeChange.bind(this);
    }
    
    routeChange() {
        let path = '/experiment';
        this.props.history.push(path);
    }

    render() {
        return (
            <div id="container-instructions">

                <Typography variant="h4">
                    Instructions
                </Typography>

                <br />
                <Paper style={paper}>
                    <Typography>
                      This is the first page of instructions.
                    </Typography>
                    <Typography>
                      Here I can put lots of examples
                    </Typography>
                    <Typography>
                      And pictures
                    </Typography>
                </Paper>
                <br />

                <Button 
                    variant="contained" 
                    color="primary" 
                    onClick={() => this.routeChange()}
                >
                    Next <KeyboardArrowRight/>
                </Button>
            </div>
        )
    }
}

