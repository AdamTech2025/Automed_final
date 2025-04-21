import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import confetti from 'canvas-confetti';
import { gsap } from 'gsap';
import Particles from '../Particles/Particles';
import SuccessModal from '../Modal/SuccessModal';
import { sendSignupOtp, verifySignupOtp } from '../../interceptors/services';
import logo from '../../assets/Adam_tech_logo.png';

const Signup = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [password, setPassword] = useState('');
  const [otp, setOtp] = useState('');
  const [progress, setProgress] = useState(0);
  const [showModal, setShowModal] = useState(false);
  const [modalData, setModalData] = useState({ title: '', message: '', isSuccess: true });
  const [step, setStep] = useState(1);
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    gsap.fromTo('.card', { y: 100, opacity: 0 }, { y: 0, opacity: 1, duration: 1, ease: 'power3.out' });
    gsap.fromTo('.form-element', { y: 20, opacity: 0 }, { y: 0, opacity: 1, duration: 0.8, stagger: 0.15, ease: 'power3.out', delay: 0.2 });
  }, []);

  useEffect(() => {
    const totalFields = step === 1 ? 4 : 1;
    let filledFields = 0;
    if (name.trim()) filledFields++;
    if (email.trim()) filledFields++;
    if (password.trim()) filledFields++;
    if (phone.trim()) filledFields++;
    if (step === 2 && otp.trim()) filledFields++;
    setProgress((filledFields / totalFields) * 100);
  }, [name, email, password, phone, otp, step]);

  const handleSendOtp = async () => {
    setIsLoading(true);
    try {
      const userData = { name, email, password, phone };
      const response = await sendSignupOtp(userData);
      setModalData({ title: 'OTP Sent!', message: response.message, isSuccess: true });
      setShowModal(true);
      setStep(2);
    } catch (error) {
      setModalData({ title: 'Error', message: error.detail || error.message || 'Failed to send OTP.', isSuccess: false });
      setShowModal(true);
    } finally {
      setIsLoading(false);
    }
  };

  const handleVerifyOtp = async () => {
    setIsLoading(true);
    try {
      const verificationData = { email, otp };
      const response = await verifySignupOtp(verificationData);
      if (response.access_token) {
        localStorage.setItem('authToken', response.access_token);
        localStorage.setItem('tokenType', response.token_type);
        setModalData({ title: 'Success!', message: 'Account verified successfully! Redirecting...', isSuccess: true });
        setShowModal(true);
        confetti({ particleCount: 100, spread: 70, origin: { y: 0.6 } });
        setTimeout(() => navigate('/dashboard'), 2000);
      } else {
        throw new Error('Verification response did not include an access token.');
      }
    } catch (error) {
      setModalData({ title: 'Error', message: error.detail || error.message || 'Invalid OTP or verification failed.', isSuccess: false });
      setShowModal(true);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (step === 1) {
      if (name && email && password && phone) {
        handleSendOtp();
      } else {
        setModalData({ title: 'Error', message: 'Please fill in all fields.', isSuccess: false });
        setShowModal(true);
      }
    } else if (step === 2) {
      if (otp) {
        handleVerifyOtp();
      } else {
        setModalData({ title: 'Error', message: 'Please enter the OTP.', isSuccess: false });
        setShowModal(true);
      }
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 flex flex-col justify-between relative">
      <Particles />
      <div className="container mx-auto max-w-md px-4 py-12 flex-grow flex items-center relative z-10">
        <div className="card w-full p-8 bg-white bg-opacity-10 backdrop-blur-lg border border-white border-opacity-10 rounded-2xl shadow-xl">
          <div className="flex justify-center mb-6">
            <img src={logo} alt="Adam Tech Logo" className="w-24 h-24 animate-[float_3s_ease-in-out_infinite]" />
          </div>
          <h2 className="text-3xl font-bold text-center text-white mb-2">Adam Tech</h2>
          <p className="text-center text-gray-300 mb-6 text-sm">Dental Coding Software</p>
          <div className="w-full bg-gray-700 bg-opacity-30 rounded-full h-1.5 mb-6">
            <div style={{ width: `${progress}%` }} className="bg-gradient-to-r from-yellow-400 to-yellow-500 h-1.5 rounded-full transition-all duration-500 ease-out" />
          </div>
          <form onSubmit={handleSubmit}>
            {step === 1 && (
              <>
                <div className="mb-5 form-element">
                  <label htmlFor="name" className="block text-sm font-medium text-gray-200 mb-1">Full Name</label>
                  <input
                    type="text"
                    id="name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    required
                    className="w-full rounded-lg border-none bg-white bg-opacity-10 text-white placeholder-gray-400 focus:ring-2 focus:ring-yellow-400 focus:ring-opacity-50 p-3 transition-all duration-300"
                    placeholder="John Doe"
                  />
                </div>
                <div className="mb-5 form-element">
                  <label htmlFor="email" className="block text-sm font-medium text-gray-200 mb-1">Email</label>
                  <input
                    type="email"
                    id="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                    className="w-full rounded-lg border-none bg-white bg-opacity-10 text-white placeholder-gray-400 focus:ring-2 focus:ring-yellow-400 focus:ring-opacity-50 p-3 transition-all duration-300"
                    placeholder="you@example.com"
                  />
                </div>
                <div className="mb-5 form-element">
                  <label htmlFor="password" className="block text-sm font-medium text-gray-200 mb-1">Password</label>
                  <input
                    type="password"
                    id="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    className="w-full rounded-lg border-none bg-white bg-opacity-10 text-white placeholder-gray-400 focus:ring-2 focus:ring-yellow-400 focus:ring-opacity-50 p-3 transition-all duration-300"
                    placeholder="Choose a strong password"
                  />
                </div>
                <div className="mb-5 form-element">
                  <label htmlFor="phone" className="block text-sm font-medium text-gray-200 mb-1">Phone Number</label>
                  <input
                    type="tel"
                    id="phone"
                    value={phone}
                    onChange={(e) => setPhone(e.target.value)}
                    required
                    className="w-full rounded-lg border-none bg-white bg-opacity-10 text-white placeholder-gray-400 focus:ring-2 focus:ring-yellow-400 focus:ring-opacity-50 p-3 transition-all duration-300"
                    placeholder="+1 123-456-7890"
                  />
                </div>
                <button
                  type="submit"
                  disabled={isLoading}
                  className="w-full bg-gradient-to-r from-yellow-400 to-yellow-500 text-gray-900 font-semibold py-3 rounded-lg hover:from-yellow-500 hover:to-yellow-600 transition-all duration-300 shadow-md disabled:opacity-50"
                >
                  {isLoading ? 'Sending...' : 'Send OTP'}
                </button>
              </>
            )}
            {step === 2 && (
              <>
                <div className="mb-6 form-element">
                  <label htmlFor="otp" className="block text-sm font-medium text-gray-200 mb-1">Enter OTP</label>
                  <input
                    type="text"
                    id="otp"
                    value={otp}
                    onChange={(e) => setOtp(e.target.value)}
                    required
                    className="w-full rounded-lg border-none bg-white bg-opacity-10 text-white placeholder-gray-400 focus:ring-2 focus:ring-yellow-400 focus:ring-opacity-50 p-3 transition-all duration-300"
                    placeholder="Enter 6-digit code"
                  />
                </div>
                <button
                  type="submit"
                  disabled={isLoading}
                  className="w-full bg-gradient-to-r from-yellow-400 to-yellow-500 text-gray-900 font-semibold py-3 rounded-lg hover:from-yellow-500 hover:to-yellow-600 transition-all duration-300 shadow-md disabled:opacity-50"
                >
                  {isLoading ? 'Verifying...' : 'Verify OTP & Sign Up'}
                </button>
              </>
            )}
          </form>
          <p className="mt-4 text-center text-sm text-gray-300">
            Already have an account?{' '}
            <Link to="/" className="text-yellow-400 hover:underline font-medium">Login</Link>
          </p>
        </div>
      </div>
      {showModal && (
        <SuccessModal title={modalData.title} message={modalData.message} isSuccess={modalData.isSuccess} onClose={() => setShowModal(false)} />
      )}
      <style>{`
        @keyframes float {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-10px); }
        }
      `}</style>
    </div>
  );
};

export default Signup;