import React, { useState } from 'react';
import './LoginForm.css';
import { FaUser, FaLock } from "react-icons/fa";

export function LoginForm({ setUser, setIsRegistering }) {
  const [name, setName] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (name === '' || password === '') {
      setError(true);
      return;
    }
    setError(false);
    setUser([name]);
  };

  return (
    <div className="wrapper">
      <form action="" onSubmit={handleSubmit}>
        <h1>Login SIGA</h1>
        {error && <p className="error">All fields are required</p>}
        <div className="input-box">
          <input
            type="email"
            value={name}
            onChange={e => setName(e.target.value)}
            placeholder="Username"
            required
          />
          <FaUser className="icon" />
        </div>
        <div className="input-box">
          <input
            type="password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            placeholder="Password"
            required
          />
          <FaLock className="icon" />
        </div>
        <div className="remember-forgot">
          <label><input type="checkbox" />Remember me</label>
          <a href="#">Forgot Password?</a>  
        </div>
        <button type="submit">Login</button>
        <div className="register-link">
          <p>Don't have an account? <a href="#" onClick={() => setIsRegistering(true)}>Register</a></p>
        </div>
      </form>
    </div>
  );
}

export default LoginForm;
