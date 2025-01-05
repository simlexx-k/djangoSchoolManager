import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/dashboard/',
  withCredentials: true,
});

// Add this function to get the CSRF token from cookies
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Add this interceptor to include the CSRF token in requests
api.interceptors.request.use(function (config) {
  config.headers['X-CSRFToken'] = getCookie('csrftoken');
  return config;
}, function (error) {
  return Promise.reject(error);
});

export default api;

export const registerStudent = (data) => api.post('/register/student/', data);
export const registerParent = (data) => api.post('/register/parent/', data);
export const getClassLevels = () => api.get('/class-levels/');
export const getStudents = (classLevel) => api.get('/students/', { params: { class_level: classLevel } });
