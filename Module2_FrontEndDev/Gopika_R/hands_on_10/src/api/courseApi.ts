import apiClient from './apiClient';
import type { Course, ApiPost } from '../types/course';

// =========================================================================
// HANDS-ON 10: Task 1 - Course API Service Layer Functions
// =========================================================================

/**
 * Fetch all available courses from API and map posts to course objects
 */
export async function getAllCourses(): Promise<Course[]> {
  // apiClient interceptor automatically returns response.data (array of posts)
  const posts = (await apiClient.get('/posts?_limit=5')) as ApiPost[];

  return posts.map((post) => ({
    id: post.id,
    name: post.title
      .split(' ')
      .slice(0, 3)
      .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
      .join(' '),
    code: `CS10${post.id}`,
    credits: post.id % 2 === 0 ? 4 : 3,
    grade: ['A', 'B', 'A+', 'B+', 'A'][post.id % 5],
    description: post.body,
  }));
}

/**
 * Fetch a single course by ID
 */
export async function getCourseById(id: number): Promise<Course> {
  const post = (await apiClient.get(`/posts/${id}`)) as ApiPost;
  return {
    id: post.id,
    name: post.title
      .split(' ')
      .slice(0, 3)
      .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
      .join(' '),
    code: `CS10${post.id}`,
    credits: post.id % 2 === 0 ? 4 : 3,
    grade: ['A', 'B', 'A+', 'B+', 'A'][post.id % 5],
    description: post.body,
  };
}

/**
 * Simulate student enrollment via API POST request
 */
export async function enrollStudent(studentId: number, courseId: number): Promise<{ success: boolean; message: string }> {
  await apiClient.post('/posts', {
    studentId,
    courseId,
    enrolledAt: new Date().toISOString(),
  });
  return {
    success: true,
    message: `Student ${studentId} successfully enrolled in course ${courseId}`,
  };
}
