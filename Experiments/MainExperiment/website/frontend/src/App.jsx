import React, { Component } from 'react';

import { BrowserRouter as Router, Route } from "react-router-dom";

import TrustwordsSimulation from './components/Experiment/Simulation' 
import LandingPage from './components/Experiment/LandingPage.jsx' 

import Consent from './components/InfoPages/Consent.jsx'
import Instruction from './components/InfoPages/Instructions.jsx'
import PostExperiment from './components/InfoPages/PostExperiment.jsx'

import './stylesheets/App.css';

export default class App extends Component {

  render() {

    var isMobile = {
      Android: function() {
          return navigator.userAgent.match(/Android/i);
      },
      BlackBerry: function() {
          return navigator.userAgent.match(/BlackBerry/i);
      },
      iOS: function() {
          return navigator.userAgent.match(/iPhone|iPod/i);
      },
      Opera: function() {
          return navigator.userAgent.match(/Opera Mini/i);
      },
      Windows: function() {
          return navigator.userAgent.match(/IEMobile/i) || navigator.userAgent.match(/WPDesktop/i);
      },
      any: function() {
          return (isMobile.Android() || isMobile.BlackBerry() || isMobile.iOS() || isMobile.Opera() || isMobile.Windows());
      }
    };

    return (
        <Router>
          <Route exact path="/" component={Consent} />
          <Route exact path="/experiment" component={LandingPage} />
          <Route exact path="/instructions" component={Instruction} />
          <Route exact path="/post_experiment" component={PostExperiment} />
          <Route exact path="/bd65600d-8669-4903-8a14-af88203add38/" component={TrustwordsSimulation} />
        </Router>
      );
    }
  } 
