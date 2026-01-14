import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

const Home = () => {
  const [fundingForm, setFundingForm] = useState({
    name: '',
    email: '',
    phone: '',
    capital_available: ''
  });
  const [fundingStatus, setFundingStatus] = useState('');

  const handleFundingSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('/api/funding-inquiry', fundingForm);
      setFundingStatus('Thank you! We will be in touch shortly.');
      setFundingForm({ name: '', email: '', phone: '', capital_available: '' });
    } catch (err) {
      setFundingStatus('Something went wrong. Please try again.');
    }
  };

  return (
    <div className="space-y-20 pb-20">
      {/* Hero Section */}
      <section className="relative overflow-hidden pt-16 pb-32 lg:pt-32">
        <div className="absolute top-0 left-1/2 -ml-[40rem] w-[80rem] h-[30rem] bg-gradient-to-r from-teal-200/20 to-emerald-200/20 rounded-full blur-3xl -z-10" />
        
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight text-gray-900 mb-8">
            Ethical Microloans. <br/>
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-teal-600 to-emerald-500">
              Zero Interest.
            </span>
          </h1>
          <p className="max-w-2xl mx-auto text-xl text-gray-600 mb-10 leading-relaxed">
            Empowering your financial future with transparent, fair, and accessible lending. 
            Only 2% commission fee. No hidden strings attached.
          </p>
          <div className="flex justify-center gap-4">
            <Link to="/register" className="px-8 py-4 bg-teal-600 text-white rounded-full font-bold text-lg shadow-xl shadow-teal-500/20 hover:bg-teal-700 hover:shadow-2xl hover:-translate-y-1 transition-all">
              Start Your Application
            </Link>
            <Link to="/login" className="px-8 py-4 bg-white text-gray-700 border border-gray-200 rounded-full font-bold text-lg hover:bg-gray-50 transition-all">
              Login
            </Link>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid md:grid-cols-3 gap-8">
          {[
            { title: "0% Interest", desc: "Keep more of your money. We only charge a small one-time fee.", icon: "💎" },
            { title: "Instant Decision", desc: "Our AI-powered engine processes your application in minutes.", icon: "⚡" },
            { title: "Secure & Private", desc: "Bank-grade encryption protects your data and documents.", icon: "🔒" },
          ].map((feature, i) => (
            <div key={i} className="p-8 rounded-3xl bg-white border border-gray-100 shadow-sm hover:shadow-md transition-shadow">
              <div className="text-4xl mb-4">{feature.icon}</div>
              <h3 className="text-xl font-bold mb-2">{feature.title}</h3>
              <p className="text-gray-500">{feature.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Funding / Investor Section (NEW) */}
      <section className="bg-gray-900 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid lg:grid-cols-2 gap-16 items-center">
            <div>
              <h2 className="text-4xl font-bold mb-6">Become a Funding Partner</h2>
              <p className="text-gray-400 text-lg mb-8">
                Join our mission to provide ethical financial services. We connect investors 
                with verified borrowers, offering a secure platform for social impact investing.
              </p>
              <ul className="space-y-4 mb-8">
                {['Verified borrower profiles', 'Transparent portfolio tracking', 'Direct social impact'].map(item => (
                  <li key={item} className="flex items-center gap-3">
                    <span className="w-6 h-6 rounded-full bg-teal-500/20 flex items-center justify-center text-teal-400">✓</span>
                    {item}
                  </li>
                ))}
              </ul>
            </div>

            <div className="bg-white/5 backdrop-blur-sm p-8 rounded-2xl border border-white/10">
              <h3 className="text-2xl font-bold mb-6">Inquire About Funding</h3>
              <form onSubmit={handleFundingSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-400 mb-1">Company / Name</label>
                  <input 
                    type="text" 
                    required
                    className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 text-white focus:ring-2 focus:ring-teal-500 outline-none"
                    value={fundingForm.name}
                    onChange={(e) => setFundingForm({...fundingForm, name: e.target.value})}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-400 mb-1">Email Address</label>
                  <input 
                    type="email" 
                    required
                    className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 text-white focus:ring-2 focus:ring-teal-500 outline-none"
                    value={fundingForm.email}
                    onChange={(e) => setFundingForm({...fundingForm, email: e.target.value})}
                  />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-400 mb-1">Phone</label>
                    <input 
                      type="tel" 
                      className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 text-white focus:ring-2 focus:ring-teal-500 outline-none"
                      value={fundingForm.phone}
                      onChange={(e) => setFundingForm({...fundingForm, phone: e.target.value})}
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-400 mb-1">Capital ($)</label>
                    <input 
                      type="number" 
                      className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 text-white focus:ring-2 focus:ring-teal-500 outline-none"
                      value={fundingForm.capital_available}
                      onChange={(e) => setFundingForm({...fundingForm, capital_available: e.target.value})}
                    />
                  </div>
                </div>
                <button type="submit" className="w-full bg-gradient-to-r from-teal-500 to-emerald-500 text-white font-bold py-3 rounded-lg hover:shadow-lg hover:from-teal-600 hover:to-emerald-600 transition-all">
                  Submit Interest
                </button>
                {fundingStatus && <p className="text-teal-400 text-center text-sm">{fundingStatus}</p>}
              </form>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
