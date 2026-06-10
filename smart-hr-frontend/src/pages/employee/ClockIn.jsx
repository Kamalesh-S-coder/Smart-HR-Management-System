import { useState } from 'react';
import { apiClient } from '../../api/client';
import { useNavigate } from 'react-router-dom';

export default function ClockIn() {
    const [message, setMessage] = useState('');
    const [isAnomaly, setIsAnomaly] = useState(false);
    const navigate = useNavigate();

    const handleLogout = () => {
        localStorage.clear();
        navigate('/login');
    };

    const sendPunch = async (mode, coords = null) => {
        setMessage('Processing punch...');
        try {
            const response = await apiClient.post('/attendance/clock-in', {
                work_mode: mode,
                // THE FIX: If coords is null, send an empty string
                gps_location: coords || "" 
            });
            
            setMessage(response.data.message);
            setIsAnomaly(response.data.anomaly);
        } catch (err) {
            let errorDetail = err.response?.data?.detail;
            if (typeof errorDetail !== 'string') {
                errorDetail = JSON.stringify(errorDetail);
            }
            setMessage(errorDetail || "Punch failed. Check backend terminal.");
            setIsAnomaly(false);
        }
    };

    const handleOfficePunch = () => {
        sendPunch("OFFICE");
    };

    const handleRemotePunch = () => {
        if (!navigator.geolocation) {
            setMessage("Geolocation is not supported by your browser.");
            return;
        }

        setMessage("Locating satellite coordinates...");
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const coords = `${position.coords.latitude}, ${position.coords.longitude}`;
                sendPunch("REMOTE", coords);
            },
            (error) => {
                setMessage("ERROR: You must allow GPS access to clock in remotely.");
            }
        );
    };

    const handleClockOut = async () => {
        try {
            const response = await apiClient.post('/attendance/clock-out');
            setMessage(response.data.message);
        } catch (err) {
            let errorDetail = err.response?.data?.detail;
            if (typeof errorDetail !== 'string') {
                errorDetail = JSON.stringify(errorDetail);
            }
            setMessage(errorDetail || "Clock out failed.");
        }
    };

    return (
        <div className="min-h-screen bg-gray-100 p-8">
            <div className="max-w-2xl mx-auto bg-white rounded-xl shadow-lg p-8">
                <div className="flex justify-between items-center border-b pb-4 mb-6">
                    <h1 className="text-3xl font-bold text-gray-800">Employee Terminal</h1>
                    <button onClick={handleLogout} className="text-red-600 font-semibold hover:underline">Logout</button>
                </div>

                {message && (
                    <div className={`p-4 mb-6 rounded text-white font-medium ${isAnomaly ? 'bg-orange-500' : 'bg-slate-800'}`}>
                        {message}
                        {isAnomaly && " (WARNING: IP Anomaly Flagged by System)"}
                    </div>
                )}

                <div className="grid grid-cols-2 gap-6 mb-8">
                    <button 
                        onClick={handleOfficePunch}
                        className="p-6 bg-blue-50 border border-blue-200 rounded-lg hover:bg-blue-100 transition shadow-sm text-center"
                    >
                        <span className="block text-2xl mb-2">🏢</span>
                        <span className="font-bold text-blue-900">Office Clock-In</span>
                        <span className="block text-sm text-blue-600 mt-1">Verifies Local IP</span>
                    </button>

                    <button 
                        onClick={handleRemotePunch}
                        className="p-6 bg-emerald-50 border border-emerald-200 rounded-lg hover:bg-emerald-100 transition shadow-sm text-center"
                    >
                        <span className="block text-2xl mb-2">🌍</span>
                        <span className="font-bold text-emerald-900">Remote Clock-In</span>
                        <span className="block text-sm text-emerald-600 mt-1">Requires GPS Lock</span>
                    </button>
                </div>

                <button 
                    onClick={handleClockOut}
                    className="w-full py-4 bg-red-600 text-white rounded-lg font-bold text-lg hover:bg-red-700 transition shadow-md"
                >
                    End Shift (Clock Out)
                </button>
            </div>
        </div>
    );
}