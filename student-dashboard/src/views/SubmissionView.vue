<template>
  <div class="submission-view">
    <v-container>
      <v-row justify="center">
        <v-col cols="12" md="8">
          <v-card class="elevation-3">
            <v-card-title class="text-h4 font-weight-bold primary white--text py-4">
              Assignment Submission
            </v-card-title>
            <v-card-text>
              <v-progress-circular
                v-if="loading"
                indeterminate
                color="primary"
                size="64"
                class="ma-4"
              ></v-progress-circular>
              
              <v-alert v-else-if="error" type="error" class="mt-4">
                {{ error }}
              </v-alert>
              
              <template v-else-if="submission">
                <v-list>
                  <v-list-item>
                    <v-list-item-content>
                      <v-list-item-title class="text-subtitle-1">Submitted on</v-list-item-title>
                      <v-list-item-subtitle>{{ formatDate(submission.submitted_at) }}</v-list-item-subtitle>
                    </v-list-item-content>
                  </v-list-item>
                  <v-divider></v-divider>
                  <v-list-item>
                    <v-list-item-content>
                      <v-list-item-title class="text-subtitle-1">Status</v-list-item-title>
                      <v-list-item-subtitle>
                        <v-chip :color="getStatusColor(submission.status)" small>
                          {{ submission.status }}
                        </v-chip>
                      </v-list-item-subtitle>
                    </v-list-item-content>
                  </v-list-item>
                  <v-divider></v-divider>
                  <v-list-item>
                    <v-list-item-content>
                      <v-list-item-title class="text-subtitle-1">Score</v-list-item-title>
                      <v-list-item-subtitle>
                        <v-chip v-if="submission.score !== null" color="success" small>
                          {{ submission.score }}
                        </v-chip>
                        <v-chip v-else color="warning" small>
                          Not graded yet
                        </v-chip>
                      </v-list-item-subtitle>
                    </v-list-item-content>
                  </v-list-item>
                </v-list>

                <v-expansion-panels v-if="submission.question_responses && submission.question_responses.length > 0" class="mt-6">
                  <v-expansion-panel
                    v-for="(response, index) in submission.question_responses"
                    :key="index"
                  >
                    <v-expansion-panel-header>
                      Question {{ index + 1 }}
                    </v-expansion-panel-header>
                    <v-expansion-panel-content>
                      <v-card flat>
                        <v-card-text>
                          <p class="text-subtitle-1 font-weight-bold">Question:</p>
                          <p>{{ response.question }}</p>
                          <p class="text-subtitle-1 font-weight-bold mt-4">Your Answer:</p>
                          <p>{{ response.answer }}</p>
                          <v-chip
                            v-if="response.is_correct !== null"
                            :color="response.is_correct ? 'success' : 'error'"
                            class="mt-2"
                            small
                          >
                            {{ response.is_correct ? 'Correct' : 'Incorrect' }}
                          </v-chip>
                          <p v-if="response.score !== null" class="mt-2">
                            <strong>Score:</strong> {{ response.score }}
                          </p>
                        </v-card-text>
                      </v-card>
                    </v-expansion-panel-content>
                  </v-expansion-panel>
                </v-expansion-panels>
                <v-alert v-else type="info" class="mt-4">
                  No question responses found.
                </v-alert>
              </template>
              
              <v-alert v-else type="warning" class="mt-4">
                No submission found.
              </v-alert>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import studentApi from '@/api/student'

const route = useRoute()
const submission = ref(null)
const loading = ref(true)
const error = ref(null)

onMounted(async () => {
  try {
    const assignmentId = route.params.id
    submission.value = await studentApi.getSubmission(assignmentId)
    loading.value = false
  } catch (err) {
    error.value = 'Failed to load submission. Please try again.'
    loading.value = false
    console.error('Error fetching submission:', err)
  }
})

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleString()
}

const getStatusColor = (status) => {
  switch (status.toLowerCase()) {
    case 'submitted':
      return 'info'
    case 'graded':
      return 'success'
    default:
      return 'warning'
  }
}
</script>

<style scoped>
.submission-view {
  min-height: 100vh;
  background-color: #f5f5f5;
}
</style>
