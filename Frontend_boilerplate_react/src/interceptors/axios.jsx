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
  timeout: 600000, // 10 minutes timeout
  // Remove withCredentials if you're using Bearer tokens and not cookies for auth
  // withCredentials: true 
});

// Request interceptor to add the auth token header
apiInstance.interceptors.request.use(
  (config) => {
    // List of endpoints that should NOT receive the Authorization header
    const publicEndpoints = [
      '/api/auth/login',
      '/api/auth/signup/send-otp',
      '/api/auth/signup/verify-otp'
      // Add any other public endpoints here
    ];

    // Check if the request URL is for a protected endpoint
    if (config.url && !publicEndpoints.some(endpoint => config.url.startsWith(endpoint))) {
      const token = localStorage.getItem('accessToken');
      if (token) {
        config.headers['Authorization'] = `Bearer ${token}`;
      }
    }
    return config;
  },
  (error) => {
    // Handle request error here
    return Promise.reject(error);
  }
);

export default apiInstance;