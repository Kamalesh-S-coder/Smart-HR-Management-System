import { useState, useEffect } from 'react';
import { apiClient } from '../../api/client';

export default function Leaves() {
    const [requests, setRequests] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchLeaves = async () => {
            try {
                const response = await apiClient.get('/leave/all-pending');
                setRequests(response.data);
            } catch (err) {
                console.error("Failed to load leaves");
            } finally {
                setLoading(false);
            }
        };
        fetchLeaves();
    }, []);

    const handleApproval = async (id, status) => {
        try {
            await apiClient.post('/leave/update-status', { id, status });
            // Remove the approved/rejected item from the UI list
            setRequests(requests.filter(r => r.id !== id));
        } catch (err) {
            alert("Update failed");
        }
    };

    return (
        <div className="min-h-screen bg-slate-100 p-8">
            <h1 className="text-3xl font-black mb-6">Leave Management</h1>
            <div className="bg-white rounded shadow overflow-hidden">
                <table className="w-full text-left">
                    <thead className="bg-slate-800 text-white">
                        <tr>
                            <th className="p-4">Employee</th>
                            <th className="p-4">Type</th>
                            <th className="p-4">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {requests.map(req => (
                            <tr key={req.id} className="border-b">
                                <td className="p-4">{req.user.employee_id}</td>
                                <td className="p-4">{req.leave_type}</td>
                                <td className="p-4 space-x-2">
                                    <button onClick={() => handleApproval(req.id, 'APPROVED')} className="bg-green-600 text-white px-3 py-1 rounded">Approve</button>
                                    <button onClick={() => handleApproval(req.id, 'REJECTED')} className="bg-red-600 text-white px-3 py-1 rounded">Deny</button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}