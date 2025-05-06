import { Route, Routes, Outlet, Navigate } from 'react-router-dom';
import { useState } from 'react';
import Home1 from '../components/Pages/Home.jsx';
import Navbar from '../components/Comman/Navbar.jsx';
import Sidebar from '../components/Comman/Sidebar.jsx';
import Login from '../components/Comman/Login.jsx';
import Signup from '../components/Comman/Signup.jsx';
import AdminDashboard from '../components/Pages/AdminDashboard.jsx';
import UserActivity from '../components/Pages/UserActivity.jsx';
import Topics from '../components/Pages/Admin/Topics.jsx';
import Extractor from '../components/Pages/Extractor.jsx';
import { useAuth } from '../context/AuthContext';
import PropTypes from 'prop-types';

const Layout = () => {
  const [isSidebarVisible, setIsSidebarVisible] = useState(false);

  const toggleSidebar = () => {
    setIsSidebarVisible(!isSidebarVisible);
  };

  return (
    <div className="flex min-h-screen">
      <Sidebar isVisible={isSidebarVisible} toggleSidebar={toggleSidebar} />
      <div className="flex-1 flex flex-col">
        <Navbar toggleSidebar={toggleSidebar} />
        <main className="flex-1">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

const ProtectedRoute = ({ children }) => {
  const { isAuthenticated } = useAuth();
  if (!isAuthenticated) {
    return <Navigate to="/" replace />;
  }
  return children;
};

ProtectedRoute.propTypes = {
    children: PropTypes.node.isRequired,
};

const AdminProtectedRoute = ({ children }) => {
  const { isAuthenticated, user } = useAuth();
  if (!isAuthenticated) {
    return <Navigate to="/" replace />;
  }
  if (user?.role !== 'admin') {
    console.warn("Admin route access denied for user role:", user?.role);
    return <Navigate to="/dashboard" replace />;
  }
  return children;
};

AdminProtectedRoute.propTypes = {
    children: PropTypes.node.isRequired,
};

// Simple component for the extractor page without sidebar/navbar layout
// This component handles its own auth check to prevent redirect loops
const ExtractorPage = () => {
  const { isAuthenticated } = useAuth();
  
  // If not authenticated, show a login prompt instead of redirecting
  if (!isAuthenticated) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gray-100 dark:bg-gray-900">
        <div className="bg-white dark:bg-gray-800 p-8 rounded-lg shadow-lg max-w-md w-full text-center">
          <h2 className="text-2xl font-bold mb-4 text-gray-800 dark:text-white">Authentication Required</h2>
          <p className="text-gray-600 dark:text-gray-300 mb-6">Please login to access the PDF Extractor</p>
          <a 
            href="/" 
            className="inline-block bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Go to Login
          </a>
        </div>
      </div>
    );
  }
  
  // User is authenticated, show the extractor
  return <Extractor />;
};

const AppRoutes = () => {
  const { isAuthenticated } = useAuth();

  return (
    <Routes>
      <Route 
        path="/" 
        element={isAuthenticated ? <Navigate to="/dashboard" replace /> : <Login />} 
      />
      <Route 
        path="/signup" 
        element={isAuthenticated ? <Navigate to="/dashboard" replace /> : <Signup />} 
      />
      <Route 
        path="/dashboard" 
        element={
          <ProtectedRoute>
            <Layout />
          </ProtectedRoute>
        }
      >
        <Route index element={<Home1 />} />
      </Route>
      <Route 
        path="/extractor" 
        element={<ExtractorPage />}
      />
      <Route 
        path="/admin/dashboard" 
        element={
          <AdminProtectedRoute>
            <Layout />
          </AdminProtectedRoute>
        }
      >
        <Route index element={<AdminDashboard />} />
      </Route>
      <Route
        path="/admin/prompt-management/topics"
        element={
          <AdminProtectedRoute>
            <Layout />
          </AdminProtectedRoute>
        }
      >
        <Route index element={<Topics />} />
      </Route>
      <Route 
        path="/user/:userId/activity" 
        element={
          <AdminProtectedRoute>
            <Layout />
          </AdminProtectedRoute>
        }
      >
        <Route index element={<UserActivity />} /> 
      </Route>
    </Routes>
  );
};

export default AppRoutes;
