<template>
  <div class="add-parent max-w-4xl mx-auto bg-white shadow-lg rounded-lg overflow-hidden">
    <!-- Improved Header -->
    <div class="header bg-gradient-to-r from-blue-500 to-blue-600 py-8 px-6 text-center">
      <h2 class="text-3xl font-bold text-white">Add Parent</h2>
      <p class="text-sm text-blue-100 mt-2">
        Fill out the form below to register a new parent and associate learners.
      </p>
    </div>

    <!-- Form -->
    <form @submit.prevent="submitForm" class="p-6 space-y-6">
      <!-- Parent Details -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- First Name -->
        <div class="form-group">
          <label for="first-name" class="block text-sm font-medium text-gray-700">First Name:</label>
          <input
            type="text"
            id="first-name"
            v-model="parent.first_name"
            required
            class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            placeholder="Enter first name"
          />
        </div>

        <!-- Last Name -->
        <div class="form-group">
          <label for="last-name" class="block text-sm font-medium text-gray-700">Last Name:</label>
          <input
            type="text"
            id="last-name"
            v-model="parent.last_name"
            required
            class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            placeholder="Enter last name"
          />
        </div>

        <!-- Email -->
        <div class="form-group">
          <label for="email" class="block text-sm font-medium text-gray-700">Email:</label>
          <input
            type="email"
            id="email"
            v-model="parent.email"
            required
            class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            placeholder="Enter email"
          />
        </div>

        <!-- Phone Number -->
        <div class="form-group">
          <label for="phone-number" class="block text-sm font-medium text-gray-700">Phone Number:</label>
          <input
            type="tel"
            id="phone-number"
            v-model="parent.phone_number"
            required
            class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            placeholder="Enter phone number"
          />
        </div>

        <!-- Address -->
        <div class="form-group md:col-span-2">
          <label for="address" class="block text-sm font-medium text-gray-700">Address:</label>
          <textarea
            id="address"
            v-model="parent.address"
            required
            class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            placeholder="Enter address"
          ></textarea>
        </div>

        <!-- Occupation -->
        <div class="form-group">
          <label for="occupation" class="block text-sm font-medium text-gray-700">Occupation:</label>
          <input
            type="text"
            id="occupation"
            v-model="parent.occupation"
            class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            placeholder="Enter occupation"
          />
        </div>

        <!-- Relationship to Learner -->
        <div class="form-group">
          <label for="relationship" class="block text-sm font-medium text-gray-700">Relationship to Learner:</label>
          <select
            id="relationship"
            v-model="parent.relationship_to_learner"
            required
            class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="Father">Father</option>
            <option value="Mother">Mother</option>
            <option value="Guardian">Guardian</option>
          </select>
        </div>
      </div>

      <!-- Learner Selection -->
      <div v-for="(learnerGroup, index) in learnerGroups" :key="index" class="learner-group p-6 border border-gray-200 rounded-lg bg-gray-50">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Select Grade -->
          <div class="form-group">
            <label :for="`grade-${index}`" class="block text-sm font-medium text-gray-700">Select Grade:</label>
            <select
              :id="`grade-${index}`"
              v-model="learnerGroup.grade"
              @change="fetchLearners(index)"
              required
              class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="">-- Select a grade --</option>
              <option v-for="grade in grades" :key="grade.id" :value="grade.id">
                {{ grade.grade_name }}
              </option>
            </select>
          </div>

          <!-- Select Learner -->
          <div class="form-group">
            <label :for="`learner-${index}`" class="block text-sm font-medium text-gray-700">Select Learner:</label>
            <select
              :id="`learner-${index}`"
              v-model="learnerGroup.learner"
              required
              class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="">-- Select a learner --</option>
              <option v-for="learner in learnerGroup.learners" :key="learner.id" :value="learner.id">
                {{ learner.name }} (ID: {{ learner.id }})
              </option>
            </select>
          </div>
        </div>

        <!-- Remove Learner Button -->
        <button
          type="button"
          @click="removeLearnerGroup(index)"
          class="mt-4 w-full bg-red-500 text-white py-2 px-4 rounded-md hover:bg-red-600 transition duration-200"
        >
          Remove Learner
        </button>
      </div>

      <!-- Add Another Learner Button -->
      <button
        type="button"
        @click="addLearnerGroup"
        class="w-full bg-green-500 text-white py-2 px-4 rounded-md hover:bg-green-600 transition duration-200"
      >
        Add Another Learner
      </button>

      <!-- Submit Button -->
      <button
        type="submit"
        class="w-full bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600 transition duration-200"
      >
        Add Parent
      </button>
    </form>

    <!-- Success/Error Message -->
    <div v-if="message" :class="['mt-6 p-4 rounded-md', message.type === 'success' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700']">
      {{ message.text }}
    </div>

    <!-- Loading Spinner -->
    <div v-if="loading" class="mt-6 flex justify-center">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      parent: {
        first_name: '',
        last_name: '',
        email: '',
        phone_number: '',
        address: '',
        occupation: '',
        relationship_to_learner: 'Father',
      },
      grades: [], // List of grades fetched from the backend
      learnerGroups: [
        {
          grade: '', // Selected grade
          learner: '', // Selected learner
          learners: [], // List of learners filtered by grade
        },
      ],
      message: null, // For success/error messages
      loading: false, // Loading state
    };
  },
  methods: {
    // Fetch grades from the backend
    async fetchGrades() {
      this.loading = true;
      try {
        const response = await axios.get('http://127.0.0.1:8000/parent_data/api/grades/');
        this.grades = response.data;
      } catch (error) {
        this.message = {
          type: 'error',
          text: 'Failed to fetch grades. Please try again.',
        };
        console.error('Error fetching grades:', error);
      } finally {
        this.loading = false;
      }
    },

    // Fetch learners based on the selected grade
    async fetchLearners(index) {
      const gradeId = this.learnerGroups[index].grade;
      if (!gradeId) {
        this.learnerGroups[index].learners = [];
        return;
      }

      this.loading = true;
      try {
        const response = await axios.get(`http://127.0.0.1:8000/parent_data/api/learners/?grade=${gradeId}`);
        if (Array.isArray(response.data)) {
          this.learnerGroups[index].learners = response.data;
        } else {
          throw new Error("Invalid response format: Expected an array of learners.");
        }
      } catch (error) {
        this.message = {
          type: 'error',
          text: 'Failed to fetch learners. Please check the grade and try again.',
        };
        console.error('Error fetching learners:', error);
      } finally {
        this.loading = false;
      }
    },

    // Add a new learner group
    addLearnerGroup() {
      this.learnerGroups.push({
        grade: '',
        learner: '',
        learners: [],
      });
    },

    // Remove a learner group
    removeLearnerGroup(index) {
      this.learnerGroups.splice(index, 1);
    },

    // Submit the form
    async submitForm() {
      this.loading = true;
      try {
        // Create the parent
        const parentResponse = await axios.post('http://127.0.0.1:8000/parent_data/api/parents/', this.parent);
        const parentId = parentResponse.data.id;

        // Associate learners with the parent
        const learnerPromises = this.learnerGroups
          .filter((group) => group.learner)
          .map((group) =>
            axios.post('http://127.0.0.1:8000/parent_data/api/parent-learner-relationships/', {
              parent: parentId,
              learner: group.learner,
            })
          );

        await Promise.all(learnerPromises);

        // Success message
        this.message = {
          type: 'success',
          text: 'Parent and learners added successfully!',
        };

        // Reset the form
        this.parent = {
          first_name: '',
          last_name: '',
          email: '',
          phone_number: '',
          address: '',
          occupation: '',
          relationship_to_learner: 'Father',
        };
        this.learnerGroups = [
          {
            grade: '',
            learner: '',
            learners: [],
          },
        ];
      } catch (error) {
        this.message = {
          type: 'error',
          text: 'Failed to add parent and learners. Please try again.',
        };
        console.error('Error:', error);
      } finally {
        this.loading = false;
      }
    },
  },
  mounted() {
    // Fetch grades when the component is mounted
    this.fetchGrades();
  },
};
</script>

<style scoped>
/* Add custom styles if needed */
</style>
