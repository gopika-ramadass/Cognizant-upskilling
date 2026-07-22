import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { enroll } from '../enrollmentSlice';
import CourseCard from '../components/CourseCard';

export default function CoursesPage() {
    const [courses, setCourses] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const dispatch = useDispatch();
    const navigate = useNavigate();
    const enrolledCourses = useSelector(state => state.enrollment.enrolledCourses);

    useEffect(() => {
        const fetchCourses = async () => {
            try {
                setLoading(true);
                const response = await fetch('https://jsonplaceholder.typicode.com/posts?_limit=5');
                if (!response.ok) {
                    throw new Error(`HTTP Error! Status: ${response.status}`);
                }
                const data = await response.json();
                
                const mappedCourses = data.map(post => ({
                    id: post.id,
                    name: post.title.split(' ').slice(0, 3).map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' '),
                    code: `CS${100 + post.id}`,
                    credits: (post.id % 2 === 0) ? 4 : 3,
                    grade: ['A', 'B', 'A+', 'B+', 'A'][post.id % 5]
                }));
                
                setCourses(mappedCourses);
            } catch (err) {
                setError(`Failed to fetch courses: ${err.message}`);
            } finally {
                setLoading(false);
            }
        };

        fetchCourses();
    }, []);

    const handleEnroll = (courseId) => {
        const course = courses.find(c => c.id === courseId);
        if (course) {
            dispatch(enroll(course));
            navigate('/profile'); // Programmatic navigation to profile page
        }
    };

    const filteredCourses = courses.filter(course => 
        course.name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <section className="courses-section">
            <h2>Available Courses</h2>

            {/* Search Controls */}
            <div className="search-bar-container">
                <input 
                    type="text" 
                    className="search-input"
                    placeholder="🔍 Search courses by name..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                />
            </div>

            {/* Loading / Error / Grid */}
            {loading && (
                <div className="loader-container">
                    <div className="spinner"></div>
                    <p>Loading course catalog...</p>
                </div>
            )}

            {error && (
                <div className="error-banner">
                    <p>⚠️ {error}</p>
                </div>
            )}

            {!loading && !error && (
                <>
                    {filteredCourses.length === 0 ? (
                        <p className="no-results">No courses match your search criteria.</p>
                    ) : (
                        <div className="course-grid">
                            {filteredCourses.map(course => {
                                const isEnrolled = enrolledCourses.some(c => c.id === course.id);
                                return (
                                    <CourseCard 
                                        key={course.id}
                                        id={course.id}
                                        name={course.name}
                                        code={course.code}
                                        credits={course.credits}
                                        grade={course.grade}
                                        isEnrolled={isEnrolled}
                                        onEnroll={handleEnroll}
                                    />
                                );
                            })}
                        </div>
                    )}
                </>
            )}
        </section>
    );
}
