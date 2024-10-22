<!-- src/views/RegistrationView.vue -->
<template>
  <div class="registration">
    <h2>Student Registration</h2>
    <form @submit.prevent="register">
      <div>
        <label for="grade-select">Select Grade:</label>
        <select id="grade-select" v-model="selectedGradeId" @change="fetchStudents">
          <option value="">Please select a grade</option>
          <option v-for="grade in grades" :key="grade.id" :value="grade.id">
            {{ grade.grade_name }}
          </option>
        </select>
      </div>

      <div v-if="students.length > 0">
        <label for="student-select">Select Student:</label>
        <select id="student-select" v-model="selectedLearnerId">
          <option value="">Please select a student</option>
          <option v-for="student in students" :key="student.learner_id" :value="student.learner_id">
            {{ student.name }}
          </option>
        </select>
      </div>

      <div>
        <label for="username">Username:</label>
        <input id="username" v-model="username" placeholder="Enter username" required>
      </div>

      <div>
        <label for="password">Password:</label>
        <input id="password" v-model="password" type="password" placeholder="Enter password" required>
      </div>

      <button type="submit" :disabled="!isFormValid">Register</button>
    </form>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import api from '@/api/config';

export default {
  setup() {
    const grades = ref([]);
    const students = ref([]);
    const selectedGradeId = ref('');
    const selectedLearnerId = ref('');
    const username = ref('');
    const password = ref('');

    const fetchGrades = async () => {
      try {
        const response = await api.get('/grades/');
        grades.value = response.data;
      } catch (error) {
        console.error('Error fetching grades:', error);
        alert('Failed to fetch grades. Please try again.');
      }
    };

    const fetchStudents = async () => {
      if (selectedGradeId.value) {
        try {
          const response = await api.get('/students/', { params: { grade_id: selectedGradeId.value } });
          students.value = response.data;
        } catch (error) {
          console.error('Error fetching students:', error);
          alert('Failed to fetch students. Please try again.');
        }
      } else {
        students.value = [];
      }
    };

    const register = async () => {
      if (!isFormValid.value) return;

      try {
        await api.post('/register/student/', {
          grade_id: selectedGradeId.value,
          learner_id: selectedLearnerId.value,
          username: username.value,
          password: password.value,
        });
        alert('Registration successful!');
        // Redirect to login or dashboard
      } catch (error) {
        console.error('Registration failed:', error);
        if (error.response?.data?.error === "Username already exists") {
          alert('This username is already taken. Please choose a different one.');
        } else if (error.response?.data?.error === "Student record not found") {
          alert('No matching student record found. Please check your details.');
        } else if (error.response?.data?.error === "This student already has an account") {
          alert('An account already exists for this student. Please log in instead.');
        } else {
          alert('Registration failed: ' + (error.response?.data?.error || 'Unknown error'));
        }
      }
    };

    const isFormValid = computed(() => {
      return selectedGradeId.value && 
             selectedLearnerId.value && 
             username.value.trim() !== '' && 
             password.value.trim() !== '';
    });

    onMounted(fetchGrades);

    return {
      grades,
      students,
      selectedGradeId,
      selectedLearnerId,
      username,
      password,
      fetchStudents,
      register,
      isFormValid
    };
  },
};
</script>

<style scoped>
/* ... (styles remain the same) ... */
</style>
