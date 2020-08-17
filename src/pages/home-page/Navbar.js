import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import { Navbar, Nav } from 'react-bootstrap';
import './Navbar.css';

class NavBar extends Component{
    render(){
        return(
            <div id='nav-id'>
                <Navbar collapseOnSelect bg='light' expand='lg'>
                    <Navbar.Brand className="nav-brand">
                        Emoji Search Engine
                    </Navbar.Brand>
                    <Navbar.Toggle aria-controls="responsive-navbar-nav" />
                    <Nav>
                        <Nav.Link className="nav-item" href='/'>
                            Home
                        </Nav.Link>
                        <Nav.Link className="nav-item" href='/webcam'>
                            Explore Emoji
                        </Nav.Link>
                        <Nav.Link className="nav-item" href='about'>
                            About us
                        </Nav.Link>
                    </Nav>
                </Navbar>
            </div>
        );
    }
}
export default NavBar;