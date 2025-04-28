import { createContext, useState, useContext, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import PropTypes from 'prop-types';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null); // Store user details { name, email }
  const navigate = useNavigate();

  // Check local storage on initial load
  useEffect(() => {
    const checkAuth = () => {
      const token = localStorage.getItem('accessToken');
      const storedUser = localStorage.getItem('user');
      
      if (token && storedUser) {
        try {
          const parsedUser = JSON.parse(storedUser);
          setIsAuthenticated(true);
          setUser(parsedUser);
          console.log("Auth restored from localStorage:", { user: parsedUser });
        } catch (error) {
          console.error("Failed to parse user from localStorage", error);
          // Clear invalid storage if parsing fails
          localStorage.removeItem('accessToken');
          localStorage.removeItem('user');
          setIsAuthenticated(false);
          setUser(null);
        }
      } else {
        // Ensure state is synced if no valid data in localStorage
        setIsAuthenticated(false);
        setUser(null);
      }
    };
    
    checkAuth();
    
    // Listen for storage events (if user logs in/out in another tab)
    window.addEventListener('storage', checkAuth);
    return () => window.removeEventListener('storage', checkAuth);
  }, []);

  // This function can either:
  // 1. Be called after services.js has already set localStorage (normal case)
  // 2. Be called with userData and token to set localStorage itself (alternative usage)
  const login = (userData = null, token = null) => {
    console.log("AuthContext: login function called", { providedData: userData, providedToken: !!token });
    
    // If user data and token were passed directly, store them in localStorage
    if (userData && token) {
      localStorage.setItem('accessToken', token);
      // Ensure userData includes name, email, and role
      const userToStore = { 
        name: userData.name, 
        email: userData.email,
        role: userData.role // Extract role
      };
      localStorage.setItem('user', JSON.stringify(userToStore));
      console.log("AuthContext: Stored in localStorage:", { token, userToStore });
    }
    
    // Read from localStorage (either what was just set or what was set by services.js)
    const accessToken = localStorage.getItem('accessToken');
    const storedUser = localStorage.getItem('user');
    console.log("AuthContext: Read from localStorage:", { accessToken, storedUser });

    if (accessToken && storedUser) {
      try {
        const parsedUser = JSON.parse(storedUser);
        console.log("AuthContext: Parsed user:", parsedUser);
        
        // Ensure user state includes the role
        const userWithRole = { 
          name: parsedUser.name, 
          email: parsedUser.email, 
          role: parsedUser.role // Ensure role is included
        };

        // Update state
        setIsAuthenticated(true);
        setUser(userWithRole);
        
        console.log("AuthContext: State updated:", { isAuthenticated: true, user: userWithRole });
        
        // Navigate to dashboard after successful login state update
        navigate('/dashboard');
      } catch(error) {
        console.error("Error processing login data", error);
        logout(); // Log out if data is bad
      }
    } else {
      console.error("Login called but token or user not found in localStorage");
      // Optional: Could set an error state here if needed
    }
  };

  const logout = () => {
    console.log("AuthContext: logout function called");
    localStorage.removeItem('accessToken');
    localStorage.removeItem('user');
    setIsAuthenticated(false);
    setUser(null);
    // Navigate to login page (root path) after logout
    navigate('/'); 
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

// Add prop validation
AuthProvider.propTypes = {
  children: PropTypes.node.isRequired,
};

// Custom hook to use the auth context
export const useAuth = () => {
  return useContext(AuthContext);
}; 