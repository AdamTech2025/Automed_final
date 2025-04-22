import React, { createContext, useState, useContext, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null); // Store user details { name, email }
  const navigate = useNavigate();

  // Check local storage on initial load
  useEffect(() => {
    const token = localStorage.getItem('accessToken');
    const storedUser = localStorage.getItem('user');
    if (token && storedUser) {
      try {
        const parsedUser = JSON.parse(storedUser);
        setIsAuthenticated(true);
        setUser(parsedUser);
      } catch (error) {
        console.error("Failed to parse user from localStorage", error);
        // Clear invalid storage if parsing fails
        localStorage.removeItem('accessToken');
        localStorage.removeItem('user');
      }
    }
  }, []);

  const login = (userData) => {
    // Assumes userData contains { name, email, access_token, ... }
    // We already stored token and user in services.js, just update state here
     const token = localStorage.getItem('accessToken'); // Re-read token just in case
     const storedUser = localStorage.getItem('user');
     if (token && storedUser) {
         try {
             const parsedUser = JSON.parse(storedUser);
             setIsAuthenticated(true);
             setUser(parsedUser);
             // Optionally navigate after login, e.g., to dashboard
             // navigate('/'); 
         } catch(error) {
             console.error("Error processing login data", error);
             logout(); // Log out if data is bad
         }
     } else {
         console.error("Login called but token or user not found in localStorage");
     }
  };

  const logout = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('user');
    setIsAuthenticated(false);
    setUser(null);
    // Navigate to login or home page after logout
    navigate('/login'); 
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

// Custom hook to use the auth context
export const useAuth = () => {
  return useContext(AuthContext);
}; 