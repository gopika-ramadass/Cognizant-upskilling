import React, { useState } from 'react';

export default function StudentProfile() {
    const [profile, setProfile] = useState({
        name: 'Gopika R',
        email: 'gopika.r@example.com',
        semester: '6'
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setProfile(prev => ({
            ...prev,
            [name]: value
        }));
    };

    return (
        <section className="profile-section">
            <h2>Student Profile</h2>
            <div className="profile-container">
                {/* Form to update state */}
                <form className="profile-form" onSubmit={(e) => e.preventDefault()}>
                    <div className="form-group">
                        <label htmlFor="name-input">Full Name</label>
                        <input 
                            type="text" 
                            id="name-input"
                            name="name" 
                            value={profile.name} 
                            onChange={handleChange} 
                            placeholder="Enter full name"
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="email-input">Email Address</label>
                        <input 
                            type="email" 
                            id="email-input"
                            name="email" 
                            value={profile.email} 
                            onChange={handleChange} 
                            placeholder="Enter email address"
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="semester-input">Current Semester</label>
                        <input 
                            type="number" 
                            id="semester-input"
                            name="semester" 
                            value={profile.semester} 
                            onChange={handleChange} 
                            min="1" 
                            max="8" 
                            placeholder="Semester"
                        />
                    </div>
                </form>

                {/* Profile Live Card View */}
                <div className="profile-card-preview">
                    <div className="avatar-placeholder">
                        {profile.name ? profile.name.split(' ').map(n => n[0]).join('').toUpperCase() : 'S'}
                    </div>
                    <div className="preview-details">
                        <h3>{profile.name || "Student Name"}</h3>
                        <p className="email-text">📧 {profile.email || "student@example.com"}</p>
                        <p className="sem-text">Semester <strong>{profile.semester || "-"}</strong></p>
                    </div>
                </div>
            </div>
        </section>
    );
}
