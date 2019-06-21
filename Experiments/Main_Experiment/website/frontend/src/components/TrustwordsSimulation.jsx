import React, { Component } from 'react';
import { View, Image, StyleSheet, Text} from 'react-native';
import {IoMdVolumeHigh} from "react-icons/io";


var trustword_top = require("../images/trustwords_top.jpg");
var trustword_filler = require("../images/trustwords_filler.jpg");


let styles = StyleSheet.create({
  top: {
    height: "30vh",
    resizeMode: 'stretch'
  },
  filler: {
    height: "25vh",
    resizeMode: "stretch"
  },
  soundButton: {

  }
});

export default class TrustwordSimulation extends Component {

  constructor(props) {
    super(props);
    this.state = {
        words: [],
        audio_url: [],
        controls_disabled: false,
        audio_button_visibility: "visible"
    }

    this.expr_id = []
    this.setup_experiment();
  }

  experiment_finished(response_text) {
    console.log(response_text)  
    if (response_text === "DONE") {
      alert("The experiment is finished. \n\n" + this.expr_id)

      console.log(this)
      this.setState({
        controls_disabled: true,
        audio_button_visibility: "hidden"
      })

      return true
    }

    return false
  }

  onClick_accept() {
    fetch('/submit_result?id=' + this.expr_id + '&result=True')
    .then((response) => {return response.text()})
    .then((text) => {
      this.refresh_words(this.expr_id)
    })
  }
  
  onClick_decline() {
    fetch('/submit_result?id=' + this.expr_id + '&result=False')
    .then((response) => {return response.text()})
    .then((text) => {
      this.refresh_words(this.expr_id)
    })
  }

  play_audio() {
    var audio = new Audio("/get_audio?id=" + this.expr_id);
    audio.play()
  }


  setup_experiment() {
    fetch('/new_experiment?similar=TODO')
    .then(response => response.text()) 
    .then(t => {
      console.log(t)
      this.expr_id = t
      this.refresh_words(t)
    })
  }

  refresh_words(id) {
    fetch('/get_words?id=' + id)
    .then(response => response.text()) 
    .then(t => {
      
      if(!this.experiment_finished(t)) {
        this.setState({words: t})
      }
    })
  }

  render() {
  return (
      <View style={{backgroundColor: "white"}}>
          <Image
            source={trustword_top}
            style={styles.top}
          />
          <Text style={{ backgroundColor: "white", color: "black", margin: "10px" }}>
            {this.state.words}
          </Text>
          <button 
            disabled={this.state.controls_disabled}
            style={{'margin': '10px', "backgroundColor": '#5cdd5c'}} 
            onClick={() => this.onClick_accept()}>
            ACCEPT
          </button>
          <button 
            disabled={this.state.controls_disabled}
            style={{'margin': '10px', "backgroundColor": '#ff5c5c'}} 
            onClick={() => this.onClick_decline()}>
            DECLINE
          </button>
          <Image
            source={trustword_filler}
            style={styles.filler}
          />        
          <button 
            disabled={this.state.controls_disabled}
            style={{
              alignItems: "center",
              margin: "50px",
              height: "75px",
              color: "#ffffff",
              backgroundColor: "#0000cc",
              visibility: this.state.audio_button_visibility
            }} 
            onClick={() => this.play_audio()}>
            <IoMdVolumeHigh size={50}/>
          </button>
      </View> 
      );
  }

  
}
  