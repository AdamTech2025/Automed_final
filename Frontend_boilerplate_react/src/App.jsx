import React from "react";
import {
  BrowserRouter as Router,
  Route,
  Routes,
  Outlet,
} from "react-router-dom";
import Home1 from "./components/Pages/Home/Home1/Home1";
import Navbar from "./components/Main/Navbar.jsx";``
import Footer from "./components/Main/Footer.jsx";
// import Projects from './page/Projects.jsx';
import ContactUs from "./components/Pages/Contact/ContactUs.jsx";

const Layout = () => (
  <>
    <Navbar />
    <Outlet />
    <Footer />
  </>
);

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Home1 />} />
          <Route path="home1" element={<Home1 />} />
          {/* <Route path="home2" element={<Home2 />} /> */}
          {/* <Route path="about-company" element={<Banner />} /> */}
          {/* <Route path="core-values" element={<CoreValues />} /> */}
          {/* <Route path="leadership" element={<Leadership />} /> */}
          <Route path="history" element={<History />} />
          {/* <Route path="projects" element={<Projects />} /> */}
          {/* <Route path="services" element={<ServicesList />} /> */}
          {/* <Route path="blog-grid" element={<BlogGrid />} /> */}
          {/* <Route path="blog-list" element={<BlogList />} /> */}
          {/* <Route path="blog-details" element={<BlogDetails />} /> */}
          <Route path="contact-us" element={<ContactUs />} />
          {/* <Route path="services-list" element={<ServicesList />} /> */}
          {/* <Route path="services-details" element={<ServiceItems />} /> */}
          {/* <Route path="project-list" element={<ProjectList />} /> */}
          {/* <Route path="project-grid" element={<ProjectGrid />} /> */}
          {/* <Route path="project-details" element={<ProjectDetails />} /> */}
        </Route>
      </Routes>
    </Router>
  );
};

export default App;
