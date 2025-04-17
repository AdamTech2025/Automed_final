import { Link } from 'react-router-dom';
import { FaTooth, FaSun, FaMoon, FaQuestion } from 'react-icons/fa';
import { useTheme } from '../../context/ThemeContext';

const Navbar = () => {
  const { isDark, toggleTheme } = useTheme();

  return (
    <nav className="w-full p-4 shadow-md flex flex-col sm:flex-row items-center justify-between transition-colors">
      <div className="flex items-center mb-4 sm:mb-0">
        <FaTooth className={`${isDark ? 'text-blue-400' : 'text-blue-600'} text-2xl md:text-3xl mr-2`} />
        <Link to="/" className={`${isDark ? 'text-blue-400' : 'text-blue-600'} font-bold text-lg md:text-xl`}>
          Dental Code Extractor Pro
        </Link>
      </div>
      
      <div className="flex items-center space-x-4">
        <Link 
          to="/questions" 
          className={`${isDark ? 'text-blue-400 hover:text-blue-300' : 'text-blue-600 hover:text-blue-700'} 
            flex items-center transition-colors`}
        >
          <FaQuestion className="mr-1" />
          <span>Questions</span>
        </Link>
        <button 
          onClick={toggleTheme}
          className="theme-toggle p-2 rounded-full focus:outline-none"
          aria-label="Toggle dark/light mode"
        >
          {isDark ? (
            <FaSun className="text-yellow-300 text-xl hover:text-yellow-200 transition-colors" />
          ) : (
            <FaMoon className="text-gray-600 text-xl hover:text-gray-800 transition-colors" />
          )}
        </button>
      </div>
    </nav>
  );
};

export default Navbar;