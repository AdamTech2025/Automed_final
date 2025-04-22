import { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import { FaTooth, FaSun, FaMoon, FaQuestion, FaPlus, FaUserCircle, FaSignOutAlt } from 'react-icons/fa';
import { useTheme } from '../../context/ThemeContext';
import { useAuth } from '../../context/AuthContext';

const Navbar = () => {
  const { isDark, toggleTheme } = useTheme();
  const { isAuthenticated, user, logout } = useAuth();
  const [showDropdown, setShowDropdown] = useState(false);
  const dropdownRef = useRef(null);

  // Log the state received from context
  console.log("Navbar received from useAuth:", { isAuthenticated, user });

  const openNewTab = () => {
    window.open(window.location.href, '_blank');
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
    <nav className="w-full p-4 shadow-md flex flex-col sm:flex-row items-center justify-between transition-colors">
      <div className="flex items-center mb-4 sm:mb-0">
        <FaTooth className={`${isDark ? 'text-blue-400' : 'text-blue-600'} text-2xl md:text-3xl mr-2`} />
        <Link to="/" className={`${isDark ? 'text-blue-400' : 'text-blue-600'} font-bold text-lg md:text-xl`}>
          Dental Code Extractor Pro
        </Link>
      </div>
      
      <div className="flex items-center space-x-4">
        <button
          onClick={openNewTab}
          className={`${isDark ? 'text-gray-400 hover:text-blue-300' : 'text-gray-600 hover:text-blue-700'} 
            flex items-center transition-colors p-2 rounded-md`}
          aria-label="Open in new tab"
        >
          <FaPlus className="text-lg" />
        </button>
        <Link 
          to="/questions" 
          className={`${isDark ? 'text-gray-300 hover:text-blue-300' : 'text-gray-700 hover:text-blue-700'} 
            flex items-center transition-colors p-2 rounded-md text-sm sm:text-base`}
        >
          <FaQuestion className="mr-1" />
          <span>Questions</span>
        </Link>
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
                className={`absolute right-0 mt-2 w-48 ${isDark ? 'bg-gray-700' : 'bg-white'} rounded-md shadow-lg py-1 z-50`}
              >
                <div className={`px-4 py-2 text-sm ${isDark ? 'text-gray-300' : 'text-gray-700'} border-b ${isDark ? 'border-gray-600' : 'border-gray-200'}`}>
                  <p className="font-medium truncate">{user.name}</p>
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

export default Navbar;