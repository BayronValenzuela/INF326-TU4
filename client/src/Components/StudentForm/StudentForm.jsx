import React, { useState, useEffect } from 'react';
import axios from 'axios';

const StudentForm = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [major, setMajor] = useState('');
  const [status, setStatus] = useState('active');
  const [message, setMessage] = useState('');
  const [students, setStudents] = useState([]);

  // Listar estudiantes
  useEffect(() => {
    const fetchStudents = async () => {
      try {
        const response = await axios.get('/api/v1/students');
        setStudents(response.data);
      } catch (error) {
        setMessage('Error al cargar los estudiantes.');
      }
    };

    fetchStudents();
  }, []);

  // Registrar un nuevo estudiante
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('/api/v1/students', {
        name,
        email,
        major,
        status,
      });
      setMessage('Estudiante creado exitosamente.');
      setStudents([...students, response.data]);  // Agregar el nuevo estudiante a la lista
    } catch (error) {
      setMessage('Error al crear el estudiante.');
    }
  };

  // Eliminar un estudiante
  const handleDelete = async (studentId) => {
    try {
      await axios.delete(`/api/v1/students/${studentId}`);
      setMessage('Estudiante eliminado exitosamente.');
      setStudents(students.filter(student => student._id !== studentId));  // Eliminar de la lista local
    } catch (error) {
      setMessage('Error al eliminar el estudiante.');
    }
  };

  return (
    <div>
      <h2>Formulario de Estudiante</h2>
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
          <label>Email</label>
          <input 
            type="email" 
            value={email} 
            onChange={(e) => setEmail(e.target.value)} 
            required 
          />
        </div>
        <div>
          <label>Carrera</label>
          <input 
            type="text" 
            value={major} 
            onChange={(e) => setMajor(e.target.value)} 
            required 
          />
        </div>
        <div>
          <label>Estado</label>
          <select 
            value={status} 
            onChange={(e) => setStatus(e.target.value)}
          >
            <option value="active">Activo</option>
            <option value="inactive">Inactivo</option>
          </select>
        </div>
        <button type="submit">Crear Estudiante</button>
      </form>
      {message && <p>{message}</p>}

      <h3>Estudiantes Activos</h3>
      <ul>
        {students.map(student => (
          <li key={student._id}>
            {student.name} - {student.email} - {student.major} - {student.status}
            <button onClick={() => handleDelete(student._id)}>Eliminar</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default StudentForm;
