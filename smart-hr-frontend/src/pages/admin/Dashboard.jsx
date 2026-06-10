import { Link } from 'react-router-dom';

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-slate-100 p-10">
      <div className="max-w-4xl mx-auto">
        <header className="mb-10">
          <h1 className="text-4xl font-black text-slate-900">Admin Control Center</h1>
          <p className="text-slate-500 font-bold mt-2">Welcome to the central management hub.</p>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Payroll Card */}
          <Link 
            to="/admin/payroll" 
            className="group bg-white p-8 rounded-2xl shadow-lg border-b-4 border-blue-600 hover:bg-blue-50 transition-all active:scale-95 block"
          >
            <div className="text-4xl mb-4">💰</div>
            <h2 className="text-2xl font-black text-slate-800">Payroll Engine</h2>
            <p className="text-slate-500 mt-2 font-medium">Execute payments and view audit logs.</p>
          </Link>

          {/* Leave Card */}
          <Link 
            to="/admin/leaves" 
            className="group bg-white p-8 rounded-2xl shadow-lg border-b-4 border-purple-600 hover:bg-purple-50 transition-all active:scale-95 block"
          >
            <div className="text-4xl mb-4">🌴</div>
            <h2 className="text-2xl font-black text-slate-800">Leave Management</h2>
            <p className="text-slate-500 mt-2 font-medium">Review and approve PTO requests.</p>
          </Link>
        </div>
      </div>
    </div>
  );
}