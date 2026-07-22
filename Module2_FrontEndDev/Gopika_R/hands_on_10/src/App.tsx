import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import type { AppDispatch } from './store/store';
import {
  fetchAllCourses,
  selectCourses,
  selectCoursesLoading,
  selectCoursesError,
} from './store/coursesSlice';
import {
  enroll,
  unenroll,
  selectEnrolledCourses,
} from './store/enrollmentSlice';
import './index.css';

export default function App() {
  const dispatch = useDispatch<AppDispatch>();

  // Selectors decouple component from direct store shape
  const courses = useSelector(selectCourses);
  const loading = useSelector(selectCoursesLoading);
  const error = useSelector(selectCoursesError);
  const enrolledCourses = useSelector(selectEnrolledCourses);

  const [searchTerm, setSearchTerm] = useState('');
  const [triggerCrash, setTriggerCrash] = useState(false);

  // 1. Dispatch createAsyncThunk on mount to load courses via Centralized API Service Layer
  useEffect(() => {
    dispatch(fetchAllCourses());
  }, [dispatch]);

  // Handle Intentional Component Crash for Error Boundary testing
  if (triggerCrash) {
    throw new Error('Simulated Unhandled Runtime Exception for ErrorBoundary Verification!');
  }

  const filteredCourses = courses.filter((c) =>
    c.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="app-wrapper">
      {/* Header */}
      <header className="site-header">
        <h1 className="site-title">Student Portal — API & Redux Toolkit</h1>
        <div className="badge">
          📚 Enrolled Courses: <strong>{enrolledCourses.length}</strong>
        </div>
      </header>

      {/* Main Content */}
      <main className="main-content">
        <section className="hero-banner">
          <h1>Centralised API Layer & Async Thunks</h1>
          <p>
            Consuming API via Axios interceptors, Redux Toolkit createAsyncThunk extraReducers, and global Error Boundary.
          </p>
        </section>

        {/* Search & Diagnostic Controls */}
        <div style={{ marginBottom: '1.5rem', display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
          <input
            type="text"
            className="search-box"
            placeholder="🔍 Search courses by name..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            style={{ flex: 1, marginBottom: 0 }}
          />

          <button
            type="button"
            className="btn btn-danger"
            style={{ width: 'auto', marginTop: 0 }}
            onClick={() => setTriggerCrash(true)}
          >
            🧪 Test Error Boundary Crash
          </button>
        </div>

        {/* Loading State */}
        {loading && (
          <div className="spinner-container">
            <div className="spinner"></div>
            <p>Loading course catalog via Async Thunk & Axios...</p>
          </div>
        )}

        {/* API Error State */}
        {error && (
          <div className="error-banner">
            <span>⚠️ {error}</span>
            <button
              type="button"
              className="btn btn-primary"
              style={{ width: 'auto', padding: '6px 12px' }}
              onClick={() => dispatch(fetchAllCourses())}
            >
              Retry API Request
            </button>
          </div>
        )}

        {/* Course Catalog Grid */}
        {!loading && !error && (
          <div className="course-grid">
            {filteredCourses.length === 0 ? (
              <p style={{ gridColumn: '1/-1', textAlign: 'center', color: '#64748b' }}>
                No courses match your search criteria.
              </p>
            ) : (
              filteredCourses.map((course) => {
                const isEnrolled = enrolledCourses.some((c) => c.id === course.id);
                return (
                  <div key={course.id} className={`course-card ${isEnrolled ? 'enrolled' : ''}`}>
                    <div>
                      <span style={{ fontSize: '0.85rem', fontWeight: 'bold', color: '#2563eb' }}>
                        {course.code}
                      </span>
                      <h3>{course.name}</h3>
                      <p style={{ fontSize: '0.9rem', color: '#64748b', marginBottom: '1rem' }}>
                        {course.description}
                      </p>
                      <div style={{ display: 'flex', gap: '8px', marginBottom: '1rem' }}>
                        <span style={{ background: '#e2e8f0', padding: '2px 8px', borderRadius: '4px', fontSize: '0.8rem', fontWeight: 'bold' }}>
                          Credits: {course.credits}
                        </span>
                        <span style={{ background: '#e2e8f0', padding: '2px 8px', borderRadius: '4px', fontSize: '0.8rem', fontWeight: 'bold' }}>
                          Grade: {course.grade}
                        </span>
                      </div>
                    </div>

                    <button
                      type="button"
                      className={`btn ${isEnrolled ? 'btn-success' : 'btn-primary'}`}
                      onClick={() =>
                        isEnrolled ? dispatch(unenroll(course.id)) : dispatch(enroll(course))
                      }
                    >
                      {isEnrolled ? '✓ Enrolled (Click to Unenroll)' : '+ Enroll Course'}
                    </button>
                  </div>
                );
              })
            )}
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="site-footer">
        <p>© 2026 Student Portal | Digital Nurture 5.0 | Hands-On 10 Advanced State & Centralised API Layer</p>
      </footer>
    </div>
  );
}
