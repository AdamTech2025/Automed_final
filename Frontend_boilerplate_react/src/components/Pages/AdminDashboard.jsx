import { useState, useEffect } from 'react';
import { getAllUsersActivity, getUserActivity, updateUserRules } from '../../interceptors/services';
import { useTheme } from '../../context/ThemeContext';
import { FaUsers, FaEnvelope, FaPhone, FaCalendarAlt, FaCheckCircle, FaTimesCircle, FaChartBar, FaUserCircle, FaClipboardList, FaTimes, FaEdit, FaSave } from 'react-icons/fa';

const AdminDashboard = () => {
  const [usersData, setUsersData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Add states for selected user
  const [selectedUserId, setSelectedUserId] = useState(null);
  const [selectedUserData, setSelectedUserData] = useState(null);
  const [isLoadingUserData, setIsLoadingUserData] = useState(false);
  const [userDataError, setUserDataError] = useState(null);
  
  // Add states for rules editing
  const [isEditingRules, setIsEditingRules] = useState(false);
  const [userRules, setUserRules] = useState("");
  const [isSavingRules, setIsSavingRules] = useState(false);
  const [rulesSaveError, setRulesSaveError] = useState(null);
  
  const { isDark } = useTheme();

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

  // Add effect to fetch selected user data
  useEffect(() => {
    if (!selectedUserId) return;
    
    const controller = new AbortController();
    const fetchUserData = async () => {
      setIsLoadingUserData(true);
      setUserDataError(null);
      setIsEditingRules(false); // Reset editing state
      try {
        const response = await getUserActivity(selectedUserId, controller.signal);
        setSelectedUserData(response);
        // Initialize rules state if rules exist
        setUserRules(response.user_details.rules || "");
      } catch (err) {
        if (err.name !== 'AbortError') {
          console.error(`Failed to fetch activity for user ${selectedUserId}:`, err);
          setUserDataError(err.detail || err.message || 'Failed to load user activity data.');
        }
      } finally {
        setIsLoadingUserData(false);
      }
    };

    fetchUserData();

    return () => {
      controller.abort();
    };
  }, [selectedUserId]);

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

  const formatDateTime = (dateString) => {
    if (!dateString) return 'N/A';
    try {
      return new Date(dateString).toLocaleString('en-US', {
        year: 'numeric', month: 'short', day: 'numeric',
        hour: 'numeric', minute: '2-digit', hour12: true
      });
    } catch (e) {
      return 'Invalid Date';
    }
  };

  // Handle saving user rules
  const handleSaveRules = async () => {
    if (!selectedUserId) return;
    
    setIsSavingRules(true);
    setRulesSaveError(null);
    
    try {
      await updateUserRules(selectedUserId, userRules);
      // Update the selected user data with new rules
      if (selectedUserData) {
        setSelectedUserData({
          ...selectedUserData,
          user_details: {
            ...selectedUserData.user_details,
            rules: userRules
          }
        });
      }
      setIsEditingRules(false);
    } catch (err) {
      console.error(`Failed to save rules for user ${selectedUserId}:`, err);
      setRulesSaveError(err.detail || err.message || 'Failed to save rules.');
    } finally {
      setIsSavingRules(false);
    }
  };

  // Handle user selection
  const handleUserClick = (userId) => {
    if (selectedUserId === userId) {
      // If clicking the same user, close the details
      setSelectedUserId(null);
      setSelectedUserData(null);
      setUserRules("");
      setIsEditingRules(false);
    } else {
      // Otherwise select the user
      setSelectedUserId(userId);
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
                    className={`${isDark ? 'hover:bg-gray-700' : 'hover:bg-gray-50'} ${selectedUserId === user.id ? (isDark ? 'bg-gray-700' : 'bg-gray-200') : ''} transition-colors cursor-pointer`}
                    onClick={() => handleUserClick(user.id)}
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

      {/* User Activity Details Section */}
      {selectedUserId && (
        <div className={`mt-8 p-6 rounded-lg shadow-lg ${isDark ? 'bg-gray-800' : 'bg-white'}`}>
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold flex items-center">
              <FaUserCircle className="mr-2" /> User Activity Details
            </h2>
            <button 
              onClick={() => {
                setSelectedUserId(null);
                setSelectedUserData(null);
              }}
              className={`p-2 rounded-full hover:bg-opacity-80 ${isDark ? 'hover:bg-gray-700' : 'hover:bg-gray-200'}`}
              aria-label="Close details"
            >
              <FaTimes />
            </button>
          </div>

          {isLoadingUserData && (
            <div className="flex justify-center items-center h-32">
              <div className="animate-spin rounded-full h-12 w-12 border-t-4 border-b-4 border-blue-500"></div>
            </div>
          )}

          {userDataError && (
            <div className={`p-4 rounded-md ${isDark ? 'bg-red-800 bg-opacity-50 text-red-200' : 'bg-red-100 text-red-700'}`}>
              <p className="font-semibold">Error loading user data:</p>
              <p>{userDataError}</p>
            </div>
          )}

          {!isLoadingUserData && !userDataError && selectedUserData && (
            <>
              {/* User Details Card */}
              <div className={`mb-8 p-6 rounded-lg ${isDark ? 'bg-gray-700' : 'bg-gray-50'}`}>
                <h3 className="text-lg font-semibold mb-4 flex items-center"><FaUserCircle className="mr-2" /> User Details</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <p><strong className="font-medium">Name:</strong> {selectedUserData.user_details.name}</p>
                  <p className="flex items-center"><FaEnvelope className="mr-2 opacity-70" /> <strong className="font-medium mr-1">Email:</strong> {selectedUserData.user_details.email}</p>
                  <p className="flex items-center"><FaPhone className="mr-2 opacity-70" /> <strong className="font-medium mr-1">Phone:</strong> {selectedUserData.user_details.phone || 'N/A'}</p>
                  <p className="flex items-center"><FaCalendarAlt className="mr-2 opacity-70" /> <strong className="font-medium mr-1">Joined:</strong> {formatDate(selectedUserData.user_details.created_at)}</p>
                  <p><strong className="font-medium">Role:</strong> 
                    <span className={`ml-2 px-2 py-0.5 rounded-full text-xs font-medium ${
                      selectedUserData.user_details.role === 'admin'
                      ? (isDark ? 'bg-purple-600 text-purple-100' : 'bg-purple-200 text-purple-800')
                      : (isDark ? 'bg-blue-600 text-blue-100' : 'bg-blue-200 text-blue-800')
                    }`}>
                      {selectedUserData.user_details.role}
                    </span>
                  </p>
                  <p><strong className="font-medium">Email Verified:</strong> {selectedUserData.user_details.is_email_verified ? 'Yes' : 'No'}</p>
                </div>

                {/* User Rules Section */}
                <div className="mt-6">
                  <div className="flex justify-between items-center mb-2">
                    <h4 className="text-md font-semibold">User-Specific Rules</h4>
                    {!isEditingRules ? (
                      <button 
                        onClick={() => setIsEditingRules(true)}
                        className={`p-2 rounded-md ${isDark ? 'bg-blue-600 hover:bg-blue-700' : 'bg-blue-500 hover:bg-blue-600'} text-white`}
                      >
                        <FaEdit className="mr-1" /> Edit Rules
                      </button>
                    ) : (
                      <div className="flex space-x-2">
                        <button 
                          onClick={handleSaveRules}
                          disabled={isSavingRules}
                          className={`p-2 rounded-md ${isDark ? 'bg-green-600 hover:bg-green-700' : 'bg-green-500 hover:bg-green-600'} text-white ${isSavingRules ? 'opacity-50 cursor-not-allowed' : ''}`}
                        >
                          <FaSave className="mr-1" /> {isSavingRules ? 'Saving...' : 'Save Rules'}
                        </button>
                        <button 
                          onClick={() => {
                            setIsEditingRules(false);
                            setUserRules(selectedUserData.user_details.rules || "");
                          }}
                          disabled={isSavingRules}
                          className={`p-2 rounded-md ${isDark ? 'bg-gray-600 hover:bg-gray-700' : 'bg-gray-500 hover:bg-gray-600'} text-white ${isSavingRules ? 'opacity-50 cursor-not-allowed' : ''}`}
                        >
                          Cancel
                        </button>
                      </div>
                    )}
                  </div>
                  
                  {rulesSaveError && (
                    <div className={`p-2 mb-2 rounded-md ${isDark ? 'bg-red-800 bg-opacity-50 text-red-200' : 'bg-red-100 text-red-700'}`}>
                      {rulesSaveError}
                    </div>
                  )}
                  
                  {isEditingRules ? (
                    <textarea
                      value={userRules}
                      onChange={(e) => setUserRules(e.target.value)}
                      placeholder="Enter custom rules for this user..."
                      rows={6}
                      className={`w-full p-2 rounded-md ${isDark ? 'bg-gray-800 text-gray-200 border-gray-700' : 'bg-white text-gray-800 border-gray-300'} border`}
                    />
                  ) : (
                    <div className={`p-4 rounded-md ${isDark ? 'bg-gray-800' : 'bg-white'} border ${isDark ? 'border-gray-700' : 'border-gray-300'}`}>
                      {selectedUserData.user_details.rules ? (
                        <pre className="whitespace-pre-wrap font-mono text-sm">
                          {selectedUserData.user_details.rules}
                        </pre>
                      ) : (
                        <p className="text-gray-500 italic">No custom rules defined for this user.</p>
                      )}
                    </div>
                  )}
                </div>
              </div>

              {/* Activity Details Card */}
              <div className={`p-6 rounded-lg ${isDark ? 'bg-gray-700' : 'bg-gray-50'}`}>
                <h3 className="text-lg font-semibold mb-4 flex items-center"><FaClipboardList className="mr-2" /> Activity Details ({selectedUserData.analysis_count} Analyses)</h3>
                {selectedUserData.analyses && selectedUserData.analyses.length > 0 ? (
                  <ul className={`divide-y ${isDark ? 'divide-gray-600' : 'divide-gray-300'}`}>
                    {selectedUserData.analyses.map(analysis => (
                      <li key={analysis.id} className="py-4">
                        <p className="text-sm mb-1"><strong className="font-medium">Analysis ID:</strong> {analysis.id}</p>
                        <p className="text-sm mb-1"><strong className="font-medium">Created:</strong> {formatDateTime(analysis.created_at)}</p>
                        <p className={`text-sm p-2 rounded ${isDark ? 'bg-gray-800' : 'bg-white'}`}>
                          <strong className="font-medium">Question/Scenario:</strong> {analysis.user_question || 'N/A'}
                        </p>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="text-center py-4">No specific activity details found for this user.</p>
                )}
              </div>
            </>
          )}
        </div>
      )}
    </div>
  );
};

export default AdminDashboard;