import LoginForm from './Components/LoginForm/LoginForm';
import Home from './Components/Home/Home';
import { useState } from 'react';

function App() {
  const [user, setUser] = useState([])
  return (
    <div className="App">
      {
      !user.length > 0
      ? <LoginForm setUser= {setUser}/>
      : <Home user = {user} setUser = {setUser}/>
      }
    </div>
  );
}

export default App;
