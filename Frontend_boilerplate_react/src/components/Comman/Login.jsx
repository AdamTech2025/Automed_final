import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import confetti from 'canvas-confetti';
import { gsap } from 'gsap';
import Particles from '../Particles/Particles';
import SuccessModal from '../Modal/SuccessModal';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [progress, setProgress] = useState(0);
  const [showModal, setShowModal] = useState(false);
  const [modalData, setModalData] = useState({ title: '', message: '', isSuccess: true });
  const navigate = useNavigate();

  useEffect(() => {
    // GSAP animations on component mount
    gsap.from(".card", { duration: 1.2, y: 150, opacity: 0, ease: "power4.out" });
    gsap.from(".card h2", { duration: 1, delay: 0.3, opacity: 0, x: -30, ease: "power4.out" });
    gsap.from(".card input", { duration: 0.8, delay: 0.5, opacity: 0, y: 20, stagger: 0.2, ease: "power4.out" });
    gsap.from("footer", { duration: 1, delay: 0.8, opacity: 0, y: 50, ease: "power4.out" });
  }, []);

  useEffect(() => {
    // Update progress bar based on form completion
    const totalFields = 2; // email and password
    let filledFields = 0;
    
    if (email.trim()) filledFields++;
    if (password.trim()) filledFields++;
    
    setProgress((filledFields / totalFields) * 100);
  }, [email, password]);

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (email && password) {
      // Show success modal
      setModalData({
        title: 'Welcome Back!',
        message: 'You have successfully logged in to Adam Tech! (Demo)',
        isSuccess: true
      });
      setShowModal(true);
      
      // Launch confetti
      confetti({
        particleCount: 100,
        spread: 70,
        origin: { y: 0.6 }
      });
      
      // Add actual login logic here
    } else {
      // Show error modal
      setModalData({
        title: 'Error',
        message: 'Please fill in all fields.',
        isSuccess: false
      });
      setShowModal(true);
    }
  };

  return (
    <>
      <Particles />
      
      <div className="container mx-auto max-w-lg px-4 py-8 relative">
        <div className="card p-8 backdrop-blur-xl bg-white bg-opacity-20 border border-white border-opacity-20 rounded-2xl">
          <div className="flex justify-center mb-6">
            <img src="https://via.placeholder.com/80?text=🦷" alt="Adam Tech Logo" className="w-20 h-20 animate-[float_3s_ease-in-out_infinite]" />
          </div>
          
          <h2 className="text-4xl font-bold text-center text-white mb-2">Adam Tech</h2>
          <p className="text-center text-gray-300 mb-6">Dental Coding Software</p>
          
          <div className="w-full bg-gray-700 bg-opacity-50 rounded-full h-1 mb-6">
            <div 
              className="bg-yellow-400 h-1 rounded-full transition-all duration-300"
              style={{ width: `${progress}%` }}
            ></div>
          </div>
          
          <form onSubmit={handleSubmit}>
            <div className="mb-4">
              <label htmlFor="email" className="block text-sm font-medium text-gray-200">Email</label>
              <input 
                type="email" 
                id="email" 
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="mt-1 block w-full rounded-lg border-none bg-white bg-opacity-20 text-white focus:border-yellow-400 focus:ring focus:ring-yellow-400 focus:ring-opacity-50 p-3 transition-all duration-300"
                placeholder="you@example.com"
              />
            </div>
            
            <div className="mb-6">
              <label htmlFor="password" className="block text-sm font-medium text-gray-200">Password</label>
              <input 
                type="password" 
                id="password" 
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="mt-1 block w-full rounded-lg border-none bg-white bg-opacity-20 text-white focus:border-yellow-400 focus:ring focus:ring-yellow-400 focus:ring-opacity-50 p-3 transition-all duration-300"
                placeholder="••••••••"
              />
            </div>
            
            <button 
              type="submit"
              className="w-full bg-yellow-400 text-gray-900 font-semibold py-3 rounded-lg hover:bg-yellow-500 transition duration-300 relative overflow-hidden"
            >
              Login
            </button>
          </form>
          
          <p className="mt-4 text-center text-sm text-gray-300">
            Don&apos;t have an account? <Link to="/signup" className="text-yellow-400 hover:underline">Sign Up</Link>
          </p>
        </div>
      </div>
      
      {/* Success Modal */}
      {showModal && (
        <SuccessModal 
          title={modalData.title}
          message={modalData.message}
          isSuccess={modalData.isSuccess}
          onClose={() => setShowModal(false)}
        />
      )}
      
      {/* Footer */}
      <footer className="bg-gray-900 text-gray-300 py-6">
        <div className="container mx-auto px-4 text-center">
          <p className="mb-2">&copy; 2025 Adam Tech. All rights reserved.</p>
          <div className="flex justify-center space-x-4">
            <a href="#" className="hover:text-yellow-400 transition">Twitter</a>
            <a href="#" className="hover:text-yellow-400 transition">LinkedIn</a>
            <a href="#" className="hover:text-yellow-400 transition">Support</a>
          </div>
        </div>
      </footer>
    </>
  );
};

export default Login; 