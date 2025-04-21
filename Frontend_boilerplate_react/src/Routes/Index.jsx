import { Route, Routes, Outlet } from 'react-router-dom';
import Home1 from '../components/Pages/Home.jsx';
import Navbar from '../components/Comman/Navbar.jsx';
import Login from '../components/Comman/Login.jsx';
import Signup from '../components/Comman/Signup.jsx';

const Layout = () => (
  <>
    <Navbar />
    <Outlet />
  </>
);

const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/signup" element={<Signup />} />
      <Route path="/dashboard" element={<Layout />}>
        <Route index element={<Home1 />} />
        <Route path="home" element={<Home1 />} />
      </Route>
    </Routes>
  );
};

export default AppRoutes;
