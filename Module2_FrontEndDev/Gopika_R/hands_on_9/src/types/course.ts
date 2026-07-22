// ============================================================
// Core domain interfaces for the Student Portal
// ============================================================

export interface Course {
  id: number;
  name: string;
  code: string;
  credits: number;
  grade: string;
  description?: string; // optional — only available in detail view
}

export interface Profile {
  name: string;
  email: string;
  semester: string;
}

// API response shape from JSONPlaceholder
export interface Post {
  userId: number;
  id: number;
  title: string;
  body: string;
}
