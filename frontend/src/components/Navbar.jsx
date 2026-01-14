import React, { useState, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import axios from 'axios';

const Navbar = () => {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    // Check auth status
    const checkAuth = async () => {
      try {
        const res = await axios.get('/api/auth/status');
        if (res.data.is_authenticated) {
          setUser(res.data.user);
        } else {
          setUser(null);
        }
      } catch (err) {
        setUser(null);
      }
    };
    checkAuth();
  }, [location.pathname]);

  const handleLogout = async () => {
    try {
      await axios.post('/api/logout');
      setUser(null);
      navigate('/login');
    } catch (err) {
      console.error("Logout failed", err);
    }
  };

  return (
    <nav className="bg-white/80 backdrop-blur-md border-b border-gray-100 dark:bg-gray-900/80 dark:border-gray-800 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          <div className="flex-shrink-0 flex items-center gap-2">
            <Link to="/" className="text-2xl font-bold bg-gradient-to-r from-teal-600 to-emerald-500 bg-clip-text text-transparent">
              🏦 LoanLess
            </Link>
          </div>
          
          <div className="hidden md:flex items-center space-x-8">
            <Link to="/" className="text-gray-600 hover:text-teal-600 dark:text-gray-300 dark:hover:text-teal-400 font-medium transition-colors">Home</Link>
            
            {user ? (
              <>
                {user.is_admin ? (
                   <Link to="/admin/dashboard" className="text-gray-600 hover:text-teal-600 dark:text-gray-300 font-medium">Admin Portal</Link>
                ) : (
                   <Link to="/dashboard" className="text-gray-600 hover:text-teal-600 dark:text-gray-300 font-medium">Dashboard</Link>
                )}
                <div className="flex items-center gap-4">
                  <span className="text-sm text-gray-500">Hi, {user.username}</span>
                  <button 
                    onClick={handleLogout}
                    className="bg-gray-100 hover:bg-gray-200 text-gray-700 px-4 py-2 rounded-full text-sm font-medium transition-colors"
                  >
                    Logout
                  </button>
                </div>
              </>
            ) : (
              <>
                <Link to="/login" className="text-gray-600 hover:text-teal-600 dark:text-gray-300 font-medium">Login</Link>
                <Link to="/register" className="bg-teal-600 hover:bg-teal-700 text-white px-5 py-2.5 rounded-full font-medium shadow-lg shadow-teal-500/30 transition-all hover:-translate-y-0.5">
                  Get Started
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
