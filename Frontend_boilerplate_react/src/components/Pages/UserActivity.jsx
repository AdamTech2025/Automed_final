import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { getUserActivity } from '../../interceptors/services'; // We will create this service function next
import { useTheme } from '../../context/ThemeContext';
import { FaUserClock, FaTasks } from 'react-icons/fa';

const UserActivity = () => {
  const { userId } = useParams(); // Get userId from URL
  const [activityData, setActivityData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const { isDark } = useTheme();

  useEffect(() => {
    const controller = new AbortController();
    const fetchData = async () => {
      setIsLoading(true);
      setError(null);
      try {
        console.log(`Fetching activity for user ID: ${userId}`);
        // const response = await getUserActivity(userId, controller.signal); // Call the service function
        // setActivityData(response); // Assuming response is the data needed
        // Placeholder data for now:
        await new Promise(resolve => setTimeout(resolve, 500)); // Simulate network delay
        setActivityData({ 
          message: `Activity data for user ${userId} will be shown here.`,
          details: [] // Replace with actual activity details later
        }); 
      } catch (err) {
        if (err.name !== 'AbortError') {
          console.error(`Failed to fetch activity for user ${userId}:`, err);
          setError(err.detail || err.message || 'Failed to load user activity.');
        }
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();

    return () => {
      controller.abort();
    };
  }, [userId]); // Re-run effect if userId changes

  return (
    <div className={`min-h-screen p-4 sm:p-8 transition-colors duration-300 ${isDark ? 'bg-gray-900 text-gray-200' : 'bg-gray-100 text-gray-800'}`}>
      <h1 className="text-2xl sm:text-3xl font-bold mb-6 flex items-center">
        <FaUserClock className="mr-3" /> User Activity - ID: {userId}
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

      {!isLoading && !error && activityData && (
        <div className={`${isDark ? 'bg-gray-800' : 'bg-white'} shadow-lg rounded-lg p-6`}>
          <h2 className="text-xl font-semibold mb-4 flex items-center">
            <FaTasks className="mr-2" /> Activity Details
          </h2>
          {/* Display activity data here */} 
          <p>{activityData.message}</p>
          {activityData.details && activityData.details.length > 0 ? (
            <ul>
              {activityData.details.map((item, index) => (
                <li key={index}>{/* Render activity item */}</li>
              ))}
            </ul>
          ) : (
            <p className="mt-4 text-gray-500">No specific activity details found.</p>
          )}
        </div>
      )}
      
      {!isLoading && !error && !activityData && (
         <p className="mt-4 text-gray-500">No activity data available for this user.</p>
      )}
    </div>
  );
};

export default UserActivity; 