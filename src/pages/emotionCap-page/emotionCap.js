import React, { Component } from 'react';
import Webcam from "react-webcam";
import './emotionCap.css'
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
    URLgenerator(){
        // 把截屏存成url的方法：
        // let image = new Blob([screenshot], {'type' : 'image/jpeg'});
        // // document.getElementById('tmp_screenshot').src = window.URL.createObjectURL(image);
        // var test = window.URL.createObjectURL(image);
        // console.log(test)
        var img = document.createElement('img');
        img.src = testimg;
        document.body.appendChild(img);
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
                    <button onClick={this.URLgenerator.bind(this)}>
                        Explore
                    </button>
                )}
            </div>
        );
    }
}
    
export default EmotionCap;