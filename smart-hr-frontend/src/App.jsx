import { Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/auth/Login';
import Portal from './pages/employee/Portal';
import Dashboard from './pages/admin/Dashboard';
import Payroll from './pages/admin/Payroll';
import Leaves from './pages/admin/Leaves'; // <-- 1. ADDED THIS IMPORT

export default function App() {
  return (
    <Routes>
      {/* Root path goes to Login */}
      <Route path="/" element={<Login />} />
      
      {/* Employee Dashboard/Portal */}
      <Route path="/employee/portal" element={<Portal />} />
      
      {/* Admin Menu Hub */}
      <Route path="/admin" element={<Dashboard />} /> 
      
      {/* Admin Sub-features */}
      <Route path="/admin/payroll" element={<Payroll />} />
      <Route path="/admin/leaves" element={<Leaves />} /> {/* <-- 2. ADDED THIS ROUTE */}
      
      {/* Fallback Catch-all */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}