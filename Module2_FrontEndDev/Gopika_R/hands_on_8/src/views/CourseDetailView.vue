<template>
  <section class="course-detail-section">
    <RouterLink to="/" class="btn-back">← Back to Courses</RouterLink>

    <div v-if="loading" class="loader-container">
      <div class="spinner"></div>
      <p>Loading course details...</p>
    </div>

    <div v-if="error" class="error-banner">
      <p>⚠️ {{ error }}</p>
    </div>

    <div v-if="!loading && !error && course" class="course-detail-container">
      <h2>{{ course.name }}</h2>
      <p class="detail-meta">
        Code: <strong>{{ course.code }}</strong> &nbsp;|&nbsp;
        Credits: <strong>{{ course.credits }}</strong> &nbsp;|&nbsp;
        Grade: <strong>{{ course.grade }}</strong>
      </p>

      <div class="detail-body">
        <h4>Syllabus Description</h4>
        <p>{{ course.description }}</p>
      </div>

      <button
        @click="handleEnroll"
        :disabled="isEnrolled"
        :class="isEnrolled ? 'btn-disabled btn-enroll' : 'btn-primary'"
        class="enroll-btn-lg"
      >
        {{ isEnrolled ? '✓ Already Enrolled' : 'Enroll in Course' }}
      </button>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter, RouterLink } from 'vue-router';
import { useEnrollmentStore } from '../stores/enrollment';

const route = useRoute();
const router = useRouter();
const enrollmentStore = useEnrollmentStore();

const course = ref(null);
const loading = ref(true);
const error = ref(null);

// Computed: check enrollment status reactively
const isEnrolled = computed(() =>
  course.value ? enrollmentStore.isEnrolled(course.value.id) : false
);

// Fetch details using route params
onMounted(async () => {
  const courseId = route.params.courseId;
  try {
    const response = await fetch(`https://jsonplaceholder.typicode.com/posts/${courseId}`);
    if (!response.ok) throw new Error(`Course not found (${response.status})`);
    const post = await response.json();

    const idNum = parseInt(courseId, 10);
    course.value = {
      id: post.id,
      name: post.title.split(' ').slice(0, 3).map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' '),
      code: `CS${100 + idNum}`,
      credits: idNum % 2 === 0 ? 4 : 3,
      grade: ['A', 'B', 'A+', 'B+', 'A'][idNum % 5],
      description: post.body
    };
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
});

function handleEnroll() {
  if (course.value) {
    enrollmentStore.enroll(course.value);
    router.push('/profile');
  }
}
</script>
