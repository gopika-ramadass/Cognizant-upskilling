import React from 'react';

export default function Header({ siteName, enrolledCount }) {
    return (
        <header className="site-header">
            <h2 className="logo">{siteName || "Student Portal"}</h2>
            <nav className="nav-menu">
                <ul>
                    <li><a href="#" className="active">Home</a></li>
                    <li><a href="#">Courses</a></li>
                    <li><a href="#">Profile</a></li>
                    <li><a href="#">Grades</a></li>
                </ul>
            </nav>
            <div className="enroll-badge">
                <span>📚 Enrolled: <strong>{enrolledCount}</strong></span>
            </div>
        </header>
    );
}
