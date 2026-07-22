<template>
  <div class="profile-page">
    <!-- Student Profile Form -->
    <section class="profile-section">
      <h2>Student Profile</h2>
      <div class="profile-container">
        <form class="profile-form" @submit.prevent>
          <div class="form-group">
            <label for="profile-name">Full Name</label>
            <input id="profile-name" v-model="profile.name" type="text" placeholder="Enter full name" />
          </div>
          <div class="form-group">
            <label for="profile-email">Email Address</label>
            <input id="profile-email" v-model="profile.email" type="email" placeholder="Enter email address" />
          </div>
          <div class="form-group">
            <label for="profile-semester">Current Semester</label>
            <input id="profile-semester" v-model.number="profile.semester" type="number" min="1" max="8" placeholder="Semester" />
          </div>
        </form>

        <!-- Live Profile Card Preview -->
        <div class="profile-card-preview">
          <div class="avatar-placeholder">
            {{ initials }}
          </div>
          <div class="preview-details">
            <h3>{{ profile.name || 'Student Name' }}</h3>
            <p class="email-text">📧 {{ profile.email || 'student@example.com' }}</p>
            <p class="sem-text">Semester <strong>{{ profile.semester || '-' }}</strong></p>
          </div>
        </div>
      </div>
    </section>

    <!-- Enrolled Courses List -->
    <section class="enrolled-section">
      <h2>Enrolled Courses</h2>

      <p v-if="enrollmentStore.enrolledCourses.length === 0" class="no-results">
        No courses enrolled yet. Go to the
        <RouterLink to="/">course catalog</RouterLink> to enroll.
      </p>

      <ul v-else class="enrolled-list">
        <li
          v-for="course in enrollmentStore.enrolledCourses"
          :key="course.id"
          class="enrolled-item"
        >
          <div>
            <h4>{{ course.name }}</h4>
            <p>Code: <strong>{{ course.code }}</strong> | Credits: <strong>{{ course.credits }}</strong></p>
          </div>
          <button class="btn-remove" @click="enrollmentStore.unenroll(course.id)">Remove</button>
        </li>
      </ul>

      <div v-if="enrollmentStore.enrolledCourses.length > 0" class="credits-summary">
        Total Credits: <strong>{{ enrollmentStore.totalCredits }}</strong>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { RouterLink } from 'vue-router';
import { useEnrollmentStore } from '../stores/enrollment';

const enrollmentStore = useEnrollmentStore();

// Reactive profile state (Composition API)
const profile = ref({
  name: 'Gopika R',
  email: 'gopika.r@example.com',
  semester: 6
});

// Computed initials for avatar
const initials = computed(() => {
  if (!profile.value.name) return 'S';
  return profile.value.name
    .split(' ')
    .map(n => n[0])
    .join('')
    .toUpperCase()
    .slice(0, 2);
});
</script>
