import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import HomePage from './pages/HomePage';
import CoursesPage from './pages/CoursesPage';
import ProfilePage from './pages/ProfilePage';
import CourseDetailPage from './pages/CourseDetailPage';

export default function App() {
    return (
        <div className="app-wrapper">
            {/* Nav Header is rendered on all pages */}
            <Header siteName="Student Portal" />

            <main className="main-content">
                <Routes>
                    <Route path="/" element={<HomePage />} />
                    <Route path="/courses" element={<CoursesPage />} />
                    <Route path="/profile" element={<ProfilePage />} />
                    <Route path="/courses/:courseId" element={<CourseDetailPage />} />
                </Routes>
            </main>

            {/* Footer is rendered on all pages */}
            <Footer />
        </div>
    );
}
