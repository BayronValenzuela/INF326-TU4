import React from "react";
import './Navbar.css';
import usmLogo from '../../img/USM.svg';


export default function Navbar({ user, setUser }) {
    return (
        <header className="header">
            <img src={usmLogo} alt="USM Logo" className="logo"></img>
            <nav className="navbar">
                <button onClick={() => setUser([])}>Cerrar Sesión</button>
                <br />
                <a>Bienvenid@: {user}</a>
            </nav>
        </header>
    );
}