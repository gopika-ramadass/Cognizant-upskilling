import { createSlice } from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';
import type { Course } from '../types/course';
import type { RootState } from './store';

interface EnrollmentState {
  enrolledCourses: Course[];
}

const initialState: EnrollmentState = {
  enrolledCourses: [],
};

const enrollmentSlice = createSlice({
  name: 'enrollment',
  initialState,
  reducers: {
    enroll: (state, action: PayloadAction<Course>) => {
      const exists = state.enrolledCourses.some((c) => c.id === action.payload.id);
      if (!exists) {
        state.enrolledCourses.push(action.payload);
      }
    },
    unenroll: (state, action: PayloadAction<number>) => {
      state.enrolledCourses = state.enrolledCourses.filter((c) => c.id !== action.payload);
    },
  },
});

export const { enroll, unenroll } = enrollmentSlice.actions;

// Selector function for enrolled courses
export const selectEnrolledCourses = (state: RootState) => state.enrollment.enrolledCourses;

export default enrollmentSlice.reducer;
