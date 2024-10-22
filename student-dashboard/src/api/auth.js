import api from './config';

export default {
  login(credentials) {
    return api.post('student-parent/login/', credentials);
  },
  logout() {
    return api.post('student-parent/logout/');
  },
  getProfile() {
    return api.get('user/profile/');
  },
};

