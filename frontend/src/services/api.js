import axios from 'axios';

export const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1',
});

// Add a request interceptor
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Add a response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle 401 Unauthorized errors
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Document API
export const documentApi = {
  getAll: (params) => api.get('/documents/', { params }),
  get: (id) => api.get(`/documents/${id}`),
  upload: (formData) => api.post('/documents/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  }),
  delete: (id) => api.delete(`/documents/${id}`),
};

// Query API
export const queryApi = {
  create: (data) => api.post('/queries/', data),
  getAll: (params) => api.get('/queries/', { params }),
  get: (id) => api.get(`/queries/${id}`),
  update: (id, data) => api.put(`/queries/${id}`, data),
  delete: (id) => api.delete(`/queries/${id}`),
}; 