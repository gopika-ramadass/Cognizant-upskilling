import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

export const useEnrollmentStore = defineStore('enrollment', () => {
    // State
    const enrolledCourses = ref([]);

    // Computed (Getters)
    const totalCredits = computed(() =>
        enrolledCourses.value.reduce((sum, course) => sum + course.credits, 0)
    );

    const enrolledCount = computed(() => enrolledCourses.value.length);

    // Actions
    function enroll(course) {
        const exists = enrolledCourses.value.some(c => c.id === course.id);
        if (!exists) {
            enrolledCourses.value.push(course);
        }
    }

    function unenroll(courseId) {
        enrolledCourses.value = enrolledCourses.value.filter(c => c.id !== courseId);
    }

    function isEnrolled(courseId) {
        return enrolledCourses.value.some(c => c.id === courseId);
    }

    return { enrolledCourses, totalCredits, enrolledCount, enroll, unenroll, isEnrolled };
});
