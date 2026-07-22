import React, { useState } from 'react';
import './index.css';

interface Course {
  id: number;
  name: string;
  code: string;
  credits: number;
  grade: string;
}

const initialCourses: Course[] = [
  { id: 1, name: 'Web Accessibility & WCAG Standards', code: 'CS101', credits: 4, grade: 'A' },
  { id: 2, name: 'Advanced React Architecture', code: 'CS102', credits: 3, grade: 'A+' },
  { id: 3, name: 'Cross-Browser Testing & Compatibility', code: 'CS103', credits: 4, grade: 'B+' },
  { id: 4, name: 'State Management with Redux Toolkit', code: 'CS104', credits: 3, grade: 'A' },
  { id: 5, name: 'TypeScript Fundamentals', code: 'CS105', credits: 4, grade: 'A+' },
];

export default function App() {
  const [courses] = useState<Course[]>(initialCourses);
  const [enrolledIds, setEnrolledIds] = useState<number[]>([]);
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [activeTab, setActiveTab] = useState<'courses' | 'profile'>('courses');
  const [isNavExpanded, setIsNavExpanded] = useState<boolean>(false);

  // Profile Form State
  const [profile, setProfile] = useState({
    fullName: 'Gopika R',
    email: 'gopika.r@example.com',
    semester: '6'
  });

  const handleEnrollToggle = (courseId: number) => {
    setEnrolledIds((prev) =>
      prev.includes(courseId)
        ? prev.filter((id) => id !== courseId)
        : [...prev, courseId]
    );
  };

  const handleCardKeyDown = (e: React.KeyboardEvent, courseId: number) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      handleEnrollToggle(courseId);
    }
  };

  const filteredCourses = courses.filter((c) =>
    c.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="app-container">
      {/* 1. Skip Link for Keyboard & Screen Reader Users */}
      <a href="#main-content" className="skip-link">
        Skip to main content
      </a>

      {/* 2. Accessible Header with Landmark and ARIA Navigation */}
      <header className="site-header" role="banner">
        <div className="logo-container">
          <span className="site-title">Student Portal</span>
          <button
            type="button"
            className="nav-toggle-btn"
            aria-expanded={isNavExpanded}
            aria-controls="primary-navigation"
            aria-label="Toggle navigation menu"
            onClick={() => setIsNavExpanded((prev) => !prev)}
          >
            ☰ Menu
          </button>
        </div>

        <nav
          id="primary-navigation"
          className={`main-nav ${isNavExpanded ? 'expanded' : ''}`}
          aria-label="Main navigation"
        >
          <ul className="nav-list">
            <li>
              <a
                href="#courses"
                className="nav-link"
                aria-current={activeTab === 'courses' ? 'page' : undefined}
                onClick={(e) => {
                  e.preventDefault();
                  setActiveTab('courses');
                }}
              >
                Courses Catalog
              </a>
            </li>
            <li>
              <a
                href="#profile"
                className="nav-link"
                aria-current={activeTab === 'profile' ? 'page' : undefined}
                onClick={(e) => {
                  e.preventDefault();
                  setActiveTab('profile');
                }}
              >
                Student Profile
              </a>
            </li>
          </ul>
          <div className="enroll-badge">
            <span aria-label={`Enrolled in ${enrolledIds.length} courses`}>
              📚 Enrolled: <strong>{enrolledIds.length}</strong>
            </span>
          </div>
        </nav>
      </header>

      {/* 3. Main Content Area */}
      <main id="main-content" className="main-content" tabIndex={-1}>
        {/* Hero Banner Section */}
        <section className="hero-section" aria-labelledby="hero-heading">
          <h1 id="hero-heading">Accessible & Responsive Student Portal</h1>
          <p>
            Demonstrating WCAG 2.1 AA accessibility, ARIA live regions, full keyboard navigability, and cross-browser resilience.
          </p>
        </section>

        {activeTab === 'courses' ? (
          <section aria-labelledby="courses-heading">
            <h2 id="courses-heading" style={{ marginBottom: '1rem', color: 'var(--primary)' }}>
              Available Courses
            </h2>

            {/* Accessible Search Controls with Explicit Label */}
            <div className="controls-section">
              <div className="form-group">
                <label htmlFor="course-search-input">
                  🔍 Search Courses by Name (Filter list in real time)
                </label>
                <input
                  id="course-search-input"
                  type="text"
                  className="search-input"
                  placeholder="Type to filter courses (e.g. Accessibility, React)..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
              </div>

              {/* ARIA Live Region for Screen Reader Announcements */}
              <div
                role="status"
                aria-live="polite"
                aria-atomic="true"
                className="results-status"
              >
                Showing {filteredCourses.length} of {courses.length} courses matching search criteria.
              </div>
            </div>

            {/* Course Cards Grid */}
            <div className="course-grid" role="region" aria-label="Course cards listing">
              {filteredCourses.length === 0 ? (
                <p style={{ color: 'var(--text-muted)', fontStyle: 'italic' }}>
                  No courses found matching "{searchTerm}".
                </p>
              ) : (
                filteredCourses.map((course) => {
                  const isEnrolled = enrolledIds.includes(course.id);
                  return (
                    <article
                      key={course.id}
                      className={`course-card ${isEnrolled ? 'enrolled' : ''}`}
                      tabIndex={0}
                      onKeyDown={(e) => handleCardKeyDown(e, course.id)}
                      aria-label={`${course.name}, Code ${course.code}, Credits ${course.credits}, Grade ${course.grade}. ${
                        isEnrolled ? 'Status: Enrolled.' : 'Status: Not Enrolled.'
                      } Press Enter or Space to toggle enrollment.`}
                    >
                      <div>
                        <div className="course-code">{course.code}</div>
                        <h3>{course.name}</h3>
                        <div className="course-meta">
                          <span className="badge">Credits: {course.credits}</span>
                          <span className="badge">Grade: {course.grade}</span>
                        </div>
                      </div>
                      <button
                        type="button"
                        className={`btn ${isEnrolled ? 'btn-success' : 'btn-primary'}`}
                        onClick={(e) => {
                          e.stopPropagation(); // Avoid double toggle if clicked directly
                          handleEnrollToggle(course.id);
                        }}
                        aria-pressed={isEnrolled}
                      >
                        {isEnrolled ? '✓ Enrolled' : '+ Enroll Course'}
                      </button>
                    </article>
                  );
                })
              )}
            </div>
          </section>
        ) : (
          /* Profile Section with Accessible Form Controls */
          <section aria-labelledby="profile-heading" style={{ background: 'white', padding: '2rem', borderRadius: '12px', border: '1px solid var(--border-color)' }}>
            <h2 id="profile-heading" style={{ marginBottom: '1.5rem', color: 'var(--primary)' }}>
              Student Profile Settings
            </h2>
            <form onSubmit={(e) => e.preventDefault()} style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem', maxWidth: '500px' }}>
              <div className="form-group">
                <label htmlFor="student-name">Full Name</label>
                <input
                  id="student-name"
                  type="text"
                  className="search-input"
                  value={profile.fullName}
                  onChange={(e) => setProfile({ ...profile, fullName: e.target.value })}
                />
              </div>

              <div className="form-group">
                <label htmlFor="student-email">Email Address</label>
                <input
                  id="student-email"
                  type="email"
                  className="search-input"
                  value={profile.email}
                  onChange={(e) => setProfile({ ...profile, email: e.target.value })}
                />
              </div>

              <div className="form-group">
                <label htmlFor="student-semester">Current Semester</label>
                <input
                  id="student-semester"
                  type="number"
                  min="1"
                  max="8"
                  className="search-input"
                  value={profile.semester}
                  onChange={(e) => setProfile({ ...profile, semester: e.target.value })}
                />
              </div>

              <button type="submit" className="btn btn-primary" style={{ width: 'auto', alignSelf: 'flex-start' }}>
                Save Profile Updates
              </button>
            </form>
          </section>
        )}
      </main>

      {/* Footer */}
      <footer className="site-footer" role="contentinfo">
        <p>© 2026 Student Portal | Digital Nurture 5.0 | Web Accessibility & Cross-Browser Compliant</p>
      </footer>
    </div>
  );
}
