import React, { useState } from 'react';
import './RegisterForm.css';
import { FaUser, FaLock, FaEnvelope } from "react-icons/fa";

export function RegisterForm({ setUser, setIsRegistering }) {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (name === '' || email === '' || password === '' || confirmPassword === '') {
      setError('All fields are required');
      return;
    }
    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }
    setError(false);
    setUser([name]); // You can handle this differently based on your backend logic
  };

  return (
    <div className="wrapper">
      <form action="" onSubmit={handleSubmit}>
        <h1>Register SIGA</h1>
        {error && <p className="error">{error}</p>}
        <div className="input-box">
          <input
            type="text"
            value={name}
            onChange={e => setName(e.target.value)}
            placeholder="Full Name"
            required
          />
          <FaUser className="icon" />
        </div>
        <div className="input-box">
          <input
            type="email"
            value={email}
            onChange={e => setEmail(e.target.value)}
            placeholder="Email"
            required
          />
          <FaEnvelope className="icon" />
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
        <div className="input-box">
          <input
            type="password"
            value={confirmPassword}
            onChange={e => setConfirmPassword(e.target.value)}
            placeholder="Confirm Password"
            required
          />
          <FaLock className="icon" />
        </div>
        <button type="submit">Register</button>
        <div className="register-link">
          <p>Already have an account? <a href="#" onClick={() => setIsRegistering(false)}>Login</a></p>
        </div>
      </form>
    </div>
  );
}

export default RegisterForm;
