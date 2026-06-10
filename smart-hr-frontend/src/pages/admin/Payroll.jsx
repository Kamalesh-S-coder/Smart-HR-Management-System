import { useState, useEffect } from 'react';
import { apiClient } from '../../api/client';

export default function Payroll() {
    const [employees, setEmployees] = useState([]);
    const [loading, setLoading] = useState(true);
    const [month, setMonth] = useState('2026-06');
    
    // We are now tracking hourly rates instead of flat salaries
    const [hourlyRates, setHourlyRates] = useState({});
    
    const [result, setResult] = useState(null);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchDirectory = async () => {
            try {
                const response = await apiClient.get('/employee/all');
                setEmployees(response.data);
                
                // Initialize default hourly rates
                const initialRates = {};
                response.data.forEach(emp => {
                    initialRates[emp.employee_id] = emp.role_name === 'Admin' ? 50 : 25;
                });
                setHourlyRates(initialRates);

            } catch (err) {
                setError("Failed to load employee directory.");
            } finally {
                setLoading(false);
            }
        };
        fetchDirectory();
    }, []);

    const handleRateChange = (employeeId, value) => {
        setHourlyRates(prev => ({
            ...prev,
            [employeeId]: value
        }));
    };

    const handleExecute = async (employeeId) => {
        setError('');
        setResult(null);
        
        const adminId = localStorage.getItem('currentUser');
        if (!adminId) {
            setError("You are not logged in!");
            return;
        }

        const specificRate = parseFloat(hourlyRates[employeeId]) || 0;

        try {
            const response = await apiClient.post('/payroll/execute', {
                target_user_id: employeeId,
                month: month,
                hourly_rate: specificRate, // Sending the hourly rate to our new backend engine!
                admin_id: adminId 
            });
            setResult(response.data);
        } catch (err) {
            const msg = err.response?.data?.detail || "Execution failed.";
            setError(typeof msg === 'object' ? JSON.stringify(msg) : msg);
        }
    };

    return (
        <div className="min-h-screen bg-slate-100 p-8">
            <div className="max-w-6xl mx-auto space-y-6">
                
                <div className="bg-white p-6 rounded shadow flex justify-between items-center">
                    <h1 className="text-3xl font-bold text-slate-800">Automated Payroll Engine</h1>
                    <div className="flex space-x-4">
                        <div>
                            <label className="block text-xs font-bold text-slate-500 uppercase">Billing Month</label>
                            <input type="month" className="p-2 border rounded" value={month} onChange={(e) => setMonth(e.target.value)} />
                        </div>
                    </div>
                </div>

                {error && <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded font-bold">{error}</div>}
                {result && (
                    <div className="bg-emerald-100 border border-emerald-400 text-emerald-800 px-4 py-3 rounded flex justify-between items-center">
                        <span className="font-bold">{result.message}</span>
                        <span className="text-2xl font-black">${result.net_pay}</span>
                    </div>
                )}

                <div className="bg-white rounded shadow overflow-hidden">
                    {loading ? (
                        <div className="p-8 text-center text-slate-500 font-bold">Loading Directory...</div>
                    ) : (
                        <table className="w-full text-left border-collapse">
                            <thead>
                                <tr className="bg-slate-800 text-white">
                                    <th className="p-4 font-bold">Employee ID</th>
                                    <th className="p-4 font-bold">System Role</th>
                                    <th className="p-4 font-bold">Hourly Rate ($)</th>
                                    <th className="p-4 text-right font-bold">Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                {employees.map((emp) => (
                                    <tr key={emp.id} className="border-b hover:bg-slate-50">
                                        <td className="p-4 font-mono text-sm text-slate-600">{emp.employee_id}</td>
                                        <td className="p-4">
                                            <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs font-bold">{emp.role_name}</span>
                                        </td>
                                        <td className="p-4">
                                            <input 
                                                type="number" 
                                                className="p-2 border rounded w-32" 
                                                value={hourlyRates[emp.employee_id] || ''} 
                                                onChange={(e) => handleRateChange(emp.employee_id, e.target.value)}
                                            />
                                        </td>
                                        <td className="p-4 text-right">
                                            <button 
                                                onClick={() => handleExecute(emp.employee_id)}
                                                className="bg-emerald-600 hover:bg-emerald-700 text-white px-4 py-2 rounded font-bold transition-colors"
                                            >
                                                Execute Payroll
                                            </button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    )}
                </div>
            </div>
        </div>
    );
}