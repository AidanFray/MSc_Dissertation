import React, { Component } from 'react';
import { View, Image, StyleSheet, Text} from 'react-native';

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
    height: "45vh",
    resizeMode: "stretch"
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

    this.refresh_words();
  }

  onClick_accept() {
    fetch(BASE_URL + '/debug?debug=accept')
    .then(function(response) {
      return response.text();
    })
    .then(function(text) {
      console.log(text);
      alert(text);
    })
    this.refresh_words();
  }
  
  onClick_decline() {
    fetch(BASE_URL + '/debug?debug=decline')
    .then(function(response) {
      return response.text();
    })
    .then(function(text) {
      console.log(text);
      alert(text);
    })
    this.refresh_words();
  }

  play_audio() {
    var audio = new Audio(BASE_URL + "/get_audio?id=" + this.state.expr_id);
    audio.play()
  }

  refresh_words() {
    fetch(BASE_URL +'/new_experiment?similar=TODO')
    .then(response => response.text()) 
    .then(t => 
      {
        this.setState({expr_id: t})
        console.log(t)

        fetch(BASE_URL +'/get_words?id=' + t)
        .then(response => response.text()) 
        .then(t => this.setState({words: t}))
      });
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
          <button onClick={() => this.play_audio()}>
            AUTHENTICATE OVER CALL
          </button>
      </View> 
      );
  }

  
}
  