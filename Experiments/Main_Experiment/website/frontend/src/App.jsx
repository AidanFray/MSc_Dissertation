import React from 'react';
import { BrowserRouter as Router, Route } from "react-router-dom";

import TrustwordsSimulation from './components/TrustwordsSimulation' 
import LandingPage from './components/LandingPage.jsx' 

import './stylesheets/App.css';
import './stylesheets/iPhone.css';


function App() {
  return (
    <Router>
      <Route path="/" exact component={LandingPage} />
      <Route path="/bd65600d-8669-4903-8a14-af88203add38/" component={TrustwordsSimulation} />
    </Router>
  );
}

export default App;
