import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './AdminForm.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000'

const AdminForm = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [role, setRole] = useState('');
  const [message, setMessage] = useState('');
  const [password, setPassword] = useState('');
  const [admins, setAdmins] = useState([]);


  // Listar administradores
  useEffect(() => {
    const fetchAdmins = async () => {
      try {
        const response = await axios.get(`${API_URL}/api/v1/admins`);
        setAdmins(response.data);
      } catch (error) {
        setMessage('Error al cargar los administradores.');
      }
    };

    fetchAdmins();
  }, []);

  // Registrar un nuevo administrador
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(`${API_URL}/api/v1/admins`, {
        name,
        role: 'administrator',
        email,
        password,
        status: 'active',
      });
      setMessage('Administrador creado exitosamente.');
    } catch (error) {
      setMessage('Error al crear el administrador.');
    }
  };

  // Eliminar un administrador
  const handleDelete = async (adminId) => {
    console.log('Admin ID:', adminId);
    if (!adminId) {
      setMessage('Error: Admin ID is undefined.');
      return;
    }

    try {
      await axios.delete(`${API_URL}/api/v1/admins/${adminId}`);
      setMessage('Administrador eliminado exitosamente.');
      setAdmins(admins.filter(admin => admin.id !== adminId)); // Eliminar de la lista local
    } catch (error) {
      setMessage('Error al eliminar el administrador.');
    }
  };

  return (
    <div className='wrapper'>
      <h2>Formulario de Administrador</h2>
      <form onSubmit={handleSubmit}>
        <div className='input-box'>
          <input
            type="text"
            placeholder='Nombre'
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </div>
        <div className='input-box'>
          <input
            type="email"
            placeholder='Email'
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div className='input-box'>
          <input
            type="password"
            placeholder='password'
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">Crear Administrador</button>
      </form>
      {message && <p className='message'>{message}</p>}

      <h3>Administradores Activos</h3>
      <ul>
        {admins.map(admin => (
          <li key={admin.id}>
            {admin.name} - {admin.email} - {admin.role}
            <button onClick={() => handleDelete(admin.id)}>Eliminar</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default AdminForm;
