import { useState, useEffect, useRef } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { FaTooth, FaSun, FaMoon, FaPlus, FaUserCircle, FaSignOutAlt, FaUsers, FaBars, FaFileUpload } from 'react-icons/fa';
import { useTheme } from '../../context/ThemeContext';
import { useAuth } from '../../context/AuthContext';
import PropTypes from 'prop-types';

const Navbar = ({ toggleSidebar }) => {
  const { isDark, toggleTheme } = useTheme();
  const { isAuthenticated, user, logout } = useAuth();
  const [showDropdown, setShowDropdown] = useState(false);
  const dropdownRef = useRef(null);
  const navigate = useNavigate();
  const location = useLocation();

  // Log the state received from context
  console.log("Navbar received from useAuth:", { isAuthenticated, user });

  const handleNewAnalysis = () => {
    // If already on dashboard page, reload it to reset state
    if (location.pathname === '/dashboard') {
      // Create a custom event that the Home component can listen for
      const event = new CustomEvent('newAnalysis', { 
        detail: { timestamp: new Date().getTime() } 
      });
      window.dispatchEvent(event);
      
      // Scroll to top to focus on the input
      window.scrollTo(0, 0);
    } else {
      // If on another page, navigate to dashboard
      navigate('/dashboard');
    }
  };

  const handleLogout = () => {
    logout();
    setShowDropdown(false);
  };

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setShowDropdown(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [dropdownRef]);

  const userInitial = user?.name ? user.name[0].toUpperCase() : '?';

  return (
    <nav className="w-full p-4 shadow-md flex flex-col sm:flex-row items-center justify-between bg-[var(--color-bg-card)] dark:bg-[var(--color-bg-secondary)] transition-colors">
      <div className="flex items-center mb-4 sm:mb-0">
        <button 
          onClick={toggleSidebar} 
          className={`${isDark ? 'text-gray-300 hover:text-blue-300' : 'text-gray-700 hover:text-blue-700'} mr-4 p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500`} 
          aria-label="Toggle sidebar"
        >
          <FaBars className="text-xl" />
        </button>
        <FaTooth className={`${isDark ? 'text-blue-400' : 'text-blue-600'} text-2xl md:text-3xl mr-2`} />
      </div>
      
      <div className="flex items-center flex-wrap gap-2 space-x-4">
        <button
          onClick={handleNewAnalysis}
          className={`${isDark ? 'text-gray-300 hover:text-blue-300' : 'text-gray-600 hover:text-blue-700'} 
            flex items-center transition-colors p-2 rounded-md`}
          aria-label="New Analysis"
          title="Start a new analysis"
        >
          <FaPlus className="text-lg" />
          <span className="ml-1 hidden sm:inline">New Analysis</span>
        </button>
        <Link 
          to="/extractor" 
          className={`${isDark ? 'text-gray-300 hover:text-blue-300' : 'text-gray-600 hover:text-blue-700'} 
            flex items-center transition-colors p-2 rounded-md`}
          aria-label="Extractor"
          title="Extract from files"
        >
          <FaFileUpload className="text-lg" />
          <span className="ml-1 hidden sm:inline">Extractor</span>
        </Link>
        {/* <Link 
          to="/questions" 
          className={`${isDark ? 'text-gray-300 hover:text-blue-300' : 'text-gray-700 hover:text-blue-700'} 
            flex items-center transition-colors p-2 rounded-md text-sm sm:text-base`}
        >
          <FaQuestion className="mr-1" />
          <span>Questions</span>
        </Link> */}
        <button 
          onClick={toggleTheme}
          className="theme-toggle p-2 rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          aria-label="Toggle dark/light mode"
        >
          {isDark ? (
            <FaSun className="text-yellow-300 text-xl hover:text-yellow-200 transition-colors" />
          ) : (
            <FaMoon className="text-gray-600 text-xl hover:text-gray-800 transition-colors" />
          )}
        </button>

        {isAuthenticated && user ? (
          <>
          {/* Conditionally render Admin Dashboard link */} 
          {user.role === 'admin' && (
             <Link 
                to="/admin/dashboard"
                className={`${isDark ? 'text-gray-300 hover:text-purple-300' : 'text-gray-600 hover:text-purple-700'} 
                           flex items-center transition-colors p-2 rounded-md text-sm sm:text-base`}
                title="Admin Dashboard"
              >
                <FaUsers className="mr-1" />
                <span className="hidden sm:inline">Admin</span>
             </Link>
          )}

          <div className="relative" ref={dropdownRef}>
            <button 
              onClick={() => setShowDropdown(!showDropdown)}
              className={`flex items-center justify-center w-8 h-8 rounded-full 
                        ${isDark ? 'bg-blue-600 hover:bg-blue-500' : 'bg-blue-500 hover:bg-blue-600'} 
                        text-white font-semibold text-sm cursor-pointer focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500`}
              aria-label="User menu"
            >
              {userInitial}
            </button>
            {showDropdown && (
              <div 
                className={`absolute right-0 mt-2 w-48 bg-[var(--color-bg-card)] dark:bg-[var(--color-bg-secondary)] rounded-md shadow-lg py-1 z-50 border border-[var(--color-border)] dark:border-slate-600`}
              >
                <div className={`px-4 py-2 text-sm text-[var(--color-text-secondary)] border-b border-[var(--color-border)] dark:border-slate-600`}>
                  <p className="font-medium truncate text-[var(--color-text-primary)]">{user.name}</p>
                  <p className="text-xs truncate">{user.email}</p>
                </div>
                <button
                  onClick={handleLogout}
                  className={`w-full text-left px-4 py-2 text-sm ${isDark ? 'text-red-400 hover:bg-red-500 hover:text-white' : 'text-red-600 hover:bg-red-100'} flex items-center transition-colors`}
                >
                  <FaSignOutAlt className="mr-2" />
                  Logout
                </button>
              </div>
            )}
          </div>
          </>
        ) : (
          <Link 
            to="/"
            className={`${isDark ? 'text-gray-300 hover:text-blue-300' : 'text-gray-700 hover:text-blue-700'} 
            flex items-center transition-colors p-2 rounded-md text-sm sm:text-base`}
          >
             <FaUserCircle className="mr-1" />
            Login
          </Link>
        )}
      </div>
    </nav>
  );
};

// Add prop type validation
Navbar.propTypes = {
  toggleSidebar: PropTypes.func.isRequired,
};

export default Navbar;