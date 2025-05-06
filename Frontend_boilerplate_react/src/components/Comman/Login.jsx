import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { gsap } from 'gsap';
import Particles from '../Particles/Particles';
import SuccessModal from '../Modal/SuccessModal';
import { loginUser, sendResetOtp, verifyResetOtp } from '../../interceptors/services';
import { useAuth } from '../../context/AuthContext';
import logo from '../../assets/Adam_tech_logo.png';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [progress, setProgress] = useState(0);
  const [showModal, setShowModal] = useState(false);
  const [modalData, setModalData] = useState({ title: '', message: '', isSuccess: true });
  const [isLoading, setIsLoading] = useState(false);
  const { login } = useAuth();

  // Forgot password states
  const [showForgotPassword, setShowForgotPassword] = useState(false);
  const [resetEmail, setResetEmail] = useState('');
  const [resetOtp, setResetOtp] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [otpSent, setOtpSent] = useState(false);
  const [isResetting, setIsResetting] = useState(false);

  useEffect(() => {
    gsap.fromTo('.card', { y: 100, opacity: 0 }, { y: 0, opacity: 1, duration: 1, ease: 'power3.out' });
    gsap.fromTo('.form-element', { y: 20, opacity: 0 }, { y: 0, opacity: 1, duration: 0.8, stagger: 0.15, ease: 'power3.out', delay: 0.2 });
  }, []);

  useEffect(() => {
    const totalFields = 2;
    let filledFields = 0;
    if (email.trim()) filledFields++;
    if (password.trim()) filledFields++;
    setProgress((filledFields / totalFields) * 100);
  }, [email, password]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (email && password) {
      setIsLoading(true);
      try {
        const response = await loginUser({ email, password });
        if (response.access_token && response.name && response.email && response.role) {
          const userData = { 
            name: response.name,
            email: response.email,
            role: response.role,
            has_seen_tour: response.has_seen_tour || false
          };
          login(userData, response.access_token);
        } else {
          throw new Error(response.detail || 'Login response missing token or user details.');
        }
      } catch (error) {
        setModalData({ title: 'Login Failed', message: error.detail || error.message || 'Invalid credentials or server error.', isSuccess: false });
        setShowModal(true);
      } finally {
        setIsLoading(false);
      }
    } else {
      setModalData({ title: 'Error', message: 'Please fill in all fields.', isSuccess: false });
      setShowModal(true);
    }
  };

  const handleSendResetOtp = async (e) => {
    e.preventDefault();
    if (!resetEmail.trim()) {
      setModalData({ title: 'Error', message: 'Please enter your email address.', isSuccess: false });
      setShowModal(true);
      return;
    }

    setIsResetting(true);
    try {
      const response = await sendResetOtp({ email: resetEmail });
      setModalData({ title: 'Success', message: response.message || 'OTP sent successfully. Please check your email.', isSuccess: true });
      setShowModal(true);
      setOtpSent(true);
    } catch (error) {
      setModalData({ title: 'Error', message: error.detail || error.message || 'Failed to send OTP.', isSuccess: false });
      setShowModal(true);
    } finally {
      setIsResetting(false);
    }
  };

  const handleResetPassword = async (e) => {
    e.preventDefault();
    if (!resetOtp || !newPassword || !confirmPassword) {
      setModalData({ title: 'Error', message: 'Please fill in all fields.', isSuccess: false });
      setShowModal(true);
      return;
    }

    if (newPassword !== confirmPassword) {
      setModalData({ title: 'Error', message: 'Passwords do not match.', isSuccess: false });
      setShowModal(true);
      return;
    }

    setIsResetting(true);
    try {
      const response = await verifyResetOtp({
        email: resetEmail,
        otp: resetOtp,
        new_password: newPassword
      });
      setModalData({ title: 'Success', message: response.message || 'Password reset successful. Please login with your new password.', isSuccess: true });
      setShowModal(true);
      // Reset states and show login form
      setShowForgotPassword(false);
      setResetEmail('');
      setResetOtp('');
      setNewPassword('');
      setConfirmPassword('');
      setOtpSent(false);
    } catch (error) {
      setModalData({ title: 'Error', message: error.detail || error.message || 'Failed to reset password.', isSuccess: false });
      setShowModal(true);
    } finally {
      setIsResetting(false);
    }
  };

  return (
    <>
      <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 flex flex-col justify-between relative">
        <Particles />
        <div className="container mx-auto max-w-md px-4 py-12 flex-grow flex items-center relative z-10">
          <div className="card w-full p-8 bg-white bg-opacity-10 backdrop-blur-lg border border-white border-opacity-10 rounded-2xl shadow-xl">
            <div className="flex justify-center mb-6">
              <img src={logo} alt="Adam Tech Logo" className="w-24 h-24 animate-[float_3s_ease-in-out_infinite]" />
            </div>
            <h2 className="text-3xl font-bold text-center text-white mb-2">Adam Tech</h2>
            <p className="text-center text-gray-300 mb-6 text-sm">Dental Coding Software</p>
            
            {!showForgotPassword ? (
              // Login Form
              <>
                <div className="w-full bg-gray-700 bg-opacity-30 rounded-full h-1.5 mb-6">
                  <div style={{ width: `${progress}%` }} className="bg-gradient-to-r from-yellow-400 to-yellow-500 h-1.5 rounded-full transition-all duration-500 ease-out" />
                </div>
                <form onSubmit={handleSubmit}>
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
                  <div className="mb-6 form-element">
                    <label htmlFor="password" className="block text-sm font-medium text-gray-200 mb-1">Password</label>
                    <input
                      type="password"
                      id="password"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      required
                      className="w-full rounded-lg border-none bg-white bg-opacity-10 text-white placeholder-gray-400 focus:ring-2 focus:ring-yellow-400 focus:ring-opacity-50 p-3 transition-all duration-300"
                      placeholder="••••••••"
                    />
                  </div>
                  <button
                    type="submit"
                    disabled={isLoading}
                    className="w-full bg-gradient-to-r from-yellow-400 to-yellow-500 text-gray-900 font-semibold py-3 rounded-lg hover:from-yellow-500 hover:to-yellow-600 transition-all duration-300 shadow-md disabled:opacity-50"
                  >
                    {isLoading ? 'Logging In...' : 'Login'}
                  </button>
                </form>
                <div className="mt-4 text-center space-y-2">
                  <button
                    onClick={() => setShowForgotPassword(true)}
                    className="text-yellow-400 hover:underline text-sm font-medium"
                  >
                    Forgot Password?
                  </button>
                  <p className="text-sm text-gray-300">
                    Don&apos;t have an account?{' '}
                    <Link to="/signup" className="text-yellow-400 hover:underline font-medium">Sign Up</Link>
                  </p>
                </div>
              </>
            ) : (
              // Forgot Password Form
              <form onSubmit={otpSent ? handleResetPassword : handleSendResetOtp} className="space-y-4">
                {!otpSent ? (
                  // Email Input for OTP
                  <div className="form-element">
                    <label htmlFor="resetEmail" className="block text-sm font-medium text-gray-200 mb-1">Email</label>
                    <input
                      type="email"
                      id="resetEmail"
                      value={resetEmail}
                      onChange={(e) => setResetEmail(e.target.value)}
                      required
                      className="w-full rounded-lg border-none bg-white bg-opacity-10 text-white placeholder-gray-400 focus:ring-2 focus:ring-yellow-400 focus:ring-opacity-50 p-3 transition-all duration-300"
                      placeholder="Enter your email"
                    />
                  </div>
                ) : (
                  // OTP and New Password Fields
                  <>
                    <div className="form-element">
                      <label htmlFor="otp" className="block text-sm font-medium text-gray-200 mb-1">OTP</label>
                      <input
                        type="text"
                        id="otp"
                        value={resetOtp}
                        onChange={(e) => setResetOtp(e.target.value)}
                        required
                        className="w-full rounded-lg border-none bg-white bg-opacity-10 text-white placeholder-gray-400 focus:ring-2 focus:ring-yellow-400 focus:ring-opacity-50 p-3 transition-all duration-300"
                        placeholder="Enter OTP"
                      />
                    </div>
                    <div className="form-element">
                      <label htmlFor="newPassword" className="block text-sm font-medium text-gray-200 mb-1">New Password</label>
                      <input
                        type="password"
                        id="newPassword"
                        value={newPassword}
                        onChange={(e) => setNewPassword(e.target.value)}
                        required
                        className="w-full rounded-lg border-none bg-white bg-opacity-10 text-white placeholder-gray-400 focus:ring-2 focus:ring-yellow-400 focus:ring-opacity-50 p-3 transition-all duration-300"
                        placeholder="Enter new password"
                      />
                    </div>
                    <div className="form-element">
                      <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-200 mb-1">Confirm Password</label>
                      <input
                        type="password"
                        id="confirmPassword"
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
                        required
                        className="w-full rounded-lg border-none bg-white bg-opacity-10 text-white placeholder-gray-400 focus:ring-2 focus:ring-yellow-400 focus:ring-opacity-50 p-3 transition-all duration-300"
                        placeholder="Confirm new password"
                      />
                    </div>
                  </>
                )}
                <button
                  type="submit"
                  disabled={isResetting}
                  className="w-full bg-gradient-to-r from-yellow-400 to-yellow-500 text-gray-900 font-semibold py-3 rounded-lg hover:from-yellow-500 hover:to-yellow-600 transition-all duration-300 shadow-md disabled:opacity-50"
                >
                  {isResetting ? 'Processing...' : (otpSent ? 'Reset Password' : 'Send OTP')}
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setShowForgotPassword(false);
                    setResetEmail('');
                    setResetOtp('');
                    setNewPassword('');
                    setConfirmPassword('');
                    setOtpSent(false);
                  }}
                  className="w-full mt-2 bg-transparent border border-yellow-400 text-yellow-400 font-semibold py-3 rounded-lg hover:bg-yellow-400 hover:text-gray-900 transition-all duration-300"
                >
                  Back to Login
                </button>
              </form>
            )}
          </div>
        </div>
      </div>
      {showModal && <SuccessModal title={modalData.title} message={modalData.message} isSuccess={modalData.isSuccess} onClose={() => setShowModal(false)} />}
      <style>{`
        @keyframes float {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-10px); }
        }
      `}</style>
    </>
  );
};

export default Login;