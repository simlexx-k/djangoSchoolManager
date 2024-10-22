<template>
  <div class="user-profile">
    <h2>Learner Profile</h2>
    <div v-if="isLoading">Loading...</div>
    <div v-else-if="error">{{ error }}</div>
    <form v-else @submit.prevent="updateProfile">
      <div class="form-group">
        <label for="name">Name:</label>
        <input id="name" v-model="profile.name" type="text" required>
      </div>
      <div class="form-group">
        <label for="grade">Grade:</label>
        <select id="grade" v-model="profile.grade_id" required>
          <option v-for="grade in grades" :key="grade.id" :value="grade.id">
            {{ grade.grade_name }}
          </option>
        </select>
      </div>
      <div class="form-group">
        <label for="dob">Date of Birth:</label>
        <input id="dob" v-model="profile.date_of_birth" type="date" required>
      </div>
      <div class="form-group">
        <label for="gender">Gender:</label>
        <select id="gender" v-model="profile.gender" required>
          <option value="Male">Male</option>
          <option value="Female">Female</option>
        </select>
      </div>
      <div class="form-group">
        <label for="parent">Parent/Guardian Name:</label>
        <input id="parent" v-model="profile.name_of_parent" type="text" required>
      </div>
      <div class="form-group">
        <label for="parent_contact">Parent/Guardian Contact:</label>
        <input id="parent_contact" v-model="profile.parent_contact" type="tel" required>
      </div>
      <button type="submit" :disabled="isUpdating">Update Profile</button>
    </form>
    <div v-if="updateMessage" class="update-message">{{ updateMessage }}</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api/config'

const profile = ref({})
const grades = ref([])
const isLoading = ref(true)
const error = ref(null)
const isUpdating = ref(false)
const updateMessage = ref('')

const fetchProfile = async () => {
  try {
    const response = await api.get('/learner/profile/')
    profile.value = response.data
    isLoading.value = false
  } catch (err) {
    console.error('Error fetching learner profile:', err)
    error.value = 'Failed to load learner profile. Please try again.'
    isLoading.value = false
  }
}

const fetchGrades = async () => {
  try {
    const response = await api.get('/grades/') // Assuming you have an API endpoint for grades
    grades.value = response.data
  } catch (err) {
    console.error('Error fetching grades:', err)
  }
}

const updateProfile = async () => {
  isUpdating.value = true
  updateMessage.value = ''
  try {
    await api.put('/learner/profile/', profile.value)
    updateMessage.value = 'Profile updated successfully!'
  } catch (err) {
    console.error('Error updating learner profile:', err)
    updateMessage.value = 'Failed to update profile. Please try again.'
  } finally {
    isUpdating.value = false
  }
}

onMounted(async () => {
  await Promise.all([fetchProfile(), fetchGrades()])
})
</script>

<style scoped>
.user-profile {
  max-width: 500px;
  margin: 0 auto;
  padding: 20px;
}
.form-group {
  margin-bottom: 15px;
}
label {
  display: block;
  margin-bottom: 5px;
}
input, textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}
button {
  background-color: #4A90E2;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
button:disabled {
  background-color: #ccc;
}
.update-message {
  margin-top: 15px;
  padding: 10px;
  background-color: #e6f3ff;
  border: 1px solid #b3d7ff;
  border-radius: 4px;
}
</style>
