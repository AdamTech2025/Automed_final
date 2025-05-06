import { useEffect } from 'react';
import confetti from 'canvas-confetti';
import PropTypes from 'prop-types';

const TourConfetti = ({ isActive }) => {
  useEffect(() => {
    if (isActive) {
      launchConfetti();
    }
  }, [isActive]);

  const launchConfetti = () => {
    // First burst
    confetti({
      particleCount: 100,
      spread: 70,
      origin: { y: 0.6 },
      colors: ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'],
    });

    // Second burst with slight delay
    setTimeout(() => {
      confetti({
        particleCount: 50,
        angle: 60,
        spread: 55,
        origin: { x: 0 },
        colors: ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'],
      });
    }, 250);

    // Third burst with slight delay
    setTimeout(() => {
      confetti({
        particleCount: 50,
        angle: 120,
        spread: 55,
        origin: { x: 1 },
        colors: ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'],
      });
    }, 400);
  };

  return null; // This component doesn't render anything
};

TourConfetti.propTypes = {
  isActive: PropTypes.bool.isRequired
};

export default TourConfetti; 