<template>
  <header class="site-header">
    <h2 class="logo">
      <RouterLink to="/">Student Portal</RouterLink>
    </h2>
    <nav class="nav-menu">
      <ul>
        <li><RouterLink to="/" active-class="active" exact-active-class="active">Courses</RouterLink></li>
        <li><RouterLink to="/profile" active-class="active">Profile</RouterLink></li>
      </ul>
    </nav>
    <div class="enroll-badge">
      <span>📚 Enrolled: <strong>{{ enrollmentStore.enrolledCount }}</strong></span>
    </div>
  </header>
</template>

<script setup>
import { RouterLink } from 'vue-router';
import { useEnrollmentStore } from '../stores/enrollment';

const enrollmentStore = useEnrollmentStore();
</script>
