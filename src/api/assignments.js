import api from './api'

// ... other existing functions ...
    
export const getSubmission = async (assignmentId) => {
  try {
    const response = await api.get(`/assignments/${assignmentId}/submission`)
    return response.data
  } catch (error) {
    console.error('Error fetching submission:', error)
    throw error
  }
}
