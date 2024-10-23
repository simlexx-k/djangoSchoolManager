import api from './config';
import axios from 'axios';

export default {
  getDashboard(studentId = null) {
    const url = studentId ? `student/dashboard/${studentId}/` : 'student/dashboard/';
    return api.get(url);
  },
  getExamResults(studentId = null, params = {}) {
    const url = studentId ? `student/exam-results/${studentId}/` : 'student/exam-results/';
    return api.get(url, { params });
  },
  getAttendance(studentId = null, params = {}) {
    const url = studentId ? `student/attendance/${studentId}/` : 'student/attendance/';
    return api.get(url, { params });
  },
  getFees(studentId = null) {
    const url = studentId ? `student/fees/${studentId}/` : 'student/fees/';
    return api.get(url);
  },
  getTimetable(studentId = null) {
    const url = studentId ? `student/timetable/${studentId}/` : 'student/timetable/';
    return api.get(url);
  },
  // New method for fetching exams
  getExams(studentId = null, params = {}) {
    const url = studentId ? `student/exam-results/${studentId}/` : 'student/exam-results/';
    return api.get(url, { params });
  },
  // New method for fetching assignments
  getAssignments(studentId = null, params = {}) {
    const url = studentId ? `student/assignments/${studentId}/` : 'student/assignments/';
    return api.get(url, { params });
  },
  // New method for fetching a single exam's details
  getExamDetails(examId) {
    return api.get(`student/exam-results/${examId}/`);
  },
  // New method for fetching a single assignment's details
  getAssignmentDetails(assignmentId) {
    return api.get(`student/assignments/${assignmentId}/`);
  },
  // You can add more methods here as needed

  getAssignment(id) {
    return api.get(`student/assignments/${id}/`);
  },

  submitAssignment(id, data) {
    return api.post(`student/assignments/${id}/submit/`, data);
  },
  async getSubmission(assignmentId) {
    try {
      const response = await api.get(`student/assignments/${assignmentId}/submission/`)
      return response.data
    } catch (error) {
      console.error('Error fetching submission:', error)
      throw error
    }
  }
};
