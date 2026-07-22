import React from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { unenroll } from '../enrollmentSlice';
import StudentProfile from '../components/StudentProfile';

export default function ProfilePage() {
    const enrolledCourses = useSelector(state => state.enrollment.enrolledCourses);
    const dispatch = useDispatch();

    const handleRemove = (courseId) => {
        dispatch(unenroll(courseId));
    };

    // Calculate total credits of enrolled courses
    const totalCredits = enrolledCourses.reduce((sum, course) => sum + course.credits, 0);

    return (
        <div className="profile-page-container">
            {/* Student Profile inputs & preview */}
            <StudentProfile />

            {/* Enrolled Courses list with Remove actions */}
            <section className="enrolled-courses-section" style={{ marginTop: '40px', background: 'white', padding: '30px', borderRadius: '12px', boxShadow: '0 4px 20px rgba(0, 0, 0, 0.06)' }}>
                <h2>Enrolled Courses</h2>
                
                {enrolledCourses.length === 0 ? (
                    <p className="no-results">You are not currently enrolled in any courses. Explore the catalog to enroll!</p>
                ) : (
                    <div>
                        <ul className="enrolled-list" style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '15px', marginBottom: '20px' }}>
                            {enrolledCourses.map(course => (
                                <li 
                                    key={course.id} 
                                    className="enrolled-item"
                                    style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '15px 20px', background: '#f8f9fa', border: '1px solid #e9ecef', borderRadius: '8px' }}
                                >
                                    <div>
                                        <h4 style={{ color: '#1f4e79', fontSize: '16px' }}>{course.name}</h4>
                                        <p style={{ fontSize: '13px', color: '#6c757d' }}>Code: <strong>{course.code}</strong> | Credits: <strong>{course.credits}</strong></p>
                                    </div>
                                    <button 
                                        onClick={() => handleRemove(course.id)}
                                        className="btn-secondary btn-small"
                                        style={{ borderColor: '#e71d36', color: '#e71d36', background: 'transparent' }}
                                        onMouseEnter={(e) => {
                                            e.target.style.background = '#e71d36';
                                            e.target.style.color = 'white';
                                        }}
                                        onMouseLeave={(e) => {
                                            e.target.style.background = 'transparent';
                                            e.target.style.color = '#e71d36';
                                        }}
                                    >
                                        Remove
                                    </button>
                                </li>
                            ))}
                        </ul>

                        <div className="summary-container" style={{ borderTop: '2px solid #e9ecef', paddingTop: '15px', textAlign: 'right' }}>
                            <p style={{ fontSize: '18px' }}>Total Registered Credits: <strong style={{ color: '#d35400', fontSize: '22px' }}>{totalCredits}</strong></p>
                        </div>
                    </div>
                )}
            </section>
        </div>
    );
}
