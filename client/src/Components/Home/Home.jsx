import React from 'react'
import Navbar from '../Navbar/Navbar'
import AdminForm from '../AdminForm/AdminForm'
import ProfessorForm from '../ProfessorForm/ProfessorForm'
import StudentForm from '../StudentForm/StudentForm'

export default function Home({user, setUser}) {
    return (
        <div>
            <Navbar user={user} setUser={setUser} />
            <ProfessorForm />
            <StudentForm />
            <AdminForm />
        </div>
    )
}