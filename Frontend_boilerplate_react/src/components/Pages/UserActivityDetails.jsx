import { useState, useEffect } from 'react';
import { useParams, useLocation, Link } from 'react-router-dom';
import { getUserActivity } from '../../interceptors/services';
import { useTheme } from '../../context/ThemeContext';
import { FaUserCircle, FaEnvelope, FaPhone, FaCalendarAlt, FaClipboardList, FaArrowLeft } from 'react-icons/fa';

const UserActivityDetails = () => {
  // Get userId from URL params or location state
  const { userId: userIdParam } = useParams();
  const location = useLocation();
  const userIdFromState = location.state?.userId;
  
  // Use state from navigate if available, otherwise use URL param
  const userId = userIdFromState || userIdParam;
  
  const [userData, setUserData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [debugInfo, setDebugInfo] = useState({ 
    userId, 
    fromState: !!userIdFromState,
    fromParams: !!userIdParam 
  });
  const { isDark } = useTheme();

  useEffect(() => {
    // Update debug info when userId changes
    setDebugInfo(prev => ({
      ...prev,
      userId,
      fromState: !!userIdFromState,
      fromParams: !!userIdParam
    }));

    if (!userId) {
      setError('User ID is missing. Cannot fetch user data.');
      setIsLoading(false);
      return;
    }
    
    const controller = new AbortController();
    const fetchData = async () => {
      setIsLoading(true);
      setError(null);
      setUserData(null); // Clear previous data
      
      try {
        console.log(`🔍 Fetching user data for ID: ${userId}`);
        const response = await getUserActivity(userId, controller.signal);
        console.log(`✅ Received user data:`, response);
        
        if (!response) {
          throw new Error('Empty response received from server');
        }
        
        // Only update state if the component is still mounted
        if (!controller.signal.aborted) {
          setUserData(response);
          setDebugInfo(prev => ({ ...prev, responseReceived: true, dataEmpty: !response }));
        }
      } catch (err) {
        // Don't set error for aborted requests - that's normal when component unmounts
        if (err.name !== 'AbortError' && err.name !== 'CanceledError') {
          console.error(`❌ Failed to fetch activity for user ${userId}:`, err);
          setError(err.detail || err.message || 'Failed to load user activity. Check permissions or user ID.');
          setDebugInfo(prev => ({ 
            ...prev, 
            error: err.message, 
            errorDetail: err.detail,
            errorStack: err.stack
          }));
        }
      } finally {
        // Only update state if the component is still mounted
        if (!controller.signal.aborted) {
          setIsLoading(false);
        }
      }
    };

    fetchData();

    // Cleanup function to abort fetch if component unmounts or userId changes
    return () => {
      controller.abort();
    };
  }, [userId, userIdParam, userIdFromState]); // Re-run effect if any of these change

  const formatDate = (dateString) => {
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

  return (
    <div className={`min-h-screen p-4 sm:p-8 transition-colors duration-300 ${isDark ? 'bg-gray-900 text-gray-200' : 'bg-gray-100 text-gray-800'}`}>
      <Link 
        to="/admin/dashboard" 
        className={`inline-flex items-center mb-6 px-4 py-2 rounded-md text-sm font-medium transition-colors ${isDark ? 'bg-gray-700 hover:bg-gray-600 text-gray-200' : 'bg-gray-200 hover:bg-gray-300 text-gray-700'}`}
      >
        <FaArrowLeft className="mr-2" /> Back to Admin Dashboard
      </Link>

      <h1 className="text-2xl sm:text-3xl font-bold mb-6 flex items-center">
        <FaUserCircle className="mr-3" /> User Activity - ID: {userId || "Not provided"}
      </h1>

      {/* Debug Panel */}
      <div className={`mb-6 p-4 rounded-lg text-xs ${isDark ? 'bg-gray-800 text-gray-300' : 'bg-gray-200 text-gray-700'}`}>
        <details>
          <summary className="font-medium cursor-pointer">Debug Info (Expand)</summary>
          <pre className="mt-2 overflow-auto">{JSON.stringify(debugInfo, null, 2)}</pre>
        </details>
      </div>

      {isLoading && (
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-blue-500"></div>
        </div>
      )}

      {error && (
        <div className={`p-4 rounded-md mb-6 ${isDark ? 'bg-red-800 bg-opacity-50 text-red-200' : 'bg-red-100 text-red-700'}`}>
          <p className="font-semibold">Error:</p>
          <p>{error}</p>
          <details className="mt-2">
            <summary className="cursor-pointer">Technical Details</summary>
            <pre className="mt-2 text-xs overflow-auto">{JSON.stringify(debugInfo, null, 2)}</pre>
          </details>
        </div>
      )}

      {!isLoading && !error && userData && (
        <>
          {/* User Details Card */}
          <div className={`mb-8 p-6 rounded-lg shadow-lg ${isDark ? 'bg-gray-800' : 'bg-white'}`}>
            <h2 className="text-xl font-semibold mb-4 flex items-center"><FaUserCircle className="mr-2" /> User Details</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <p><strong className="font-medium">Name:</strong> {userData.user_details?.name || 'N/A'}</p>
              <p className="flex items-center"><FaEnvelope className="mr-2 opacity-70" /> <strong className="font-medium mr-1">Email:</strong> {userData.user_details?.email || 'N/A'}</p>
              <p className="flex items-center"><FaPhone className="mr-2 opacity-70" /> <strong className="font-medium mr-1">Phone:</strong> {userData.user_details?.phone || 'N/A'}</p>
              <p className="flex items-center"><FaCalendarAlt className="mr-2 opacity-70" /> <strong className="font-medium mr-1">Joined:</strong> {formatDate(userData.user_details?.created_at)}</p>
              <p><strong className="font-medium">Role:</strong> 
                <span className={`ml-2 px-2 py-0.5 rounded-full text-xs font-medium ${
                  userData.user_details?.role === 'admin'
                  ? (isDark ? 'bg-purple-600 text-purple-100' : 'bg-purple-200 text-purple-800')
                  : (isDark ? 'bg-blue-600 text-blue-100' : 'bg-blue-200 text-blue-800')
                }`}>
                  {userData.user_details?.role || 'N/A'}
                </span>
              </p>
              <p><strong className="font-medium">Email Verified:</strong> {userData.user_details?.is_email_verified ? 'Yes' : 'No'}</p>
            </div>
          </div>

          {/* Activity Details Card */}
          <div className={`p-6 rounded-lg shadow-lg ${isDark ? 'bg-gray-800' : 'bg-white'}`}>
            <h2 className="text-xl font-semibold mb-4 flex items-center"><FaClipboardList className="mr-2" /> Activity Details ({userData.analysis_count || 0} Analyses)</h2>
            {userData.analyses && userData.analyses.length > 0 ? (
              <ul className={`divide-y ${isDark ? 'divide-gray-700' : 'divide-gray-200'}`}>
                {userData.analyses.map(analysis => (
                  <li key={analysis.id} className="py-4">
                    <p className="text-sm mb-1"><strong className="font-medium">Analysis ID:</strong> {analysis.id}</p>
                    <p className="text-sm mb-1"><strong className="font-medium">Created:</strong> {formatDate(analysis.created_at)}</p>
                    <p className={`text-sm p-2 rounded ${isDark ? 'bg-gray-700' : 'bg-gray-50'}`}>
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

      {!isLoading && !error && !userData && (
         <p className="text-center py-4">No data available for this user.</p>
      )}
    </div>
  );
};

export default UserActivityDetails; 