import React from 'react';
import Navbar from './Navbar';
// import Footer from './Footer';
import { Outlet } from 'react-router-dom';

const Layout = () => (
  <>
    <Navbar />
    <div className="min-h-screen pt-16">
      <Outlet />
    </div>
    {/* <Footer /> */}
  </>
);

export default Layout;
