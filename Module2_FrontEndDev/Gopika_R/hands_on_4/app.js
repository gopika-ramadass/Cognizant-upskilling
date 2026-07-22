import { courses } from './data.js';

// ============================================================================
// Task 1: Promises and async/await
// ============================================================================

/**
 * Fetch user by ID using Promise Chaining (.then)
 * @param {number} id 
 * @returns {Promise}
 */
function fetchUser(id) {
    return fetch('https://jsonplaceholder.typicode.com/users/' + id)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(user => {
            console.log(`[Promise Chaining] Fetched user ID ${id}: ${user.name}`);
            return user;
        })
        .catch(err => {
            console.error(`[Promise Chaining] Error fetching user ID ${id}:`, err.message);
        });
}

/**
 * Fetch user by ID using async/await and try/catch
 * @param {number} id 
 * @returns {Promise<Object>}
 */
async function fetchUserAsync(id) {
    try {
        const response = await fetch(`https://jsonplaceholder.typicode.com/users/${id}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const user = await response.json();
        console.log(`[async/await] Fetched user ID ${id}: ${user.name}`);
        return user;
    } catch (err) {
        console.error(`[async/await] Error fetching user ID ${id}:`, err.message);
        throw err;
    }
}

/**
 * Simulates a courses database fetch with a 1-second delay
 * @returns {Promise<Array>}
 */
function fetchAllCourses() {
    return new Promise(resolve => {
        setTimeout(() => {
            resolve(courses);
        }, 1000);
    });
}

/**
 * Demonstrating concurrent API requests using Promise.all()
 */
async function demoPromiseAll() {
    console.log("--- Starting Promise.all() Concurrent Fetch for User 1 & 2 ---");
    try {
        // Fetch users 1 and 2 concurrently
        const [user1, user2] = await Promise.all([
            fetchUserAsync(1),
            fetchUserAsync(2)
        ]);
        console.log(`[Promise.all Success] User 1: ${user1.name}, User 2: ${user2.name}`);
    } catch (err) {
        console.error("[Promise.all Failure] One of the concurrent requests failed:", err.message);
    }
}

// Execute Promise demo functions
fetchUser(1);
demoPromiseAll();


// ============================================================================
// Task 2: Fetch API with Error Handling & UI States
// ============================================================================

// DOM Element references
const coursesLoader = document.getElementById('courses-loader');
const courseGrid = document.querySelector('.course-grid');
const totalCreditsEl = document.querySelector('#total-credits strong');
const searchInput = document.getElementById('search-courses');
const sortBtn = document.getElementById('sort-btn');
const selectedCourseEl = document.getElementById('selected-course');

const notificationsLoader = document.getElementById('notifications-loader');
const notificationsError = document.getElementById('notifications-error');
const notificationsList = document.getElementById('notifications-list');
const retryNotificationsBtn = document.getElementById('retry-notifications-btn');
const test404Btn = document.getElementById('test-404-btn');
const fetchUser1Btn = document.getElementById('fetch-user1-btn');

let activeCourses = [];

/**
 * Reusable async Fetch API client with HTTP status validation
 * @param {string} url 
 * @returns {Promise<any>}
 */
async function apiFetch(url) {
    const response = await fetch(url);
    if (!response.ok) {
        throw new Error(`HTTP Request Failed! Status: ${response.status} (${response.statusText})`);
    }
    return await response.json();
}

/**
 * Loads recent announcements/posts and renders them in notifications
 */
async function loadNotifications() {
    // UI Loading State
    notificationsLoader.classList.remove('hidden');
    notificationsError.classList.add('hidden');
    notificationsList.classList.add('hidden');

    try {
        // Fetch top 5 posts from JSONPlaceholder
        const posts = await apiFetch('https://jsonplaceholder.typicode.com/posts?_limit=5');
        
        // Render notifications list
        renderNotifications(posts);
        
        // UI Success State
        notificationsLoader.classList.add('hidden');
        notificationsList.classList.remove('hidden');
    } catch (error) {
        // UI Error State
        notificationsLoader.classList.add('hidden');
        notificationsList.classList.add('hidden');
        notificationsError.classList.remove('hidden');
        
        // Inject user-friendly error message
        notificationsError.querySelector('.error-message').textContent = 
            `Unable to retrieve notices: ${error.message}`;
    }
}

/**
 * Renders notifications to the UI
 * @param {Array} posts 
 */
function renderNotifications(posts) {
    notificationsList.innerHTML = '';
    
    posts.forEach(post => {
        const card = document.createElement('div');
        card.className = 'notification-card';
        card.innerHTML = `
            <h4>📢 ${post.title}</h4>
            <p>${post.body.substring(0, 100)}...</p>
        `;
        notificationsList.appendChild(card);
    });
}


// ============================================================================
// Task 3: Introduction to Axios
// ============================================================================

/*
--------------------------------------------------------------------------------
SIDE-BY-SIDE DIFFERENCES BETWEEN FETCH AND AXIOS
--------------------------------------------------------------------------------
1. Response Parsing:
   - FETCH: Needs an explicit step to convert the response streams into JSON (e.g. `await response.json()`).
   - AXIOS: Automatically parses JSON responses and returns them under the `response.data` object.

2. Error Handling:
   - FETCH: Only rejects promises on network failures. Successive non-2xx status codes (like 404, 500) 
     resolve successfully with response.ok set to false, meaning you must check response.ok manually.
   - AXIOS: Automatically rejects the promise and throws an error if the response status lies outside 
     the 2xx range, simplifying try/catch blocks.

3. Configuration & Params Mapping:
   - FETCH: Query parameters must be hardcoded or formatted via URLSearchParams. Interceptors are not built-in.
   - AXIOS: Supports query parameters mapping via a key-value `params` object, and offers a robust built-in 
     request/response interceptor system for headers, logging, and token authorization.
--------------------------------------------------------------------------------
*/

// Set up Axios request interceptor
axios.interceptors.request.use(config => {
    console.log(`[Axios Interceptor] API call started: ${config.url}`, config.params || "");
    return config;
}, error => {
    return Promise.reject(error);
});

/**
 * Reusable async Axios client with automatic error mapping
 * @param {string} url 
 * @param {Object} config 
 * @returns {Promise<any>}
 */
async function apiFetchAxios(url, config = {}) {
    try {
        const response = await axios.get(url, config);
        // Return parsed data directly
        return response.data;
    } catch (error) {
        // Map error into a standard format
        const status = error.response ? error.response.status : 'Network Error';
        const message = error.response ? error.response.statusText : error.message;
        throw new Error(`Axios Failed! Status: ${status} - ${message}`);
    }
}

/**
 * Loads posts belonging to User ID 1 using Axios and renders them in Notifications
 */
async function loadUser1Posts() {
    notificationsLoader.classList.remove('hidden');
    notificationsError.classList.add('hidden');
    notificationsList.classList.add('hidden');

    try {
        // Fetch using params configuration object
        const posts = await apiFetchAxios('https://jsonplaceholder.typicode.com/posts', {
            params: { userId: 1 }
        });
        
        // Render user-specific posts (limit to 5)
        renderNotifications(posts.slice(0, 5));
        
        notificationsLoader.classList.add('hidden');
        notificationsList.classList.remove('hidden');
    } catch (error) {
        notificationsLoader.classList.add('hidden');
        notificationsList.classList.add('hidden');
        notificationsError.classList.remove('hidden');
        notificationsError.querySelector('.error-message').textContent = 
            `Axios error: ${error.message}`;
    }
}


// ============================================================================
// Core Dashboard Rendering & Navigation Logic (from Hands-On 3)
// ============================================================================

const renderCourses = (coursesList) => {
    courseGrid.innerHTML = '';

    if (coursesList.length === 0) {
        courseGrid.innerHTML = '<p class="placeholder-text" style="grid-column: 1/-1; text-align: center;">No courses found.</p>';
        totalCreditsEl.textContent = '0';
        return;
    }

    const fragment = document.createDocumentFragment();
    coursesList.forEach(course => {
        const article = document.createElement('article');
        article.className = 'course-card';
        article.setAttribute('data-id', course.id);
        article.innerHTML = `
            <h3>${course.name}</h3>
            <p>Course Code: <strong>${course.code}</strong></p>
            <span>Credits: ${course.credits}</span>
        `;
        fragment.appendChild(article);
    });
    courseGrid.appendChild(fragment);

    const displayTotalCredits = coursesList.reduce((sum, c) => sum + c.credits, 0);
    totalCreditsEl.textContent = displayTotalCredits;
};

// Controls and search handlers
searchInput.addEventListener('input', (e) => {
    const searchTerm = e.target.value.toLowerCase().trim();
    const filtered = activeCourses.filter(course => course.name.toLowerCase().includes(searchTerm));
    renderCourses(filtered);
});

sortBtn.addEventListener('click', () => {
    activeCourses.sort((a, b) => b.credits - a.credits);
    renderCourses(activeCourses);
});

courseGrid.addEventListener('click', (e) => {
    const card = e.target.closest('.course-card');
    if (!card) return;

    const courseId = parseInt(card.getAttribute('data-id'), 10);
    const clickedCourse = activeCourses.find(c => c.id === courseId);

    if (clickedCourse) {
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


// ============================================================================
// Initialization
// ============================================================================

// Simulated courses load with loader UI state
async function initDashboard() {
    try {
        // Fetch courses (simulate delay)
        activeCourses = await fetchAllCourses();
        
        // Hide loader, render courses
        coursesLoader.classList.add('hidden');
        courseGrid.classList.remove('hidden');
        renderCourses(activeCourses);
    } catch (err) {
        coursesLoader.innerHTML = `<p style="color:red">Failed to load courses: ${err.message}</p>`;
    }
}

// Retry notifications event
retryNotificationsBtn.addEventListener('click', loadNotifications);

// Debug buttons
test404Btn.addEventListener('click', async () => {
    notificationsLoader.classList.remove('hidden');
    notificationsError.classList.add('hidden');
    notificationsList.classList.add('hidden');
    
    try {
        // Trigger manual error with a non-existent URL
        await apiFetch('https://jsonplaceholder.typicode.com/nonexistent');
    } catch (error) {
        notificationsLoader.classList.add('hidden');
        notificationsError.classList.remove('hidden');
        notificationsError.querySelector('.error-message').textContent = 
            `Simulated 404 error: ${error.message}`;
    }
});

fetchUser1Btn.addEventListener('click', loadUser1Posts);

// Kick off page components
initDashboard();
loadNotifications();
