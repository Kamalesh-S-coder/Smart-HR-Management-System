import { useState } from 'react';
import { apiClient } from '../../api/client';
import { useNavigate } from 'react-router-dom';

export default function Login() {
    const navigate = useNavigate();
    const [isOtpMode, setIsOtpMode] = useState(false);
    const [identifier, setIdentifier] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const getDeviceData = () => ({
        device_os: navigator.platform || "Unknown OS",
        browser: navigator.userAgent.includes("Chrome") ? "Chrome" : "Other Browser"
    });

    const handlePasswordLogin = async (e) => {
        e.preventDefault();
        setError('');
        try {
            const { device_os, browser } = getDeviceData();
            
            const response = await apiClient.post('/auth/login', {
                identifier,
                password,
                device_os,
                browser
            });
            
            // --- THE FIX IS HERE ---
            localStorage.setItem('access_token', response.data.access_token);
            localStorage.setItem('user_role', response.data.role);
            localStorage.setItem('currentUser', identifier); // Passing the ID to the portal
            
            // Smart Routing
            if (response.data.role === 'Admin') {
                navigate('/admin');
            } else {
                navigate('/employee/portal');
            }

        } catch (err) {
            setError(err.response?.data?.detail || "Login failed");
        }
    };

    const handleOtpRequest = async (e) => {
        e.preventDefault();
        setError('');
        try {
            await apiClient.post('/auth/otp/request', { phone_or_email: identifier });
            alert("OTP Sent! Check the backend terminal for the code.");
        } catch (err) {
            setError("Failed to send OTP");
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50">
            <div className="max-w-md w-full bg-white p-8 rounded-lg shadow-md border border-gray-100">
                <h2 className="text-2xl font-bold text-center text-gray-800 mb-6">Smart HR Portal</h2>
                
                {error && <div className="mb-4 p-3 bg-red-100 text-red-700 rounded text-sm">{error}</div>}

                <div className="flex mb-6 border-b">
                    <button 
                        className={`flex-1 py-2 font-medium ${!isOtpMode ? 'border-b-2 border-blue-600 text-blue-600' : 'text-gray-400'}`}
                        onClick={() => setIsOtpMode(false)}
                    >
                        Password
                    </button>
                    <button 
                        className={`flex-1 py-2 font-medium ${isOtpMode ? 'border-b-2 border-blue-600 text-blue-600' : 'text-gray-400'}`}
                        onClick={() => setIsOtpMode(true)}
                    >
                        OTP Access
                    </button>
                </div>

                {!isOtpMode ? (
                    <form onSubmit={handlePasswordLogin} className="space-y-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Email or Employee ID</label>
                            <input 
                                type="text" 
                                required
                                className="mt-1 w-full p-2 border rounded focus:ring-blue-500 focus:border-blue-500"
                                value={identifier}
                                onChange={(e) => setIdentifier(e.target.value)}
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Password</label>
                            <input 
                                type="password" 
                                required
                                className="mt-1 w-full p-2 border rounded focus:ring-blue-500 focus:border-blue-500"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                            />
                        </div>
                        <button type="submit" className="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700 transition">
                            Secure Login
                        </button>
                    </form>
                ) : (
                    <form onSubmit={handleOtpRequest} className="space-y-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Registered Phone or Email</label>
                            <input 
                                type="text" 
                                required
                                className="mt-1 w-full p-2 border rounded focus:ring-blue-500 focus:border-blue-500"
                                value={identifier}
                                onChange={(e) => setIdentifier(e.target.value)}
                            />
                        </div>
                        <button type="submit" className="w-full bg-gray-800 text-white p-2 rounded hover:bg-gray-900 transition">
                            Request Code
                        </button>
                    </form>
                )}
            </div>
        </div>
    );
}