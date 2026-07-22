import { createRouter, createWebHashHistory } from 'vue-router';
import CoursesView from '../views/CoursesView.vue';
import CourseDetailView from '../views/CourseDetailView.vue';
import ProfileView from '../views/ProfileView.vue';

const routes = [
    { path: '/', component: CoursesView },
    { path: '/courses/:courseId', component: CourseDetailView },
    { path: '/profile', component: ProfileView },
];

const router = createRouter({
    history: createWebHashHistory(),
    routes
});

export default router;
