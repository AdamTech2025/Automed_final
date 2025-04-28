import { NavLink } from 'react-router-dom'; // Use NavLink for active styling
import PropTypes from 'prop-types';
import { useTheme } from '../../context/ThemeContext';
import { FaTimes, FaHome, FaUserInjured, FaFileAlt, FaDollarSign, FaSun, FaMoon } from 'react-icons/fa';

const Sidebar = ({ isVisible, toggleSidebar }) => {
  const { isDark, toggleTheme } = useTheme();

  // Define active link style
  const activeClassName = isDark ? 'bg-slate-700 text-white' : 'bg-blue-100 text-blue-700';
  const inactiveClassName = isDark ? 'text-gray-300 hover:bg-slate-700 hover:text-white' : 'text-gray-600 hover:bg-blue-100 hover:text-blue-700';

  return (
    // Overlay for closing sidebar when clicking outside (optional but professional)
    <>
      {isVisible && (
        <div 
          onClick={toggleSidebar} 
          className="fixed inset-0 bg-black bg-opacity-30 z-20 lg:hidden"
          aria-hidden="true"
        ></div>
      )}

      <div
        // Use --color-bg-secondary directly for background (adapts to theme)
        className={`fixed inset-y-0 left-0 z-30 w-64 bg-[var(--color-bg-secondary)] text-gray-800 dark:text-gray-200 
                  transform ${isVisible ? 'translate-x-0' : '-translate-x-full'} 
                  transition-transform duration-300 ease-in-out shadow-xl overflow-y-auto`}
      >
        <div className="flex flex-col h-full">
          {/* Header with Close Button - Use --color-bg-secondary directly for sticky header */}
          <div className={`flex items-center justify-between p-4 border-b border-[var(--color-border)] dark:border-slate-600 sticky top-0 bg-[var(--color-bg-secondary)] z-10`}>
            <h1 className={`text-lg font-semibold tracking-tight text-[var(--color-primary)] dark:text-blue-300`}>Menu</h1>
            <button 
              onClick={toggleSidebar} 
              className={`${isDark ? 'text-gray-400 hover:text-white' : 'text-gray-600 hover:text-gray-900'} p-1 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500`}
              aria-label="Close sidebar"
            >
              <FaTimes />
            </button>
          </div>

          {/* Navigation - Adjusted padding, font */}
          <nav className="flex-1 px-3 py-4 ">
            <ul className="space-y-2">
              <li>
                <NavLink 
                  to="/dashboard" 
                  onClick={toggleSidebar} // Close sidebar on link click
                  className={({ isActive }) => 
                    `flex items-center px-3 py-2.5 rounded-md text-sm font-medium transition-colors ${isActive ? activeClassName : inactiveClassName}`
                  }
                >
                  <FaHome className="mr-3 h-5 w-5" /> Dashboard
                </NavLink>
              </li>
              <li>
                <NavLink 
                  to="/patients" // Assuming a future route
                  onClick={toggleSidebar}
                  className={({ isActive }) => 
                    `flex items-center px-3 py-2.5 rounded-md text-sm font-medium transition-colors ${isActive ? activeClassName : inactiveClassName}`
                  }
                >
                  <FaUserInjured className="mr-3 h-5 w-5" /> Patients
                </NavLink>
              </li>
              <li>
                <NavLink 
                  to="/coding" // Assuming a future route
                  onClick={toggleSidebar}
                  className={({ isActive }) => 
                    `flex items-center px-3 py-2.5 rounded-md text-sm font-medium transition-colors ${isActive ? activeClassName : inactiveClassName}`
                  }
                >
                  <FaFileAlt className="mr-3 h-5 w-5" /> Coding
                </NavLink>
              </li>
              <li>
                <NavLink 
                  to="/billing" // Assuming a future route
                  onClick={toggleSidebar}
                   className={({ isActive }) => 
                    `flex items-center px-3 py-2.5 rounded-md text-sm font-medium transition-colors ${isActive ? activeClassName : inactiveClassName}`
                  }
                >
                  <FaDollarSign className="mr-3 h-5 w-5" /> Billing
                </NavLink>
              </li>
              {/* Add other links as needed */}
            </ul>
          </nav>

          {/* Theme Toggle - Sticky at bottom - Use --color-bg-secondary directly for sticky footer */}
          <div className={`p-3 mt-auto border-t border-[var(--color-border)] dark:border-slate-600 sticky bottom-0 bg-[var(--color-bg-secondary)]`}>
            <button 
              onClick={toggleTheme}
              className={`flex items-center px-3 py-2.5 rounded-md text-sm font-medium w-full transition-colors ${inactiveClassName}`}
            >
              {isDark ? <FaSun className="mr-3 h-5 w-5" /> : <FaMoon className="mr-3 h-5 w-5" />}
              {isDark ? 'Light Mode' : 'Dark Mode'}
            </button>
          </div>
        </div>
      </div>
    </>
  );
};

Sidebar.propTypes = {
  isVisible: PropTypes.bool.isRequired,
  toggleSidebar: PropTypes.func.isRequired,
};

export default Sidebar;
