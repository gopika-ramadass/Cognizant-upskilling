import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { enroll } from '../enrollmentSlice';

export default function CourseDetailPage() {
    const { courseId } = useParams();
    const navigate = useNavigate();
    const dispatch = useDispatch();
    const enrolledCourses = useSelector(state => state.enrollment.enrolledCourses);

    const [course, setCourse] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchCourseDetails = async () => {
            try {
                setLoading(true);
                const response = await fetch(`https://jsonplaceholder.typicode.com/posts/${courseId}`);
                if (!response.ok) {
                    throw new Error(`HTTP Error! Course not found. Status: ${response.status}`);
                }
                const post = await response.json();
                
                // Map API post to course details
                const idNum = parseInt(courseId, 10);
                const mappedCourse = {
                    id: post.id,
                    name: post.title.split(' ').slice(0, 3).map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' '),
                    code: `CS${100 + idNum}`,
                    credits: (idNum % 2 === 0) ? 4 : 3,
                    grade: ['A', 'B', 'A+', 'B+', 'A'][idNum % 5],
                    description: post.body
                };
                
                setCourse(mappedCourse);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchCourseDetails();
    }, [courseId]);

    const handleEnroll = () => {
        if (course) {
            dispatch(enroll(course));
            navigate('/profile'); // Route to profile on enroll
        }
    };

    const isEnrolled = course ? enrolledCourses.some(c => c.id === course.id) : false;

    return (
        <section className="course-detail-section" style={{ background: 'white', padding: '40px', borderRadius: '12px', boxShadow: '0 4px 20px rgba(0, 0, 0, 0.06)' }}>
            <Link to="/courses" className="btn-secondary btn-small" style={{ textDecoration: 'none', marginBottom: '25px', display: 'inline-block' }}>
                ← Back to Courses
            </Link>

            {loading && (
                <div className="loader-container">
                    <div className="spinner"></div>
                    <p>Loading course details...</p>
                </div>
            )}

            {error && (
                <div className="error-banner">
                    <p>⚠️ Error loading details: {error}</p>
                </div>
            )}

            {!loading && !error && course && (
                <div className="course-detail-container">
                    <h2 style={{ fontSize: '32px', color: '#1f4e79', marginBottom: '15px' }}>{course.name}</h2>
                    <p style={{ fontSize: '15px', color: '#6c757d', marginBottom: '25px' }}>
                        Course Code: <strong style={{ color: '#2b2d42' }}>{course.code}</strong> | 
                        Credits: <strong style={{ color: '#2b2d42' }}>{course.credits}</strong> | 
                        Standard Grade: <strong style={{ color: '#2b2d42' }}>{course.grade}</strong>
                    </p>

                    <div className="course-description" style={{ borderTop: '1px solid #e9ecef', borderBottom: '1px solid #e9ecef', padding: '25px 0', marginBottom: '30px' }}>
                        <h4 style={{ color: '#1f4e79', marginBottom: '10px' }}>Syllabus Description</h4>
                        <p style={{ color: '#2b2d42', fontSize: '16px', textTransform: 'capitalize' }}>{course.description}</p>
                    </div>

                    <button 
                        onClick={handleEnroll} 
                        disabled={isEnrolled}
                        className={`btn-primary ${isEnrolled ? 'btn-disabled' : ''}`}
                        style={{ width: '220px', padding: '14px' }}
                    >
                        {isEnrolled ? '✓ Already Enrolled' : 'Enroll in Course'}
                    </button>
                </div>
            )}
        </section>
    );
}
