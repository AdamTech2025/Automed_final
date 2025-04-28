import { Route, Routes, Outlet, Navigate } from 'react-router-dom';
import { useState } from 'react';
import Home1 from '../components/Pages/Home.jsx';
import Navbar from '../components/Comman/Navbar.jsx';
import Sidebar from '../components/Comman/Sidebar.jsx';
import Login from '../components/Comman/Login.jsx';
import Signup from '../components/Comman/Signup.jsx';
import AdminDashboard from '../components/Pages/AdminDashboard.jsx';
import UserActivity from '../components/Pages/UserActivity.jsx';
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
