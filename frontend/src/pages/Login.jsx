import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const Login = () => {
  const [formData, setFormData] = useState({ username: '', password: '' });
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post('/api/login', formData);
      if (res.data.success) {
        if (res.data.user.is_admin) {
            navigate('/admin/dashboard');
        } else {
            navigate('/dashboard');
        }
        window.location.reload(); // Refresh to update Navbar auth state
      }
    } catch (err) {
      alert('Login failed: ' + (err.response?.data?.message || err.message));
    }
  };

  return (
    <div className="min-h-[80vh] flex items-center justify-center">
      <div className="bg-white p-8 rounded-2xl shadow-xl w-full max-w-md border border-gray-100">
        <h2 className="text-2xl font-bold mb-6 text-center">Welcome Back</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            type="text"
            placeholder="Username"
            className="w-full px-4 py-3 rounded-lg bg-gray-50 border border-gray-200 focus:ring-2 focus:ring-teal-500 outline-none"
            value={formData.username}
            onChange={(e) => setFormData({...formData, username: e.target.value})}
          />
          <input
            type="password"
            placeholder="Password"
            className="w-full px-4 py-3 rounded-lg bg-gray-50 border border-gray-200 focus:ring-2 focus:ring-teal-500 outline-none"
            value={formData.password}
            onChange={(e) => setFormData({...formData, password: e.target.value})}
          />
          <button type="submit" className="w-full bg-teal-600 text-white py-3 rounded-lg font-bold hover:bg-teal-700 transition-colors">
            Login
          </button>
        </form>
      </div>
    </div>
  );
};

export default Login;
