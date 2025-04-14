import axios from "axios";

// Determine the base URL based on window location
const getBaseUrl = () => {
  // Check if we're running in a browser
  if (typeof window !== 'undefined') {
    // If hostname is our production domain, use production API
    if (window.location.hostname === 'automed.adamtechnologies.in') {
      return 'https://python.adamtechnologies.in';
    }
  }
  
  // Otherwise fallback to environment variable or localhost
  return import.meta.env.VITE_API_URL || 'http://localhost:8000';
};

const apiInstance = axios.create({
  baseURL: getBaseUrl(),
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true // Include cookies in requests (if needed for authentication)
});

export default apiInstance;