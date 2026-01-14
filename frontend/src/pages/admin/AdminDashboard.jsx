import React from 'react';
import { Link } from 'react-router-dom';

const AdminDashboard = () => {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Admin Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Link to="/admin/funding-parties" className="p-6 bg-white rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-all group">
          <h2 className="text-xl font-bold text-gray-900 group-hover:text-teal-600 mb-2">Funding Parties</h2>
          <p className="text-gray-500">Manage investors and funding inquiries.</p>
        </Link>
        <div className="p-6 bg-white rounded-xl shadow-sm border border-gray-100">
          <h2 className="text-xl font-bold text-gray-900 mb-2">Loans Management</h2>
          <p className="text-gray-500">Review and approve loan applications (Feature migrated soon).</p>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;
