import { defineStore } from 'pinia';
import authApi from '@/api/auth';
import api from '@/api/config';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: null,
    authStatus: false,
  }),
  getters: {
    isAuthenticated: (state) => state.authStatus,
  },
  actions: {
    async login(credentials) {
      try {
        const response = await authApi.login(credentials);
        this.token = response.data.token;
        this.user = response.data.user;
        this.authStatus = true;
        localStorage.setItem('token', this.token);
        return response.data;
      } catch (error) {
        console.error('Login failed:', error);
        throw error;
      }
    },
    logout() {
      this.user = null;
      this.authStatus = false;
      this.token = null;
      localStorage.removeItem('token');
    },
    async fetchUser() {
      try {
        const response = await api.get('/auth/user/');
        this.user = response.data;
        this.authStatus = true;
      } catch (error) {
        console.error('Failed to fetch user:', error);
        this.logout();
      }
    },
  },
});
