import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getAllUsersActivity } from '../../interceptors/services';
import { useTheme } from '../../context/ThemeContext';
import { FaUsers, FaEnvelope, FaPhone, FaCalendarAlt, FaCheckCircle, FaTimesCircle, FaChartBar } from 'react-icons/fa';

const AdminDashboard = () => {
  const [usersData, setUsersData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const { isDark } = useTheme();
  const navigate = useNavigate();

  useEffect(() => {
    const controller = new AbortController();
    const fetchData = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const response = await getAllUsersActivity(controller.signal);
        setUsersData(response.users || []);
      } catch (err) {
        if (err.name !== 'AbortError') {
          console.error("Failed to fetch admin data:", err);
          setError(err.detail || err.message || 'Failed to load user data. You may not have permission.');
        }
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();

    // Cleanup function to abort fetch if component unmounts
    return () => {
      controller.abort();
    };
  }, []);

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    try {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric', month: 'short', day: 'numeric',
      });
    } catch (e) {
      return 'Invalid Date';
    }
  };

  return (
    <div className={`min-h-screen p-4 sm:p-8 transition-colors duration-300 ${isDark ? 'bg-gray-900 text-gray-200' : 'bg-gray-100 text-gray-800'}`}>
      <h1 className="text-2xl sm:text-3xl font-bold mb-6 flex items-center">
        <FaUsers className="mr-3" /> Admin Dashboard - User Activity
      </h1>

      {isLoading && (
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-blue-500"></div>
        </div>
      )}

      {error && (
        <div className={`p-4 rounded-md ${isDark ? 'bg-red-800 bg-opacity-50 text-red-200' : 'bg-red-100 text-red-700'}`}>
          <p className="font-semibold">Error:</p>
          <p>{error}</p>
        </div>
      )}

      {!isLoading && !error && (
        <div className="overflow-x-auto shadow-lg rounded-lg">
          <table className={`w-full min-w-[600px] text-sm text-left ${isDark ? 'divide-gray-700' : 'divide-gray-200'}`}>
            <thead className={`${isDark ? 'bg-gray-700 text-gray-300' : 'bg-gray-200 text-gray-600'} uppercase tracking-wider`}>
              <tr>
                <th scope="col" className="px-4 py-3 font-medium">Name</th>
                <th scope="col" className="px-4 py-3 whitespace-nowrap">
                   <div className="flex items-center">
                    <FaEnvelope className={`mr-1.5 ${isDark ? 'text-gray-400' : 'text-gray-500'}`}/>
                    <span className="font-medium">Email</span>
                   </div>
                </th>
                <th scope="col" className="px-4 py-3 whitespace-nowrap">
                   <div className="flex items-center">
                    <FaPhone className={`mr-1.5 ${isDark ? 'text-gray-400' : 'text-gray-500'}`}/>
                    <span className="font-medium">Phone</span>
                   </div>
                </th>
                <th scope="col" className="px-4 py-3 whitespace-nowrap">
                   <div className="flex items-center">
                    <FaCalendarAlt className={`mr-1.5 ${isDark ? 'text-gray-400' : 'text-gray-500'}`}/>
                    <span className="font-medium">Created</span>
                   </div>
                </th>
                <th scope="col" className="px-4 py-3 text-right font-medium">Verified</th>
                <th scope="col" className="px-4 py-3 text-right whitespace-nowrap">
                   <div className="flex items-center justify-end">
                    <FaChartBar className={`mr-1.5 ${isDark ? 'text-gray-400' : 'text-gray-500'}`}/>
                    <span className="font-medium">Analyses</span>
                   </div>
                </th>
                <th scope="col" className="px-4 py-3 text-right font-medium">Role</th>
              </tr>
            </thead>
            <tbody className={`${isDark ? 'bg-gray-800 divide-gray-700' : 'bg-white divide-gray-200'}`}>
              {usersData.length > 0 ? (
                usersData.map((user) => (
                  <tr 
                    key={user.id} 
                    className={`${isDark ? 'hover:bg-gray-700' : 'hover:bg-gray-50'} transition-colors cursor-pointer`}
                    onClick={() => navigate(`/user/${user.id}/activity`)}
                  >
                    <td className="px-4 py-3 font-medium whitespace-nowrap">{user.name}</td>
                    <td className="px-4 py-3 whitespace-nowrap">{user.email}</td>
                    <td className="px-4 py-3 whitespace-nowrap">{user.phone || 'N/A'}</td>
                    <td className="px-4 py-3 whitespace-nowrap">{formatDate(user.created_at)}</td>
                    <td className="px-4 py-3 text-right">
                      {user.is_email_verified ? (
                        <FaCheckCircle className="text-green-500 inline-block text-lg" title="Verified" />
                      ) : (
                        <FaTimesCircle className="text-red-500 inline-block text-lg" title="Not Verified" />
                      )}
                    </td>
                    <td className="px-4 py-3 text-right font-semibold">{user.analysis_count}</td>
                    <td className="px-4 py-3 text-right">
                      <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${
                        user.role === 'admin'
                        ? (isDark ? 'bg-purple-600 text-purple-100' : 'bg-purple-200 text-purple-800')
                        : (isDark ? 'bg-blue-600 text-blue-100' : 'bg-blue-200 text-blue-800')
                      }`}>
                        {user.role}
                      </span>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="7" className="text-center py-4 px-4">No user data found.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default AdminDashboard;