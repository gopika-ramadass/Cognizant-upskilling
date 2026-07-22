import axios from 'axios';

// =========================================================================
// HANDS-ON 10: Task 1 - Centralised API Client Configuration
// =========================================================================

// Configure single Axios instance with baseURL, default headers, and timeout
const apiClient = axios.create({
  baseURL: 'https://jsonplaceholder.typicode.com',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 5000, // 5 second timeout
});

// Request Interceptor: Attaches mock Authorization token & logs request
apiClient.interceptors.request.use(
  (config) => {
    // Attach hardcoded mock Authorization header
    config.headers.Authorization = 'Bearer mock-token-xyz';
    console.log(`[API Interceptor] API Request Started: ${config.method?.toUpperCase()} ${config.baseURL}${config.url}`);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response Interceptor: Returns data directly & standardises error objects
apiClient.interceptors.response.use(
  (response) => {
    // Return response.data directly so callers receive data instead of Axios wrapper
    return response.data;
  },
  (error) => {
    const statusCode = error.response ? error.response.status : 500;
    const message = error.response?.data?.message || error.message || 'An unexpected API error occurred';
    
    console.error(`[API Interceptor Error] Status: ${statusCode} - ${message}`);
    
    // Throw standardized Error object with message and statusCode
    return Promise.reject({
      message: `[API Error ${statusCode}]: ${message}`,
      statusCode,
    });
  }
);

export default apiClient;
