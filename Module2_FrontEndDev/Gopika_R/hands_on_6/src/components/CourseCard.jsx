import React from 'react';
import { Link } from 'react-router-dom';

export default function CourseCard({ id, name, code, credits, grade, onEnroll, isEnrolled }) {
    return (
        <article className={`course-card ${isEnrolled ? 'enrolled' : ''}`}>
            <h3>{name}</h3>
            <p>Course Code: <strong>{code}</strong></p>
            <div className="card-meta">
                <span className="credits-tag">Credits: {credits}</span>
                <span className="grade-tag">Grade: {grade}</span>
            </div>
            
            <div className="card-actions" style={{ display: 'flex', gap: '10px', marginTop: 'auto' }}>
                <button 
                    onClick={(e) => {
                        e.stopPropagation();
                        onEnroll(id);
                    }} 
                    disabled={isEnrolled}
                    className={`enroll-btn ${isEnrolled ? 'btn-disabled' : 'btn-enroll'}`}
                    style={{ flex: 1 }}
                >
                    {isEnrolled ? '✓ Enrolled' : 'Enroll'}
                </button>
                <Link 
                    to={`/courses/${id}`} 
                    className="btn-secondary btn-small" 
                    style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', textDecoration: 'none', textAlign: 'center', fontSize: '13px', padding: '6px 12px' }}
                >
                    Details
                </Link>
            </div>
        </article>
    );
}
