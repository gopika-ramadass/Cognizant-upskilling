import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import StudentProfile from './components/StudentProfile';
import CourseCard from './components/CourseCard';
import Footer from './components/Footer';

export default function App() {
    // State management
    const [courses, setCourses] = useState([]);
    const [enrolledCourses, setEnrolledCourses] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // =========================================================================
    // useEffect for Data Fetching (Lifecycle - componentDidMount replacement)
    // =========================================================================
    useEffect(() => {
        const fetchCourses = async () => {
            try {
                setLoading(true);
                const response = await fetch('https://jsonplaceholder.typicode.com/posts?_limit=5');
                if (!response.ok) {
                    throw new Error(`HTTP Error! Status: ${response.status}`);
                }
                const data = await response.json();
                
                // Map API posts to course-like structures
                const mappedCourses = data.map(post => ({
                    id: post.id,
                    // Use capitalized post title
                    name: post.title.split(' ').slice(0, 3).map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' '),
                    code: `CS${100 + post.id}`,
                    credits: (post.id % 2 === 0) ? 4 : 3,
                    grade: ['A', 'B', 'A+', 'B+', 'A'][post.id % 5]
                }));
                
                setCourses(mappedCourses);
                setError(null);
            } catch (err) {
                setError(`Failed to fetch course data: ${err.message}`);
            } finally {
                setLoading(false);
            }
        };

        fetchCourses();
    }, []); // Empty dependency array means this runs ONLY once after the component mounts.

    // =========================================================================
    // useEffect with Dependency Array to Track State Changes
    // =========================================================================
    useEffect(() => {
        if (courses.length > 0) {
            console.log("Courses updated!", courses);
        }
        /*
        CRITICAL COMMENT explaining why the dependency array matters:
        -----------------------------------------------------------------------
        The dependency array `[courses]` specifies that React should execute this 
        effect callback if and only if the `courses` state reference changes 
        between renders. 
        - If the dependency array were omitted ``, the effect would trigger on 
          EVERY render (causing potential performance degradation or infinite loops).
        - If the dependency array were empty `[]`, the effect would trigger only 
          once after mounting and never run again when the data loads.
        - By targeting `[courses]`, we isolate this execution specifically to 
          when course data finishes loading or is modified.
        -----------------------------------------------------------------------
        */
    }, [courses]);

    // Handle course enrollment (State Lifting handler)
    const handleEnroll = (courseId) => {
        if (!enrolledCourses.includes(courseId)) {
            setEnrolledCourses(prev => [...prev, courseId]);
        }
    };

    // Filter courses based on user search term
    const filteredCourses = courses.filter(course => 
        course.name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div className="app-wrapper">
            {/* Header: displays the site name and enrollment count */}
            <Header siteName="Student Portal" enrolledCount={enrolledCourses.length} />

            <main className="main-content">
                
                {/* Student Profile component */}
                <StudentProfile />

                {/* Courses Dashboard Section */}
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

                    {/* Loading State */}
                    {loading && (
                        <div className="loader-container">
                            <div className="spinner"></div>
                            <p>Loading course catalog...</p>
                        </div>
                    )}

                    {/* Error State */}
                    {error && (
                        <div className="error-banner">
                            <p>⚠️ {error}</p>
                        </div>
                    )}

                    {/* Content List State */}
                    {!loading && !error && (
                        <>
                            {filteredCourses.length === 0 ? (
                                <p className="no-results">No courses match your search criteria.</p>
                            ) : (
                                <div className="course-grid">
                                    {filteredCourses.map(course => (
                                        <CourseCard 
                                            key={course.id}
                                            id={course.id}
                                            name={course.name}
                                            code={course.code}
                                            credits={course.credits}
                                            grade={course.grade}
                                            isEnrolled={enrolledCourses.includes(course.id)}
                                            onEnroll={handleEnroll}
                                        />
                                    ))}
                                </div>
                            )}
                        </>
                    )}
                </section>
            </main>

            {/* Footer */}
            <Footer />
        </div>
    );
}
