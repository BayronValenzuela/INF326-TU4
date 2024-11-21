import React, { useState, useEffect } from 'react';
import axios from 'axios';

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
    <div>
      <h2>Formulario de Profesor</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Nombre</label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Rol</label>
          <input
            type="text"
            value={role}
            onChange={(e) => setRole(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Email</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Departamento</label>
          <input
            type="text"
            value={department}
            onChange={(e) => setDepartment(e.target.value)}
            required
          />
        </div>
        <button type="submit">Crear Profesor</button>
      </form>
      {message && <p>{message}</p>}

      <h3>Profesores Activos</h3>
      <ul>
        {professors.map((professor) => (
          <li key={professor._id}>
            {professor.name} - {professor.email} - {professor.role} - {professor.department}
            <button onClick={() => handleDelete(professor._id)}>Eliminar</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ProfessorForm;
