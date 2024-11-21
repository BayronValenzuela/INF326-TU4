import React from 'react'
import Navbar from '../Navbar/Navbar'

export default function Home({user, setUser}) {
    return (
        <div>
            <Navbar user={user} setUser={setUser} />
        
        </div>
    )
}