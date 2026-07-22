import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useSelector } from 'react-redux';

export default function Header({ siteName }) {
    const location = useLocation();
    const enrolledCourses = useSelector(state => state.enrollment.enrolledCourses);

    return (
        <header className="site-header">
            <h2 className="logo">
                <Link to="/" style={{ color: 'inherit', textDecoration: 'none' }}>
                    {siteName || "Student Portal"}
                </Link>
            </h2>
            <nav className="nav-menu">
                <ul>
                    <li>
                        <Link to="/" className={location.pathname === '/' ? 'active' : ''}>Home</Link>
                    </li>
                    <li>
                        <Link to="/courses" className={location.pathname.startsWith('/courses') ? 'active' : ''}>Courses</Link>
                    </li>
                    <li>
                        <Link to="/profile" className={location.pathname === '/profile' ? 'active' : ''}>Profile</Link>
                    </li>
                </ul>
            </nav>
            <div className="enroll-badge">
                <span>📚 Enrolled: <strong>{enrolledCourses.length}</strong></span>
            </div>
        </header>
    );
}
