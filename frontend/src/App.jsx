import { useState } from 'react'
import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import Simulate from './pages/Simulate'
import Profile from './pages/Profile'

// Admin pages
import AdminDashboard from './pages/admin/AdminDashboard'
import FundingParties from './pages/admin/FundingParties'

function App() {
  return (
    <div className="min-h-screen bg-gray-50 text-gray-900 font-sans selection:bg-teal-100 selection:text-teal-900">
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        
        {/* User Routes */}
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/simulate" element={<Simulate />} />
        <Route path="/profile" element={<Profile />} />

        {/* Admin Routes */}
        <Route path="/admin/dashboard" element={<AdminDashboard />} />
        <Route path="/admin/funding-parties" element={<FundingParties />} />
      </Routes>
    </div>
  )
}

export default App
