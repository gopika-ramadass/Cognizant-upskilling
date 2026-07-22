export interface Course {
  id: number;
  name: string;
  code: string;
  credits: number;
  grade: string;
  description?: string;
}

export interface ApiPost {
  userId: number;
  id: number;
  title: string;
  body: string;
}

export interface ApiError {
  message: string;
  statusCode?: number;
}
