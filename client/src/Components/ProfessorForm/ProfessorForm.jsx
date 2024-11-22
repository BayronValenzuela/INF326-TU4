import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './ProfessorForm.css';

const ProfessorForm = () => {
  const [name, setName] = useState('');
  const [role, setRole] = useState('');
  const [email, setEmail] = useState('');
  const [department, setDepartment] = useState('');
  const [message, setMessage] = useState('');
  const [professors, setProfessors] = useState([]);

  // Listar profesores
  useEffect(() => {
    const fetchProfessors = async () => {
      try {
        const response = await axios.get('/api/v1/professors');
        setProfessors(response.data);
      } catch (error) {
        setMessage('Error al cargar los profesores.');
      }
    };

    fetchProfessors();
  }, []);

  // Registrar un nuevo profesor
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('/api/v1/professors', {
        name,
        role,
        email,
        department,
      });
      setMessage('Profesor creado exitosamente.');
      setProfessors([...professors, response.data]); // Agregar el nuevo profesor a la lista
    } catch (error) {
      setMessage('Error al crear el profesor.');
    }
  };

  // Eliminar un profesor
  const handleDelete = async (professorId) => {
    try {
      await axios.delete(`/api/v1/professors/${professorId}`);
      setMessage('Profesor eliminado exitosamente.');
      setProfessors(professors.filter(professor => professor._id !== professorId)); // Eliminar de la lista local
    } catch (error) {
      setMessage('Error al eliminar el profesor.');
    }
  };

  return (
    <div className='main-content'>
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
              type="text"
              placeholder="Rol"
              value={role}
              onChange={(e) => setRole(e.target.value)}
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
            <li key={professor._id} className="professor-item">
              {professor.name} - {professor.email} - {professor.role} - {professor.department}
              <button className="delete-btn" onClick={() => handleDelete(professor._id)}>
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
