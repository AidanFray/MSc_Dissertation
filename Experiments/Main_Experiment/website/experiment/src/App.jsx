import React from 'react';
import './stylesheets/App.css';
import { BrowserRouter as Router, Route, Link } from "react-router-dom";

import TrustwordImage from './components/image.jsx' 

import Home from './components/home.jsx' 


function App() {
  return (
    <Router>
      <Route path="/" exact component={Home} />
      <Route path="/image/" component={TrustwordImage} />
    </Router>
  );
}

export default App;
