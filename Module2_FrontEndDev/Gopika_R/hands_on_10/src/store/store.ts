import { configureStore } from '@reduxjs/toolkit';
import coursesReducer from './coursesSlice';
import enrollmentReducer from './enrollmentSlice';

export const store = configureStore({
  reducer: {
    courses: coursesReducer,
    enrollment: enrollmentReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
