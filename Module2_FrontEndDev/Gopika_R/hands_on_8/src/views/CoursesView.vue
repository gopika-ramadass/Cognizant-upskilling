<template>
  <section class="courses-section">
    <h2>Available Courses</h2>

    <!-- Search Input -->
    <div class="search-bar-container">
      <input
        v-model="searchTerm"
        type="text"
        class="search-input"
        placeholder="🔍 Search courses by name..."
      />
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loader-container">
      <div class="spinner"></div>
      <p>Loading course catalog...</p>
    </div>

    <!-- Error State -->
    <div v-if="error" class="error-banner">
      <p>⚠️ {{ error }}</p>
    </div>

    <!-- No results -->
    <p v-if="!loading && !error && filteredCourses.length === 0" class="no-results">
      No courses match your search.
    </p>

    <!-- Course Grid -->
    <div v-if="!loading && !error && filteredCourses.length > 0" class="course-grid">
      <CourseCard
        v-for="course in filteredCourses"
        :key="course.id"
        :course="course"
        :is-enrolled="enrollmentStore.isEnrolled(course.id)"
        @enroll="handleEnroll"
      />
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import CourseCard from '../components/CourseCard.vue';
import { useEnrollmentStore } from '../stores/enrollment';

const router = useRouter();
const enrollmentStore = useEnrollmentStore();

const courses = ref([]);
const searchTerm = ref('');
const loading = ref(true);
const error = ref(null);

// Fetch courses on mount (lifecycle hook equivalent)
onMounted(async () => {
  try {
    const response = await fetch('https://jsonplaceholder.typicode.com/posts?_limit=5');
    if (!response.ok) throw new Error(`HTTP Error: ${response.status}`);
    const data = await response.json();

    courses.value = data.map(post => ({
      id: post.id,
      name: post.title.split(' ').slice(0, 3).map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' '),
      code: `CS${100 + post.id}`,
      credits: post.id % 2 === 0 ? 4 : 3,
      grade: ['A', 'B', 'A+', 'B+', 'A'][post.id % 5]
    }));
  } catch (err) {
    error.value = `Failed to load courses: ${err.message}`;
  } finally {
    loading.value = false;
  }
});

// Computed filtering (reactive)
const filteredCourses = computed(() =>
  courses.value.filter(c =>
    c.name.toLowerCase().includes(searchTerm.value.toLowerCase())
  )
);

// Enroll action dispatches to Pinia store and navigates to profile
function handleEnroll(courseId) {
  const course = courses.value.find(c => c.id === courseId);
  if (course) {
    enrollmentStore.enroll(course);
    router.push('/profile');
  }
}
</script>
