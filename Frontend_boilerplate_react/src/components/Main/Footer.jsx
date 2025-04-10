import React from 'react';
import logo from "../../assets/images/logo_favicon.png"
import person1 from "../../assets/images/testimonial2.jpg"
import person2 from "../../assets/images/testimonial4.jpg"
import ScrollArrow from './ScrollArrow';

const Footer = () => {
  return (
    <>
    <div>
      <ScrollArrow/>
      </div>
    <footer className="bg-black text-white py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row items-center justify-between">
        {/* Logo and Contact Information */}
        <div className="flex items-center space-x-4 mb-4 md:mb-0">
          <div className="bg-gray-300 h-12 w-12 flex items-center justify-center rounded-full">
          <span className="text-gray-600 text-lg font-bold"><img src={logo} alt="" /></span>
          </div>
          <div className="text-gray-400">
            <p>Sales representative</p>
            <p>+91 9786452310</p>
            <p>free call!</p>
          </div>
        </div>

        {/* Social Icons and Consultation Button */}
        <div className="flex items-center space-x-4 mb-4 md:mb-0 ">
          <div className="flex space-x-2">
            
            <div className="bg-gray-300 h-8 w-8 flex items-center justify-center rounded-full">
            <span className="text-gray-600"><img src={person1} alt="" /></span>
            </div>
            <div className="bg-gray-300 h-8 w-8 flex items-center justify-center rounded-full">
            <span className="text-gray-600"><img src={person2} alt="" /></span>
            </div>
          </div>
          <button className="bg-white text-black font-bold py-2 px-4 rounded shadow-md">
            Get a Consultation
          </button>
        </div>
      </div>

      {/* Information, Contact Details, Newsletter */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-8">
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-8 text-center sm:text-left">
          {/* Information Section */}
          <div>
            <p className="text-gray-300">Information</p>
            <p className="text-gray-500">
              We successfully cope with tasks of varying complexity, provide long-term guarantees and regularly master new technologies.
            </p>
          </div>

          {/* Contact Section */}
          <div>
            <p className="text-gray-300">Contact</p>
            <p className="text-gray-500">
            3rd Floor, New No. 75, 77 & 79, Lohmanradhri Towers, Pantheon Rd, Egmore, Chennai, Tamil Nadu 600008
            </p>
          </div>

          {/* Newsletter Section */}
          <div className="flex flex-col">
            <p className="text-gray-300">Newsletter</p>
            <p className="text-gray-500 mb-4">
            Join our community and receive weekly news straight to your inbox.
            </p>
            <div className="flex items-center">
              <input
                type="email"
                placeholder="Your email"
                className="px-4 py-2 border border-white rounded-l w-full focus:outline-none bg-gray-700 text-white"
              />
              <button className="bg-white text-black font-bold py-2 px-4 rounded-r shadow-md">
                Send
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Footer Bottom */}
      <hr className="my-8 border-gray-600" />
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row items-center justify-between text-sm">
        <div className="text-gray-400 mb-4 md:mb-0">
            EliteConstruct Private Ltd © 2024 whythemes All rights reserved
        </div>
        <div className="flex space-x-4">
          <a href="#" className="text-gray-400 hover:text-gray-200">
            Facebook
          </a>
          <a href="#" className="text-gray-400 hover:text-gray-200">
            Twitter
          </a>
          <a href="#" className="text-gray-400 hover:text-gray-200">
            LinkedIn
          </a>
        </div>
      </div>
    </footer>
    </>
  );
};

export default Footer;
