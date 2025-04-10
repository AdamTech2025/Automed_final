import apiInstance from './axios.jsx';

// Dental scenario service
export const analyzeDentalScenario = async (scenarioData) => {
  try {
    const response = await apiInstance.post('/api/analyze', scenarioData);
    return response.data;
  } catch (error) {
    throw error.response?.data || { message: 'Failed to analyze scenario' };
  }
};

// Submit selected codes service
export const submitSelectedCodes = async (selectedCodes, recordId) => {
  try {
    const response = await apiInstance.post('/api/submit-codes', {
      ...selectedCodes,
      record_id: recordId
    });
    return response.data;
  } catch (error) {
    throw error.response?.data || { message: 'Failed to submit selected codes' };
  }
};

// Submit answers to questions service
export const submitQuestionAnswers = async (answers, recordId) => {
  try {
    const response = await apiInstance.post(`/answer-questions/${recordId}`, {
      answers: JSON.stringify(answers)
    });
    return response.data;
  } catch (error) {
    throw error.response?.data || { message: 'Failed to submit answers' };
  }
};