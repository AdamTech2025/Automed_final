import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import Dropdown from '../Pages/Navbar/Dropdown';
import ThemeToggle from '../Pages/Navbar/ThemeToggle';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCaretDown, faBars } from '@fortawesome/free-solid-svg-icons';
import LogoMain from "../../assets/images/logo_main.png";
import LogoFavicon from "../../assets/images/logo_favicon.png";

const Navbar = () => {
  const [scrollPosition, setScrollPosition] = useState(0);
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isMobile, setIsMobile] = useState(window.innerWidth < 768);

  const handleScroll = () => {
    const position = window.scrollY;
    setScrollPosition(position);
  };

  const [openStatus, setOpenStatus] = useState("home");

  const handleMenuToggle = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const handleResize = () => {
    setIsMobile(window.innerWidth < 768);
  };

  const scrollToTop = () => {
    setIsMenuOpen(false)
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  useEffect(() => {
    console.log(openStatus);
  }, [openStatus]);

  useEffect(() => {
    window.addEventListener('scroll', handleScroll, { passive: true });
    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('scroll', handleScroll);
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  const navbarBackground = scrollPosition > window.innerHeight * 0.25 ? 'bg-black' : '';

  return (
    <nav className={`flex items-center justify-between p-4 fixed z-50 top-0 left-0 right-0 text-white transition duration-300 ${navbarBackground}`}>
      <div className="flex items-center space-x-6">
        <Link to="/" className="text-2xl font-bold" onClick={scrollToTop}>
          <img src={isMobile ? LogoFavicon : LogoMain} className={isMobile ? 'w-10 h-10 ml-6' : 'w-40 h-8 ml-6'} alt="logo" />
        </Link>
      </div>
      <div className="hidden md:flex items-center space-x-6 text-lg">
        <Dropdown title="Home" setOpenStatus={() => { setOpenStatus("Home") }} icon={<FontAwesomeIcon icon={faCaretDown} />}>
          <Link to="/home1" className="block px-4 py-2 hover:bg-gray-700" onClick={scrollToTop}>Home 1</Link>
          <Link to="/home2" className="block px-4 py-2 hover:bg-gray-700" onClick={scrollToTop}>Home 2</Link>
        </Dropdown>
        <Dropdown title="About Us" setOpenStatus={() => { setOpenStatus("About Us") }} icon={<FontAwesomeIcon icon={faCaretDown} />}>
          <Link to="/about-company" className="block px-4 py-2 hover:bg-gray-700" onClick={scrollToTop}>About Company</Link>
          <Link to="/core-values" className="block px-4 py-2 hover:bg-gray-700" onClick={scrollToTop}>Core Values</Link>
          <Link to="/leadership" className="block px-4 py-2 hover:bg-gray-700" onClick={scrollToTop}>Leadership</Link>
          <Link to="/history" className="block px-4 py-2 hover:bg-gray-700" onClick={scrollToTop}>History</Link>
        </Dropdown>
        <Dropdown title="Pages" setOpenStatus={() => { setOpenStatus("Pages") }} icon={<FontAwesomeIcon icon={faCaretDown} />}>
          {openStatus === "Pages" ? <>
            <Dropdown title="Projects" icon={<FontAwesomeIcon icon={faCaretDown} />} position="right" subMenu setOpenStatus={(status) => { setOpenStatus(status) }}>
              <Link to="/project-list" className="block px-4 py-2 hover:bg-gray-700" onClick={scrollToTop}>Projects List</Link>
              <Link to="/project-grid" className="block px-4 py-2 hover:bg-gray-700" onClick={scrollToTop}>Projects Grid</Link>
              <Link to="/project-details" className="block px-4 py-2 hover:bg-gray-700" onClick={scrollToTop}>Projects Details</Link>
            </Dropdown>
            <Dropdown title="Services" icon={<FontAwesomeIcon icon={faCaretDown} />} position="right" subMenu setOpenStatus={(status) => { setOpenStatus(status) }}>
              <Link to="/services-list" className="block px-4 py-2 hover:bg-gray-700" onClick={scrollToTop}>Services List</Link>
              <Link to="/services-details" className="block px-4 py-2 hover:bg-gray-700" onClick={scrollToTop}>Services Details</Link>
            </Dropdown>
          </> : <></>}
        </Dropdown>
        <Dropdown title="Blog" setOpenStatus={() => { setOpenStatus("Blog") }} icon={<FontAwesomeIcon icon={faCaretDown} />}>
          <Link to="/blog-grid" className="block px-4 py-2 hover:bg-gray-700" onClick={scrollToTop}>Blog Grid</Link>
          <Link to="/blog-list" className="block px-4 py-2 hover:bg-gray-700" onClick={scrollToTop}>Blog List</Link>
          <Link to="/blog-details" className="block px-4 py-2 hover:bg-gray-700" onClick={scrollToTop}>Blog Details</Link>
        </Dropdown>
        <Link to="/contact-us" className="px-4 py-2 hover:bg-gray-700" onClick={scrollToTop}>Contact Us</Link>
      </div>
      <div className="flex items-center space-x-4">
        <div className="bg-gray-800 px-4 py-2 rounded-md hidden md:block">Contact: 1234567890</div>
        <ThemeToggle />
        <button className="md:hidden" onClick={handleMenuToggle}>
          <FontAwesomeIcon icon={faBars} className="text-xl" />
        </button>
      </div>
      {isMenuOpen && (
        <div className="md:hidden absolute top-16 left-0 w-full bg-black p-4 space-y-2 text-sm ">
          <Dropdown title="Home" icon={<FontAwesomeIcon icon={faCaretDown} />}>
            <Link to="/home1" className="block px-4 py-2 hover:bg-gray-700" onClick={scrollToTop}>Home 1</Link>
            <Link to="/home2" className="block px-4 py-2 hover:bg-gray-700" onClick={scrollToTop}>Home 2</Link>
          </Dropdown>
          <Dropdown title="About Us" icon={<FontAwesomeIcon icon={faCaretDown} />}>
            <Link to="/about-company" className="block px-4 py-2 hover:bg-gray-700" onClick={scrollToTop}>About Company</Link>
            <Link to="/core-values" className="block px-4 py-2 hover:bg-gray-700" onClick={scrollToTop}>Core Values</Link>
            <Link to="/leadership" className="block px-4 py-2 hover:bg-gray-700" onClick={scrollToTop}>Leadership</Link>
            <Link to="/history" className="block px-4 py-2 hover:bg-gray-700" onClick={scrollToTop}>History</Link>
          </Dropdown>
          <Dropdown title="Pages" icon={<FontAwesomeIcon icon={faCaretDown} />}>
            <Dropdown title="Projects" icon={<FontAwesomeIcon icon={faCaretDown} />} position="right">
              <Link to="/project-list" className="block px-4 py-2 hover:bg-gray-700" onClick={scrollToTop}>Projects List</Link>
              <Link to="/project-grid" className="block px-4 py-2 hover:bg-gray-700" onClick={scrollToTop}>Projects Grid</Link>
              <Link to="project-details" className="block px-4 py-2 hover:bg-gray-700" onClick={scrollToTop}>Projects Details</Link>
            </Dropdown>
            <Dropdown title="Services" icon={<FontAwesomeIcon icon={faCaretDown} />} position="right">
              <Link to="/services-list" className="block px-4 py-2 hover:bg-gray-700" onClick={scrollToTop}>Services List</Link>
              <Link to="/services-details" className="block px-4 py-2 hover:bg-gray-700" onClick={scrollToTop}>Services Details</Link>
            </Dropdown>
          </Dropdown>
          <Dropdown title="Blog" icon={<FontAwesomeIcon icon={faCaretDown} />}>
            <Link to="/blog-grid" className="block px-4 py-2 hover:bg-gray-700" onClick={scrollToTop}>Blog Grid</Link>
            <Link to="/blog-list" className="block px-4 py-2 hover:bg-gray-700" onClick={scrollToTop}>Blog List</Link>
            <Link to="/blog-details" className="block px-4 py-2 hover:bg-gray-700" onClick={scrollToTop}>Blog Details</Link>
          </Dropdown>
          <Link to="/contact-us" className="block px-4 py-2 hover:bg-gray-700" onClick={scrollToTop}>Contact Us</Link>
        </div>
      )}
    </nav>
  );
};

export default Navbar;
