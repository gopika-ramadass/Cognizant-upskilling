import { courses } from './data.js';

// ==========================================
// Task 1: ES6+ Syntax Practice
// ==========================================

console.log("--- Task 1: ES6+ Syntax Practice ---");

// Destructuring in a loop
console.log("Destructured course info:");
courses.forEach(course => {
    const { name, credits } = course;
    console.log(`Course: ${name}, Credits: ${credits}`);
});

// Array.map() for formatted strings
const courseStrings = courses.map(course => `${course.code} — ${course.name} (${course.credits} credits)`);
console.log("Mapped Course Strings:", courseStrings);

// Array.filter() for credits >= 4
const highCreditCourses = courses.filter(course => course.credits >= 4);
console.log("Count of courses with >= 4 credits:", highCreditCourses.length);
console.log("High credit courses:", highCreditCourses);

// Array.reduce() for total credits
const totalCreditsValue = courses.reduce((acc, course) => acc + course.credits, 0);
console.log("Total credits enrolled:", totalCreditsValue);

// Arrow function with template literal replacing a traditional for loop
// (We will use this arrow function syntax in our main rendering function below)
const logCourseDetails = (courseList) => {
    courseList.forEach(course => {
        console.log(`[Arrow/Template] ${course.code}: ${course.name} is a ${course.credits}-credit course with grade ${course.grade}`);
    });
};
logCourseDetails(courses);


// ==========================================
// Task 2 & 3: DOM Selection, Dynamic Rendering, & Interactivity
// ==========================================

// Global state for courses (can be sorted or filtered)
let activeCourses = [...courses];

// DOM Element references
const courseGrid = document.querySelector('.course-grid');
const totalCreditsEl = document.querySelector('#total-credits strong');
const searchInput = document.querySelector('#search-courses');
const sortBtn = document.querySelector('#sort-btn');
const selectedCourseEl = document.querySelector('#selected-course');

/**
 * Renders the course cards in the DOM based on the provided list of courses.
 * Uses arrow functions, template literals, and DocumentFragment for optimal performance.
 * @param {Array} coursesList 
 */
const renderCourses = (coursesList) => {
    // Clear existing content
    courseGrid.innerHTML = '';

    if (coursesList.length === 0) {
        courseGrid.innerHTML = '<p class="placeholder-text" style="grid-column: 1/-1; text-align: center;">No courses found matching your search.</p>';
        totalCreditsEl.textContent = '0';
        return;
    }

    // DocumentFragment for batch-appending (better performance)
    const fragment = document.createDocumentFragment();

    coursesList.forEach(course => {
        const article = document.createElement('article');
        article.className = 'course-card';
        article.setAttribute('data-id', course.id);
        
        // Build inner HTML using template literals
        article.innerHTML = `
            <h3>${course.name}</h3>
            <p>Course Code: <strong>${course.code}</strong></p>
            <span>Credits: ${course.credits}</span>
        `;
        
        fragment.appendChild(article);
    });

    courseGrid.appendChild(fragment);

    // Update total credits dynamically for the displayed courses
    const displayTotalCredits = coursesList.reduce((sum, c) => sum + c.credits, 0);
    totalCreditsEl.textContent = displayTotalCredits;
};

// ==========================================
// Event Listeners and Interactivity
// ==========================================

// Input Event: Instant search filtering
searchInput.addEventListener('input', (e) => {
    const searchTerm = e.target.value.toLowerCase().trim();
    activeCourses = courses.filter(course => course.name.toLowerCase().includes(searchTerm));
    renderCourses(activeCourses);
});

// Click Event: Sort by credits descending
sortBtn.addEventListener('click', () => {
    // Sort activeCourses in place
    activeCourses.sort((a, b) => b.credits - a.credits);
    renderCourses(activeCourses);
});

// Event Delegation: Click listener on courseGrid to catch child card clicks
courseGrid.addEventListener('click', (e) => {
    // Find closest course-card wrapper
    const card = e.target.closest('.course-card');
    if (!card) return;

    // Get course ID from data attribute
    const courseId = parseInt(card.getAttribute('data-id'), 10);
    const clickedCourse = courses.find(c => c.id === courseId);

    if (clickedCourse) {
        // Display full details in the details container
        selectedCourseEl.innerHTML = `
            <h3>Course Details</h3>
            <div class="selected-course-card">
                <h4>${clickedCourse.name}</h4>
                <p><strong>Code:</strong> ${clickedCourse.code}</p>
                <p><strong>Credits:</strong> ${clickedCourse.credits}</p>
                <p><strong>Grade Achieved:</strong> ${clickedCourse.grade}</p>
            </div>
        `;
    }
});

// Initial rendering of courses
renderCourses(activeCourses);
