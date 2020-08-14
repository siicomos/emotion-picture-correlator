import React, { Component } from 'react';
import Image from 'react-bootstrap/Image';

class TestImage extends Component{
    render(){
        return (
            <div>
                <Image 
                    src = {require('./images/test.png')}
                />
            </div>
        );
    }

}
    
export default TestImage;