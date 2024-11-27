import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './ProfessorForm.css';

// Configuración de la URL base desde una variable de entorno
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const ProfessorForm = () => {
  const [name, setName] = useState('');
  const [role, setRole] = useState('');
  const [email, setEmail] = useState('');
  const [department, setDepartment] = useState('');
  const [message, setMessage] = useState('');
  const [password, setPassword] = useState('pwd');
  const [status, setStatus] = useState('active');
  const [id, setId] = useState(Math.floor(Math.random() * 100000))
  const [professors, setProfessors] = useState([]);

  // Listar profesores
  useEffect(() => {
    const fetchProfessors = async () => {
      try {
        const response = await axios.get(`${API_URL}/api/v1/professors`); // URL actualizada
        console.log('profe:', response.data);
        setProfessors(response.data);
      } catch (error) {
        console.error('Error fetching professors:', error);
        setMessage('Error al cargar los profesores.');
      }
    };

    fetchProfessors();
  }, []);

  // Registrar un nuevo profesor
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(`${API_URL}/api/v1/professors`, {
        id,
        name,
        role: "professor",
        email,
        password,
        status: "active",
        department,
      });
      setMessage('Profesor creado exitosamente.');
      setProfessors([...professors, response.data]); // Agregar el nuevo profesor a la lista
      setName('');
      setRole('');
      setEmail('');
      setDepartment('');
    } catch (error) {
      console.error('Error creating professor:', error);
      setMessage('Error al crear el profesor.');
    }
  };

  // Eliminar un profesor
  const handleDelete = async (professorId) => {
    try {
      await axios.delete(`${API_URL}/api/v1/professors/${professorId}`);
      setMessage('Profesor eliminado exitosamente.');
      setProfessors(professors.filter((professor) => professor.id !== professorId)); // Eliminar de la lista local
    } catch (error) {
      console.error('Error deleting professor:', error);
      setMessage('Error al eliminar el profesor.');
    }
  };

  return (
    <div className="main-content">
      <div className="wrapper">
        <h1>Formulario de Profesor</h1>
        <form onSubmit={handleSubmit}>
          <div className="input-box">
            <input
              type="text"
              placeholder="Nombre"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />
          </div>
          <div className="input-box">
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="input-box">
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <div className="input-box">
            <input
              type="text"
              placeholder="Departamento"
              value={department}
              onChange={(e) => setDepartment(e.target.value)}
              required
            />
          </div>
          <button type="submit">Crear Profesor</button>
        </form>
        {message && <p className="message">{message}</p>}

        <h3>Profesores Activos</h3>
        <ul>
          {professors.map((professor) => (
            <li key={professor.id} className="professor-item">
              {professor.name} - {professor.email} - {professor.role} - {professor.department}
              <button className="delete-btn" onClick={() => handleDelete(professor.id)}>
                Eliminar
              </button>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default ProfessorForm;
