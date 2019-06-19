import React, { Component } from 'react';

import { View, Image, StyleSheet, Text} from 'react-native';

let styles = StyleSheet.create({
  top: {
    height: "30vh",
    resizeMode: 'stretch'
  },
  bottom: {
    height: "15vh",
    resizeMode: 'stretch'
  },
  filler: {
    height: "51.5vh",
    resizeMode: "stretch"
  }
});

var trustword_top = require("../images/trustwords_top.jpg");
var trustword_bottom = require("../images/trustwords_bottom.jpg");
var trustword_filler = require("../images/trustwords_filler.jpg");


export default class TrustwordImage extends Component {

  render() {
  return (
      <View style={{backgroundColor: "white"}}>
          <Image
            source={trustword_top}
            style={styles.top}
          />
          <Text style={{ backgroundColor: "white", color: "black" }}>
            SPACESHIP MOUNTAIN FORREST DOG
          </Text>
          <Image
            source={trustword_bottom}
            style={styles.bottom}
          />  
          <Image
            source={trustword_filler}
            style={styles.filler}
          />         
      </View> 
      );
  }
}
  