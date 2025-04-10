import { Link } from 'react-router-dom';
import { FaTooth, FaPowerOff } from 'react-icons/fa';

const Navbar = () => {
  return (
    <nav className="w-full p-4 bg-white shadow-md flex flex-col sm:flex-row items-center justify-between">
      <div className="flex items-center mb-4 sm:mb-0">
        <FaTooth className="text-blue-600 text-2xl md:text-3xl mr-2" />
        <Link to="/" className="text-blue-600 font-bold text-lg md:text-xl">
          Dental Code Extractor Pro
        </Link>
      </div>
      <button className="bg-red-600 text-white px-4 py-2 rounded-lg shadow-md hover:bg-red-700 text-sm md:text-base flex items-center">
        <FaPowerOff className="inline mr-2" />Reset
      </button>
    </nav>
  );
};

export default Navbar;