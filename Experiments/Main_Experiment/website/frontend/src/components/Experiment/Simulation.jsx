import React, { Component } from 'react';
import { View, Image, StyleSheet, Text } from 'react-native';
import {Flip, ToastContainer, toast } from 'react-toastify';
import Cookies from 'universal-cookie';
import 'react-toastify/dist/ReactToastify.css';

const cookies = new Cookies();

var trustword_top = require("../../images/trustwords_top.jpg");
var trustword_filler = require("../../images/trustwords_filler.jpg");

var URL_BASE = "http://localhost:5000"

let styles = StyleSheet.create({
  top: {
    height: "30vh",
    resizeMode: 'stretch'
  },
  filler: {
    height: "25vh",
    resizeMode: "stretch"
  },
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

    this.setup_experiment();
  }

  experiment_finished(response_text) {
    if (response_text === "DONE") {

      this.props.history.push("/post_experiment")

      this.setState({
        controls_disabled: true,
        audio_button_visibility: "hidden"
      })

      return true
    }

    return false
  }

  onClick_accept() {
    toast.success("ACCEPT")
    fetch(URL_BASE + '/submit_result?id=' + this.expr_id + '&result=True')
      .then((response) => { return response.text() })
      .then((text) => {
        this.refresh_words(this.expr_id)
      })
  }

  onClick_decline() {
    toast.error("DECLINE" )
    fetch(URL_BASE + '/submit_result?id=' + this.expr_id + '&result=False')
      .then((response) => { return response.text() })
      .then((text) => {
        this.refresh_words(this.expr_id)
      })
  }

  setup_experiment() {
    fetch(URL_BASE + '/new_experiment?similar=TODO')
      .then(response => response.text())
      .then(t => {
        cookies.set('ExperimentID', t);
        this.expr_id = t
        this.refresh_words(t)
      })
  }

  refresh_words(id) {
    fetch(URL_BASE + '/get_words?id=' + id)
      .then(response => response.text())
      .then(t => {

        if (!this.experiment_finished(t)) {
          this.setState({ words: t })
        }
      })
  }

  render() {

    // Adds a dialog box checking if refresh is the desired action
    window.onbeforeunload = function () { return "X"; }

    return (
      <View style={{ backgroundColor: "white" }}>
        <Image
          source={trustword_top}
          style={styles.top}
        />
        <Text style={{ backgroundColor: "white", color: "black", margin: "10px" }}>
          {this.state.words}
        </Text>
        <button
          disabled={this.state.controls_disabled}
          style={{ 'margin': '10px', "backgroundColor": '#5cdd5c' }}
          onClick={() => this.onClick_accept()}>
          ACCEPT
          </button>
        <button
          disabled={this.state.controls_disabled}
          style={{ 'margin': '10px', "backgroundColor": '#ff5c5c' }}
          onClick={() => this.onClick_decline()}>
          DECLINE
          </button>
        <Image
          source={trustword_filler}
          style={styles.filler}
        />
        <ToastContainer 
          hideProgressBar={true} 
          autoClose={1000} 
          transition={Flip}
          pauseOnHover={false}
          newestOnTop
        />
      </View>
    );
  }


}
