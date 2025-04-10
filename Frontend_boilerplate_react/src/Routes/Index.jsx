import { Route, Routes, Outlet } from 'react-router-dom';
import Home1 from '../components/Pages/Home.jsx';
import Navbar from '../components/Main/Navbar';

const Layout = () => (
  <>
    <Navbar />
    <Outlet />
  </>
);

const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Home1 />} />
        <Route path="home1" element={<Home1 />} />
      </Route>
    </Routes>
  );
};

export default AppRoutes;
