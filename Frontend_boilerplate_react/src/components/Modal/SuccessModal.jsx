import { useEffect } from 'react';
import PropTypes from 'prop-types';
import { gsap } from 'gsap';

const SuccessModal = ({ title, message, isSuccess = true, onClose }) => {
  useEffect(() => {
    // Animation for modal entrance
    gsap.from(".modal-content", { 
      duration: 0.6, 
      scale: 0.7, 
      opacity: 0, 
      ease: "back.out" 
    });
    
    // Add event listener for ESC key to close modal
    const handleEsc = (e) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };
    
    window.addEventListener('keydown', handleEsc);
    
    return () => {
      window.removeEventListener('keydown', handleEsc);
    };
  }, [onClose]);
  
  return (
    <div className="fixed inset-0 flex items-center justify-center z-50 bg-black bg-opacity-80 backdrop-blur-sm">
      <div className={`modal-content bg-white rounded-2xl p-8 max-w-sm w-full ${!isSuccess ? 'border-l-4 border-red-500' : ''}`}>
        <h3 className="text-2xl font-semibold text-gray-800 mb-4">
          {title}
        </h3>
        <p className="text-gray-600 mb-6">
          {message}
        </p>
        <button 
          onClick={onClose}
          className="w-full bg-yellow-400 text-gray-900 font-semibold py-2 rounded-lg hover:bg-yellow-500 transition duration-300"
        >
          Close
        </button>
      </div>
    </div>
  );
};

SuccessModal.propTypes = {
  title: PropTypes.string.isRequired,
  message: PropTypes.string.isRequired,
  isSuccess: PropTypes.bool,
  onClose: PropTypes.func.isRequired
};

export default SuccessModal; 