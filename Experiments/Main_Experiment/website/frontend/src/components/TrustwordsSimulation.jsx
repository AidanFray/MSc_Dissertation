import React, { Component } from 'react';
import { View, Image, StyleSheet, Text} from 'react-native';
import {IoMdVolumeHigh} from "react-icons/io";


var BASE_URL = 'http://localhost:5000'
var trustword_top = require("../images/trustwords_top.jpg");
var trustword_filler = require("../images/trustwords_filler.jpg");

// ###################################################
// TODO: Error handling for situations where
//       the flask server is down
// ###################################################

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
        expr_id: [] 
    }

    this.setup_experiment();
  }

  onClick_accept() {
    fetch(BASE_URL + '/submit_result?id=' + this.expr_id + '&result=True')
    .then((response) => {response.text()})
    .then((text) => {this.refresh_words(this.expr_id)})
    this.refresh_words();
  }
  
  onClick_decline() {
    fetch(BASE_URL + '/submit_result?id=' + this.expr_id + '&result=False')
    .then((response) => {response.text()})
    .then((text) => {this.refresh_words(this.expr_id)})
    this.refresh_words();
  }

  play_audio() {
    var audio = new Audio(BASE_URL + "/get_audio?id=" + this.expr_id);
    audio.play()
  }


  setup_experiment() {
    fetch(BASE_URL +'/new_experiment?similar=TODO')
    .then(response => response.text()) 
    .then(t => {
      console.log(t)
      this.expr_id = t
      this.refresh_words(t)
    })
  }

  refresh_words(id) {
    fetch(BASE_URL +'/get_words?id=' + id)
    .then(response => response.text()) 
    .then(t => this.setState({words: t}))
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
            style={{'margin': '10px', "backgroundColor": '#5cdd5c'}} 
            onClick={() => this.onClick_accept()}>
            ACCEPT
          </button>
          <button 
            style={{'margin': '10px', "backgroundColor": '#ff5c5c'}} 
            onClick={() => this.onClick_decline()}>
            DECLINE
          </button>
          <Image
            source={trustword_filler}
            style={styles.filler}
          />        
          <button 
            style={{
              alignItems: "center",
              margin: "50px",
              height: "75px",
              color: "#ffffff",
              backgroundColor: "#000099"
            }} 
            onClick={() => this.play_audio()}>
            <IoMdVolumeHigh size={50}/>
          </button>
      </View> 
      );
  }

  
}
  