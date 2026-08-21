import { useState } from 'react';
import LoginPage from './pages/LoginPage';
import WelcomePage from './pages/WelcomePage';

export default function App() {
  const [token, setToken] = useState(() => sessionStorage.getItem('access_token'));

  const handleLogin = (accessToken) => {
    sessionStorage.setItem('access_token', accessToken);
    setToken(accessToken);
  };

  const handleLogout = () => {
    sessionStorage.removeItem('access_token');
    setToken(null);
  };

  return token ? (
    <WelcomePage onLogout={handleLogout} />
  ) : (
    <LoginPage onLogin={handleLogin} />
  );
}
