import React from 'react';
import { BrowserRouter as Router, Route } from "react-router-dom";

import TrustwordsSimulation from './components/TrustwordsSimulation' 
import LandingPage from './components/LandingPage.jsx' 

import './stylesheets/App.css';

function App() {
  return (
    <Router>
      <Route exact path="/" exact component={LandingPage} />
      <Route exact path="/bd65600d-8669-4903-8a14-af88203add38/" exact component={TrustwordsSimulation} />
    </Router>
  );
}

export default App;
