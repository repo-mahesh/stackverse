import axios from "axios";

// Create an axios instance with default settings
const axiosInstance = axios.create({
    baseURL: "http://127.0.0.1:8000", // Replace with your backend URL
    withCredentials: true, // Ensures that cookies (JWT) are sent with requests
});

// Optional: Add request interceptor to handle any global settings, such as adding headers
axiosInstance.interceptors.request.use(
    (config) => {
        // You can add headers here if needed (e.g., Authorization)
        // const token = localStorage.getItem("access_token");
        // if (token) {
        //     config.headers["Authorization"] = `Bearer ${token}`;
        // }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Optional: Add response interceptor to handle errors or token refresh logic
axiosInstance.interceptors.response.use(
    (response) => response,
    (error) => {
        // Handle response errors globally (e.g., token expiry)
        if (error.response?.status === 401) {
            // Handle token expiry or unauthorized access
        }
        return Promise.reject(error);
    }
);

export default axiosInstance;
