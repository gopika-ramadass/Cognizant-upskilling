import { createSlice } from '@reduxjs/toolkit';

const enrollmentSlice = createSlice({
    name: 'enrollment',
    initialState: {
        enrolledCourses: [] // Stores course objects
    },
    reducers: {
        enroll: (state, action) => {
            // action.payload is the course object. Avoid duplicate enrollment.
            const exists = state.enrolledCourses.some(course => course.id === action.payload.id);
            if (!exists) {
                state.enrolledCourses.push(action.payload);
            }
        },
        unenroll: (state, action) => {
            // action.payload is the course ID
            state.enrolledCourses = state.enrolledCourses.filter(course => course.id !== action.payload);
        }
    }
});

export const { enroll, unenroll } = enrollmentSlice.actions;
export default enrollmentSlice.reducer;
