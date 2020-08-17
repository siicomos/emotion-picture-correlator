import React, { Component } from 'react';

class About extends Component {
    render(){
        return (
            <div id='about-us-id'>
                <h2 className="about-h2" class='text-center'>Motivation</h2>
                <p class='text-center'> We are using the real-time facial images from user to detect the emotions.
                According to the emotions, generate the corresponding .gif images.</p>
                <h2 class='text-center'>Algorithm</h2>
                <p class='text-center'></p>
                <h2 className="about-h2" class='text-center'>Team Members</h2>
                <p class='text-center'>Kang Ling</p>
                <p class='text-center'>Mingjun Lee</p>
                <p class='text-center'>Yiwei Ma</p>
            </div>
        );
    } 
}

export default About;
