import { createSlice } from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';
import type { Course } from './types/course';

interface EnrollmentState {
  enrolledCourses: Course[];
}

const initialState: EnrollmentState = {
  enrolledCourses: []
};

const enrollmentSlice = createSlice({
  name: 'enrollment',
  initialState,
  reducers: {
    enroll: (state, action: PayloadAction<Course>) => {
      const exists = state.enrolledCourses.some(
        (course) => course.id === action.payload.id
      );
      if (!exists) {
        state.enrolledCourses.push(action.payload);
      }
    },
    unenroll: (state, action: PayloadAction<number>) => {
      state.enrolledCourses = state.enrolledCourses.filter(
        (course) => course.id !== action.payload
      );
    }
  }
});

export const { enroll, unenroll } = enrollmentSlice.actions;
export default enrollmentSlice.reducer;
