import LoginForm from './Components/LoginForm/LoginForm';
import RegisterForm from './Components/RegisterForm/RegisterForm';
import Home from './Components/Home/Home';
import { useState } from 'react';

function App() {
  const [user, setUser] = useState([]);
  const [isRegistering, setIsRegistering] = useState(false);

  return (
    <div className="App">
      {
        !user.length > 0 ?
          isRegistering ? 
            <RegisterForm setUser={setUser} setIsRegistering={setIsRegistering} /> :
            <LoginForm setUser={setUser} setIsRegistering={setIsRegistering} /> :
          <Home user={user} setUser={setUser} />
      }
    </div>
  );
}

export default App;
