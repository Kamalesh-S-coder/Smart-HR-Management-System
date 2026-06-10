import { Navigate } from 'react-router-dom';

export default function RoleGuard({ children, allowedRole }) {
    const token = localStorage.getItem('access_token');
    const userRole = localStorage.getItem('user_role');

    // 1. Not logged in at all? Kick to login.
    if (!token) {
        return <Navigate to="/login" replace />;
    }

    // 2. Logged in, but wrong role? (Super Admins can see everything)
    if (allowedRole && userRole !== allowedRole && userRole !== 'Super Admin') {
        alert("Access Denied: You do not have clearance for this dashboard.");
        return <Navigate to="/login" replace />;
    }

    // 3. Clear to proceed. Render the page.
    return children;
}