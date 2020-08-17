import React, { Component } from 'react';
import Webcam from "react-webcam";
import './emotionCap.css';
import axios from "axios";
import testimg from '../../images/test.png';


class EmotionCap extends Component{
    constructor(props){
        super(props);
        this.state = {
            screenshot: null,
            resImg: null
        }
    }
    capture() {
        const screenshot = this.refs.webcamref.getScreenshot({width:480, height:360});
        this.setState({screenshot: screenshot});
    }
    
    handleSubmit(){
        let img = new FormData()
        const buff = new Buffer(this.state.screenshot.split(",")[1], 'base64')
        img.append("uploadFile", new Blob([buff], {type: 'application/octet-stream'}), 'image.jpeg');
        // console.log(typeof(this.state.screenshot))
        axios
        .post("http://127.0.1.1:8080/predict/", img)
        .then(res => {
            console.log(res.data);
            this.setState({
                resImg: res.data
            })
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
                {
                    this.state.resImg &&
                    this.state.resImg.map((eachImage, i) => {
                        return (
                            <img src={eachImage.image_url} alt="image" key={i}/>
                        )
                    })
                }
            </div>
        );
    }
}
    
export default EmotionCap;
