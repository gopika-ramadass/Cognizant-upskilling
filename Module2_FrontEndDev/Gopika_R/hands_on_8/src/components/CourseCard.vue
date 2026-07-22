<template>
  <article class="course-card" :class="{ enrolled: isEnrolled }">
    <h3>{{ course.name }}</h3>
    <p>Course Code: <strong>{{ course.code }}</strong></p>
    <div class="card-meta">
      <span class="credits-tag">Credits: {{ course.credits }}</span>
      <span class="grade-tag">Grade: {{ course.grade }}</span>
    </div>
    <div class="card-actions">
      <button
        :disabled="isEnrolled"
        :class="isEnrolled ? 'btn-disabled' : 'btn-enroll'"
        class="enroll-btn"
        @click="$emit('enroll', course.id)"
      >
        {{ isEnrolled ? '✓ Enrolled' : 'Enroll' }}
      </button>
      <RouterLink :to="`/courses/${course.id}`" class="btn-details">Details</RouterLink>
    </div>
  </article>
</template>

<script setup>
import { RouterLink } from 'vue-router';

defineProps({
  course: { type: Object, required: true },
  isEnrolled: { type: Boolean, default: false }
});

defineEmits(['enroll']);
</script>
