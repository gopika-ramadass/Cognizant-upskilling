import React from 'react';
import { Link } from 'react-router-dom';
import { useSelector } from 'react-redux';

export default function HomePage() {
    const enrolledCourses = useSelector(state => state.enrollment.enrolledCourses);

    return (
        <div className="homepage-container">
            <section id="hero">
                <h1>Welcome to the Student Portal</h1>
                <p>
                    Learn modern technologies, track your academic progress,
                    and explore new opportunities.
                </p>
                <Link to="/courses">
                    <button className="btn-primary">Explore Courses</button>
                </Link>
            </section>

            {/* Student Stats */}
            <section className="stats">
                <div className="stat-box">
                    <h3>{enrolledCourses.length}</h3>
                    <p>Courses Enrolled</p>
                </div>
                <div className="stat-box">
                    <h3>3.8</h3>
                    <p>GPA</p>
                </div>
                <div className="stat-box">
                    <h3>6</h3>
                    <p>Semester</p>
                </div>
            </section>
        </div>
    );
}
