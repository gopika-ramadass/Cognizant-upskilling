import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';
import type { Course } from '../types/course';
import { getAllCourses } from '../api/courseApi';
import type { RootState } from './store';

interface CoursesState {
  courses: Course[];
  loading: boolean;
  error: string | null;
}

const initialState: CoursesState = {
  courses: [],
  loading: false,
  error: null,
};

// =========================================================================
// Task 2: Async Thunk using createAsyncThunk
// =========================================================================
export const fetchAllCourses = createAsyncThunk<Course[], void, { rejectValue: string }>(
  'courses/fetchAll',
  async (_, { rejectWithValue }) => {
    try {
      const data = await getAllCourses();
      return data;
    } catch (err: any) {
      return rejectWithValue(err.message || 'Failed to fetch courses catalog');
    }
  }
);

const coursesSlice = createSlice({
  name: 'courses',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      // 1. Pending Action -> Set loading: true, clear error
      .addCase(fetchAllCourses.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      // 2. Fulfilled Action -> Populate courses array, set loading: false
      .addCase(fetchAllCourses.fulfilled, (state, action: PayloadAction<Course[]>) => {
        state.courses = action.payload;
        state.loading = false;
      })
      // 3. Rejected Action -> Store error message, set loading: false
      .addCase(fetchAllCourses.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload || 'An error occurred while fetching courses';
      });
  },
});

// Selectors decouple components from store shape
export const selectCourses = (state: RootState) => state.courses.courses;
export const selectCoursesLoading = (state: RootState) => state.courses.loading;
export const selectCoursesError = (state: RootState) => state.courses.error;

export default coursesSlice.reducer;
