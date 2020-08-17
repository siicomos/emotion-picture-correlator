import React, { Component } from 'react';
import Webcam from "react-webcam";
import './emotionCap.css';
import axios from "axios";
import testimg from '../../images/test.png';

class EmotionCap extends Component{
    constructor(props){
        super(props);
        this.state = {screenshot: null}
    }
    capture() {
        const screenshot = this.refs.webcamref.getScreenshot({width:480, height:360});
        this.setState({screenshot: screenshot});
    }
    
    handleSubmit(){
        let img = new FormData()
        img.append("uploadFile", new Blob([this.state.screenshot], {type: 'application/octet-stream'}), 'image.jpeg');
        // console.log(typeof(this.state.screenshot))
        axios
        .post("http://localhost:8080/predict", img)
        .then(function(res){
            console.log(res.data);
        })
        .catch(function(err){
            console.log(err);
        })

    }
    
    render(){
        return (
            <div>
                <p>Test in EmotionCap page</p>
                <Webcam
                    audio = {false}
                    height = {360}
                    ref='webcamref'
                    screenshotFormat = "image/jpeg"
                /> 
                <button onClick={this.capture.bind(this)}>Take photo</button>
                {this.state.screenshot && (
                    <img id="tmp_screenshot"
                        src = {this.state.screenshot}
                    />
                )}
                {this.state.screenshot && (
                    <button onClick={this.handleSubmit.bind(this)}>
                        Explore
                    </button>
                )}
            </div>
        );
    }
}
    
export default EmotionCap;