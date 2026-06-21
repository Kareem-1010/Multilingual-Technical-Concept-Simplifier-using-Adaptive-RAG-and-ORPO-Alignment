import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const loginUser = async (username, password) => {
  const formData = new URLSearchParams();
  formData.append('username', username);
  formData.append('password', password);
  
  const response = await apiClient.post('/api/auth/login', formData, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
  });
  return response.data;
};

export const registerUser = async (username, password) => {
  const response = await apiClient.post('/api/auth/register', { username, password });
  return response.data;
};

export const simplifyText = async (payload) => {
  try {
    const response = await apiClient.post('/api/simplify', payload);
    return response.data;
  } catch (error) {
    if (error.response) {
      throw new Error(error.response.data.detail || 'Server error occurred');
    } else if (error.request) {
      throw new Error('Network error. Could not connect to the server.');
    } else {
      throw new Error('An unexpected error occurred.');
    }
  }
};

export const submitFeedback = async (payload) => {
  try {
    const response = await apiClient.post('/api/feedback', payload);
    return response.data;
  } catch (error) {
    console.error('Feedback submission failed', error);
    throw error;
  }
};

export const getHistory = async () => {
  try {
    const response = await apiClient.get('/api/history');
    return response.data;
  } catch (error) {
    console.error('Failed to fetch history', error);
    return [];
  }
};

export const healthCheck = async () => {
  try {
    const response = await apiClient.get('/api/health');
    return response.data;
  } catch (error) {
    return { status: 'down' };
  }
};
