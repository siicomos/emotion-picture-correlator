import React, { Component } from 'react';
import Container from 'react-bootstrap/Container';
import Image from 'react-bootstrap/Image';
import { Row, Col } from 'react-bootstrap';
import './Home.css';
import ReactTypingEffect from 'react-typing-effect';

class Home extends Component{
    render(){
        return (
            <body>
                <div className='home-con'>
                    <div>
                        <Image src={require('../../images/3.gif')} 
                                width={380}
                                height={230}
                                rounded className='home-img'/>
                        <Image src={require('../../images/19.gif')} 
                                width={380}
                                height={230}
                                rounded className='home-img'/>
                        <Image src={require('../../images/47.gif')} 
                                width={380}
                                height={230}
                                rounded className='home-img'/>
                    </div>
                    <div>
                        <Image src={require('../../images/6.gif')} 
                                width={380}
                                height={230}
                                rounded className='home-img'/>
                        <Image src={require('../../images/75.gif')} 
                                width={380}
                                height={230}
                                rounded className='home-img'/>
                        <Image src={require('../../images/85.gif')} 
                                width={380}
                                height={230}
                                rounded className='home-img'/>
                    </div>
                    <div>
                        <Image src={require('../../images/68.gif')} 
                                width={380}
                                height={230}
                                rounded className='home-img'/>
                        <Image src={require('../../images/23.gif')} 
                                width={380}
                                height={230}
                                rounded className='home-img'/>
                        <Image src={require('../../images/26.gif')} 
                                width={380}
                                height={230}
                                rounded className='home-img'/>
                    </div>
                </div>
                <div className='home-con'>
                        <ReactTypingEffect
                                text="The world of Emojis and Memes is amazing!"
                        />
                </div>
            </body>
        );
    }

}
    
export default Home;