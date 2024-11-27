import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './StudentForm.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const StudentForm = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [major, setMajor] = useState('');
  const [status, setStatus] = useState('active');
  const [message, setMessage] = useState('');
  const [students, setStudents] = useState([]);
  const [password, setPassword] = useState('');

  useEffect(() => {
    const fetchStudents = async () => {
      try {
        const response = await axios.get(`${API_URL}/api/v1/students`);
        setStudents(response.data);
      } catch (error) {
        setMessage('Error al cargar los estudiantes.');
      }
    };

    fetchStudents();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API_URL}/api/v1/students`, {
        name,
        role: 'student',
        email,
        password,
        status: 'active',
        major,
      });
      setMessage('Estudiante creado exitosamente.');
      const response = await axios.get(`${API_URL}/api/v1/students`);
      setStudents(response.data);
    } catch (error) {
      setMessage('Error al crear el estudiante.');
    }
  };

  const handleDelete = async (studentId) => {
    try {
      await axios.delete(`${API_URL}/api/v1/students/${studentId}`);
      setMessage('Estudiante eliminado exitosamente.');
      setStudents(students.filter((student) => student.id !== studentId));
    } catch (error) {
      setMessage('Error al eliminar el estudiante.');
    }
  };

  return (
    <div className="wrapper">
      <h2>Formulario de Estudiante</h2>
      <form onSubmit={handleSubmit}>
        <div className="input-box">
          <label>Nombre</label>
          <input
            type="text"
            placeholder="Ingresa el nombre"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </div>
        <div className="input-box">
          <label>Email</label>
          <input
            type="email"
            placeholder="Ingresa el email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div className="input-box">
          <label>Password</label>
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <div className="input-box">
          <label>Carrera</label>
          <input
            type="text"
            placeholder="Ingresa la carrera"
            value={major}
            onChange={(e) => setMajor(e.target.value)}
            required
          />
        </div>
        <button type="submit">Crear Estudiante</button>
      </form>
      {message && <p className="message">{message}</p>}

      <h3>Estudiantes Activos</h3>
      <ul>
        {students.map((student) => (
          <li key={student.id}>
            {student.name} - {student.email} - {student.major} - {student.status}
            <button onClick={() => handleDelete(student.id)}>Eliminar</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default StudentForm;
