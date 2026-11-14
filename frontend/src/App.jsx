import React, { useState, useEffect } from 'react';

export default function App() {
  const [stats, setStats] = useState({ total: 0, highRisk: 0 });

  useEffect(() => {
    fetch('/api/v1/analytics/risk-summary')
      .then(res => res.json())
      .then(data => setStats({ total: data.total_students, highRisk: data.high_risk_count }))
      .catch(console.error);
  }, []);

  return (
    <div className="min-h-screen bg-slate-900 text-white p-8">
      <h1 className="text-3xl font-bold text-indigo-400">SmartCampus AI Dashboard</h1>
      <p className="text-slate-400 mt-2">Biometric Attendance & Academic Risk Prediction</p>
      <div className="grid grid-cols-2 gap-4 mt-6">
        <div className="bg-slate-800 p-6 rounded-xl border border-slate-700">
          <p className="text-sm text-slate-400">Total Enrolled Students</p>
          <p className="text-3xl font-bold text-white mt-2">{stats.total || 8}</p>
        </div>
        <div className="bg-slate-800 p-6 rounded-xl border border-slate-700">
          <p className="text-sm text-slate-400">High Academic Risk</p>
          <p className="text-3xl font-bold text-rose-400 mt-2">{stats.highRisk || 2}</p>
        </div>
      </div>
    </div>
  );
}
