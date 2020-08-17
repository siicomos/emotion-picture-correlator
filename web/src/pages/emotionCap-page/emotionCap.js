import React, { Component } from 'react';
import Webcam from "react-webcam";
import './emotionCap.css';
import axios from "axios";
import ReactLoading from 'react-loading';
import Button from 'react-bootstrap/Button';
import Image from 'react-bootstrap/Image';
import testimg from '../../images/test.png';


class EmotionCap extends Component{
    constructor(props){
        super(props);
        this.state = {
            screenshot: null,
            resImg: null,
            loading: false
        }
    }
    capture() {
        const screenshot = this.refs.webcamref.getScreenshot({width:480, height:360});
        this.setState({screenshot: screenshot});
    }
    
    handleSubmit(){
        this.setState({loading: true});
        let img = new FormData()
        const buff = new Buffer(this.state.screenshot.split(",")[1], 'base64')
        img.append("uploadFile", new Blob([buff], {type: 'application/octet-stream'}), 'image.jpeg');
        // console.log(typeof(this.state.screenshot))
        axios
        .post("http://127.0.1.1:8080/predict/", img)
        .then(res => {
            console.log(res.data);
            this.setState({
                resImg: res.data,
                loading: false
            })
        })
        .catch(err => {
            if(err.response) {
                if(err.response.status == 406) {
                    alert("There are no face in the image you taken")
                } else if(err.response.status == 500) {
                    alert("Server side error")
                } else {
                    console.log(err)
                    alert("Server side error")
                }
            } else if (err.request) {
                console.log(err)
                alert("Server no response")
            }
            this.setState({
                loading: false
            })
        })

    }
    
    render(){
        return (
            <div id='webcam-id'>
                <p>Test in EmotionCap page</p>
                <Webcam id='webcam'
                    audio = {false}
                    height = {360}
                    ref='webcamref'
                    screenshotFormat = "image/jpeg"
                /> 
                <div class='text-center'>
                    <Button className="webcam-btn" variant="outline-secondary" onClick={this.capture.bind(this)}>Take photo</Button>
                </div>
                {this.state.screenshot && (
                    <img id="tmp_screenshot"
                        src = {this.state.screenshot}
                    />
                )}
                <div class='text-center'>
                    {this.state.screenshot && (
                        <Button className="webcam-btn" variant="outline-secondary" onClick={this.handleSubmit.bind(this)}>
                        {
                            !this.state.loading ?
                            "Explore" :
                            <ReactLoading type={"bubbles"} height={100} width={100} color={'black'}/>
                        }
                        </Button>
                    )}
                </div>
                <div class='text-center'>
                    {
                        this.state.resImg &&
                        this.state.resImg.map((eachImage, i) => {
                            if ("emotion" in eachImage) {
                                return (
                                    <text style={{textTransform: 'capitalize'}}>
                                        Detect emotion: {eachImage.emotion}
                                    </text>
                                )
                            }
                        })
                    }
                </div>
                {
                    this.state.resImg &&
                    this.state.resImg.map((eachImage, i) => {
                        if ("image_url" in eachImage) {
                            return (
                                <Image className="output-img"
                                        width={380}
                                        height={230}
                                        rounded
                                        src={eachImage.image_url} alt="image" key={i}/>
                            )
                        }
                    })
                }
            </div>
        );
    }
}
    
export default EmotionCap;
