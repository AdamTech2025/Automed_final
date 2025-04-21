import { useEffect } from 'react';
import PropTypes from 'prop-types';
import { gsap } from 'gsap';
import { createPortal } from 'react-dom';

// Get the portal root element
const modalRoot = document.getElementById('modal-root');

const SuccessModal = ({ title, message, isSuccess = true, onClose }) => {
  useEffect(() => {
    console.log('Modal mounted with title:', title, 'message:', message); // Debug log
    
    // Target the container that createPortal renders into
    const portalContainer = modalRoot?.firstChild; // Get the div rendered by createPortal
    
    const animationTimeout = setTimeout(() => {
        // Animate the portal container directly
        if (portalContainer) {
          gsap.from(portalContainer, { 
            duration: 0.6, 
            scale: 0.7, 
            opacity: 0, 
            ease: "back.out",
            // Optional: Add a small delay if needed
            // delay: 0.05 
          });
        } else {
          console.error('Modal portal container not found for GSAP animation.');
        }
    }, 50); // 50ms delay, adjust if needed

    const handleEsc = (e) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };

    window.addEventListener('keydown', handleEsc);

    return () => {
      clearTimeout(animationTimeout); // Clear the timeout on unmount
      window.removeEventListener('keydown', handleEsc);
      console.log('Modal unmounted');
    };
  }, [onClose, title, message]);

  // Ensure modalRoot exists before attempting to portal
  if (!modalRoot) {
    console.error("Modal root element #modal-root not found in the DOM.");
    return null; // Don't render if the target doesn't exist
  }
  
  // Add this log to confirm the target element exists
  console.log("Rendering modal into target:", modalRoot);

  return createPortal(
    <div className="fixed inset-0 flex items-center justify-center z-[1000] bg-black bg-opacity-60 backdrop-blur-sm">
      <div className="modal-content bg-gray-800 bg-opacity-90 rounded-2xl p-0 max-w-sm w-full border border-gray-700 shadow-xl overflow-hidden">
        <div className={`text-xl font-semibold text-center py-3 px-4 ${isSuccess ? 'bg-yellow-500' : 'bg-red-600'} text-white`}>
          {title}
        </div>
        <div className="p-6 text-gray-100 text-center text-base">
          {message}
        </div>
        <div className="px-6 pb-4 text-center mt-2">
          <button
            onClick={onClose}
            className="w-full bg-yellow-400 text-gray-900 font-semibold py-2.5 px-4 rounded-lg hover:bg-yellow-500 transition duration-300 focus:outline-none focus:ring-2 focus:ring-yellow-300"
          >
            Close
          </button>
        </div>
      </div>
    </div>,
    modalRoot // Target the dedicated modal root div
  );
};

SuccessModal.propTypes = {
  title: PropTypes.string.isRequired,
  message: PropTypes.string.isRequired,
  isSuccess: PropTypes.bool,
  onClose: PropTypes.func.isRequired,
};

export default SuccessModal;