import React from 'react';

export default function CourseCard({ id, name, code, credits, grade, onEnroll, isEnrolled }) {
    return (
        <article className={`course-card ${isEnrolled ? 'enrolled' : ''}`}>
            <h3>{name}</h3>
            <p>Course Code: <strong>{code}</strong></p>
            <div className="card-meta">
                <span className="credits-tag">Credits: {credits}</span>
                <span className="grade-tag">Grade: {grade}</span>
            </div>
            <button 
                onClick={() => onEnroll(id)} 
                disabled={isEnrolled}
                className={`enroll-btn ${isEnrolled ? 'btn-disabled' : 'btn-enroll'}`}
            >
                {isEnrolled ? '✓ Enrolled' : 'Enroll Course'}
            </button>
        </article>
    );
}
