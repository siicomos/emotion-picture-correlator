import React, { Component } from 'react';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";
// import Switch from 'react-bootstrap/esm/Switch';
import Home from './pages/home-page/Home';
import About from './pages/about-page/About';
import EmotionCap from './pages/emotionCap-page/emotionCap';
import TestImage from './testImage';
import Navbar from './pages/home-page/Navbar';
import './App.css';

class App extends React.Component{
  render(){
    return (
      <div id='app-id'>
        <React.Fragment>
          <Router>
            <Navbar/>
              <Route exact path='/' component={Home}/>
              <Route path='/about' component={About}/>
              <Route path='/webcam' component={EmotionCap}/>
              <Route path='/testImage' component={TestImage}/>
          </Router>
        </React.Fragment>
      </div>
    );
  }
}

export default App;
