import React, { Component } from 'react';

import { BrowserRouter as Router, Route } from "react-router-dom";

import TrustwordsSimulation from './components/Experiment/Simulation'
import LandingPage from './components/Experiment/LandingPage.jsx'

import Consent from './components/InfoPages/Consent.jsx'
import Instruction from './components/InfoPages/Instructions.jsx'
import PostExperiment from './components/InfoPages/PostExperiment.jsx'
import Demographics from './components/InfoPages/Demographics.jsx'

import './stylesheets/App.css';

function areCookiesEnabled() {
  console.log("cookie")
  try {
    document.cookie = 'cookietest=1';
    var cookiesEnabled = document.cookie.indexOf('cookietest=') !== -1;
    document.cookie = 'cookietest=1; expires=Thu, 01-Jan-1970 00:00:01 GMT';
    return cookiesEnabled;
  } catch (e) {
    return false;
  }
}


export default class App extends Component {

  render() {

    if (areCookiesEnabled()) {
      return (
        <Router>
          <Route exact path="/" component={Consent} />
          <Route exact path="/demographics" component={Demographics} />
          <Route exact path="/instructions" component={Instruction} />
          <Route exact path="/experiment" component={LandingPage} />
          <Route exact path="/post_experiment" component={PostExperiment} />
          <Route exact path="/bd65600d-8669-4903-8a14-af88203add38/" component={TrustwordsSimulation} />
        </Router>
      );
    }
    else {
      return (
        <div>
          <div>
            This experiment cannot be completed with cookied deactivated.           
          </div>
          <div>
            Please enable cookies and reload the page.
          </div>
        </div>
      )
    }
  }
} 
