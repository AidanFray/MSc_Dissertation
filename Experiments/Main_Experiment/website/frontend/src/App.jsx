import React from 'react';
import { BrowserRouter as Router, Route } from "react-router-dom";

import TrustwordsSimulation from './components/Experiment/Simulation' 
import LandingPage from './components/Experiment/LandingPage.jsx' 

import Consent from './components/InfoPages/Consent.jsx'
import Instruction from './components/InfoPages/Instructions.jsx'
import PostExperiment from './components/InfoPages/PostExperiment.jsx'

import './stylesheets/App.css';

function App() {
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

export default App;
