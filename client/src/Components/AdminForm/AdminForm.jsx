import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './AdminForm.css';

const AdminForm = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [role, setRole] = useState('');
  const [message, setMessage] = useState('');
  const [admins, setAdmins] = useState([]);
  
  // Listar administradores
  useEffect(() => {
    const fetchAdmins = async () => {
      try {
        const response = await axios.get('/api/v1/admins');
        setAdmins(response.data);
      } catch (error) {
        setMessage('Error al cargar los administradores.');
      }
    };
    
    fetchAdmins();
  }, []);

  // Registrar un nuevo administrador
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await axios.post('/api/v1/admins', {
        name,
        email,
        role,
      });
      setMessage('Administrador creado exitosamente.');
    } catch (error) {
      setMessage('Error al crear el administrador.');
    }
  };

  // Eliminar un administrador
  const handleDelete = async (adminId: string) => {
    try {
      await axios.delete(`/api/v1/admins/${adminId}`);
      setMessage('Administrador eliminado exitosamente.');
      setAdmins(admins.filter(admin => admin._id !== adminId)); // Eliminar de la lista local
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
            type="text" 
            placeholder='Rol'
            value={role} 
            onChange={(e) => setRole(e.target.value)} 
            required 
          />
        </div>
        <button type="submit">Crear Administrador</button>
      </form>
      {message && <p className='message'>{message}</p>}
      
      <h3>Administradores Activos</h3>
      <ul>
        {admins.map(admin => (
          <li key={admin._id}>
            {admin.name} - {admin.email} - {admin.role}
            <button onClick={() => handleDelete(admin._id)}>Eliminar</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default AdminForm;
