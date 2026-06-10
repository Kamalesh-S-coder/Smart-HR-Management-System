import { useState, useEffect } from 'react';
import { apiClient } from '../../api/client';

export default function TimeClock() {
    const [employeeId, setEmployeeId] = useState('');
    const [workMode, setWorkMode] = useState('OFFICE');
    const [status, setStatus] = useState({ type: '', message: '' });
    const [currentTime, setCurrentTime] = useState(new Date());

    // Live Clock Effect
    useEffect(() => {
        const timer = setInterval(() => setCurrentTime(new Date()), 1000);
        return () => clearInterval(timer);
    }, []);

    const handlePunch = async (e) => {
        e.preventDefault();
        setStatus({ type: 'loading', message: 'Recording punch...' });
        
        try {
            const response = await apiClient.post('/attendance/clock-in', {
                employee_id: employeeId.toUpperCase(),
                work_mode: workMode
            });
            
            setStatus({ type: 'success', message: `Success! Punch recorded at ${currentTime.toLocaleTimeString()}` });
            setEmployeeId(''); // Clear the input for the next person
            
            // Clear the success message after 3 seconds
            setTimeout(() => setStatus({ type: '', message: '' }), 3000);
        } catch (err) {
            const msg = err.response?.data?.detail || "Punch failed. Check ID.";
            setStatus({ type: 'error', message: msg });
        }
    };

    return (
        <div className="min-h-screen bg-slate-900 flex items-center justify-center p-4">
            <div className="bg-white rounded-2xl shadow-2xl w-full max-w-md overflow-hidden">
                
                {/* Header / Digital Clock */}
                <div className="bg-blue-600 p-8 text-center text-white">
                    <h2 className="text-blue-200 font-bold tracking-widest uppercase text-sm mb-2">Smart HR Terminal</h2>
                    <div className="text-5xl font-black tracking-tight">
                        {currentTime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </div>
                    <div className="text-blue-100 mt-2 font-medium">
                        {currentTime.toLocaleDateString([], { weekday: 'long', month: 'long', day: 'numeric' })}
                    </div>
                </div>

                {/* Form Body */}
                <div className="p-8">
                    <form onSubmit={handlePunch} className="space-y-6">
                        <div>
                            <label className="block text-sm font-bold text-slate-700 mb-2">Scan or Enter Employee ID</label>
                            <input 
                                type="text" 
                                placeholder="EMP-XXXXXX"
                                className="w-full p-4 border-2 border-slate-200 rounded-xl text-center text-2xl font-mono uppercase focus:border-blue-500 focus:ring-0 transition-colors"
                                value={employeeId}
                                onChange={(e) => setEmployeeId(e.target.value)}
                                required 
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-bold text-slate-700 mb-2">Work Location</label>
                            <div className="grid grid-cols-2 gap-4">
                                <button 
                                    type="button"
                                    onClick={() => setWorkMode('OFFICE')}
                                    className={`p-3 rounded-lg font-bold border-2 transition-all ${workMode === 'OFFICE' ? 'bg-blue-50 border-blue-600 text-blue-700' : 'border-slate-100 text-slate-500 hover:border-slate-200'}`}
                                >
                                    🏢 Office
                                </button>
                                <button 
                                    type="button"
                                    onClick={() => setWorkMode('REMOTE')}
                                    className={`p-3 rounded-lg font-bold border-2 transition-all ${workMode === 'REMOTE' ? 'bg-blue-50 border-blue-600 text-blue-700' : 'border-slate-100 text-slate-500 hover:border-slate-200'}`}
                                >
                                    🏠 Remote
                                </button>
                            </div>
                        </div>

                        <button 
                            type="submit" 
                            disabled={status.type === 'loading'}
                            className="w-full bg-emerald-500 hover:bg-emerald-600 text-white font-black text-xl p-4 rounded-xl shadow-lg shadow-emerald-200 transition-all active:scale-95"
                        >
                            CLOCK IN
                        </button>
                    </form>

                    {/* Status Alerts */}
                    <div className="mt-6 h-12">
                        {status.message && (
                            <div className={`p-3 rounded-lg text-center font-bold text-sm ${status.type === 'success' ? 'bg-emerald-100 text-emerald-700' : status.type === 'error' ? 'bg-red-100 text-red-700' : 'bg-slate-100 text-slate-500'}`}>
                                {status.message}
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}
