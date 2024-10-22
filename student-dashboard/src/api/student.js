import api from './config';

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
};
