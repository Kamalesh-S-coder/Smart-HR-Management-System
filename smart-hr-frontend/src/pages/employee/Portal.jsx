import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiClient } from '../../api/client';

export default function Portal() {
    const [employeeId, setEmployeeId] = useState('');
    const [status, setStatus] = useState({ message: '', type: '' });
    const [leaveHistory, setLeaveHistory] = useState([]);
    const navigate = useNavigate();

    // 1. Authentication Check
    useEffect(() => {
        const token = localStorage.getItem('access_token');
        const id = localStorage.getItem('currentUser');
        
        if (!token) {
            navigate('/'); 
        } else {
            setEmployeeId(id || 'Unknown Employee');
        }
    }, [navigate]);

    // 2. Fetch Leave History
    useEffect(() => {
        const fetchHistory = async () => {
            if (!employeeId) return;
            try {
                const response = await apiClient.get(`/leave/history/${employeeId}`);
                setLeaveHistory(response.data);
            } catch (err) {
                console.error("Failed to load history");
            }
        };
        fetchHistory();
    }, [employeeId]);

    // 3. Action Handler
    const handleAction = async (endpoint, payload) => {
        setStatus({ message: 'Processing...', type: 'loading' });
        try {
            const response = await apiClient.post(endpoint, payload);
            setStatus({ message: response.data.message, type: 'success' });
            setTimeout(() => setStatus({ message: '', type: '' }), 4000);
        } catch (err) {
            setStatus({ message: err.response?.data?.detail || "Action failed.", type: 'error' });
            setTimeout(() => setStatus({ message: '', type: '' }), 6000);
        }
    };

    const handleClockIn = () => handleAction('/attendance/clock-in', { employee_id: employeeId, work_mode: 'OFFICE' });
    const handleClockOut = () => handleAction('/attendance/clock-out', { employee_id: employeeId, work_mode: 'OFFICE' });
    const handlePTO = () => handleAction('/leave/request', { employee_id: employeeId, leave_type: 'PTO' });

    const handleLogout = () => {
        localStorage.removeItem('currentUser');
        localStorage.removeItem('access_token');
        localStorage.removeItem('user_role');
        navigate('/');
    };

    return (
        <div className="min-h-screen bg-slate-100 p-8">
            <div className="max-w-4xl mx-auto space-y-6">
                
                {/* Header */}
                <div className="bg-white p-6 rounded-xl shadow flex justify-between items-center">
                    <div>
                        <h1 className="text-2xl font-black text-slate-800">Employee Portal</h1>
                        <p className="text-slate-500 font-mono font-bold mt-1">Logged in as: <span className="text-blue-600">{employeeId}</span></p>
                    </div>
                    <button onClick={handleLogout} className="text-red-500 font-bold hover:bg-red-50 px-4 py-2 rounded transition-colors">
                        Logout
                    </button>
                </div>

                {/* Status Message */}
                {status.message && (
                    <div className={`p-4 rounded-lg font-bold text-center ${status.type === 'success' ? 'bg-emerald-100 text-emerald-800' : status.type === 'error' ? 'bg-red-100 text-red-800' : 'bg-blue-100 text-blue-800'}`}>
                        {status.message}
                    </div>
                )}

                {/* Actions Grid */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <button onClick={handleClockIn} className="bg-white hover:bg-blue-50 border-2 border-transparent hover:border-blue-200 p-6 rounded-xl shadow-lg transition-all active:scale-95 flex flex-col items-center justify-center group">
                        <span className="text-5xl mb-4">🏢</span>
                        <span className="text-xl font-black text-slate-700">Clock In</span>
                    </button>

                    <button onClick={handleClockOut} className="bg-white hover:bg-orange-50 border-2 border-transparent hover:border-orange-200 p-6 rounded-xl shadow-lg transition-all active:scale-95 flex flex-col items-center justify-center group">
                        <span className="text-5xl mb-4">🏃</span>
                        <span className="text-xl font-black text-slate-700">Clock Out</span>
                    </button>
                    
                    <button onClick={handlePTO} className="bg-white hover:bg-purple-50 border-2 border-transparent hover:border-purple-200 p-6 rounded-xl shadow-lg transition-all active:scale-95 flex flex-col items-center justify-center group">
                        <span className="text-5xl mb-4">🌴</span>
                        <span className="text-xl font-black text-slate-700">Request PTO</span>
                    </button>
                </div>

                {/* Leave History Table */}
                <div className="bg-white rounded-xl shadow p-6 mt-8">
                    <h2 className="text-xl font-black text-slate-800 mb-4">Leave Request History</h2>
                    <table className="w-full text-left">
                        <thead>
                            <tr className="text-slate-400 text-sm uppercase">
                                <th className="pb-3">Type</th>
                                <th className="pb-3">Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            {leaveHistory.length > 0 ? (
                                leaveHistory.map((req) => (
                                    <tr key={req.id} className="border-t">
                                        <td className="py-3 font-medium">{req.leave_type}</td>
                                        <td className="py-3">
                                            <span className={`px-2 py-1 rounded text-xs font-bold ${
                                                req.status === 'APPROVED' ? 'bg-green-100 text-green-700' :
                                                req.status === 'REJECTED' ? 'bg-red-100 text-red-700' :
                                                'bg-amber-100 text-amber-700'
                                            }`}>
                                                {req.status}
                                            </span>
                                        </td>
                                    </tr>
                                ))
                            ) : (
                                <tr>
                                    <td colSpan="2" className="py-4 text-center text-slate-400">No requests found.</td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>

            </div>
        </div>
    );
}