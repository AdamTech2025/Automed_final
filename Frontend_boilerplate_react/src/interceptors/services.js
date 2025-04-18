import apiInstance from './axios.jsx';

// Dental scenario service
export const analyzeDentalScenario = async (scenarioData, signal) => {
  try {
    const response = await apiInstance.post('/api/analyze', scenarioData, {
      signal: signal // Pass the AbortController signal
    });
    return response.data;
  } catch (error) {
    // If request was aborted, rethrow the AbortError
    if (error.name === 'CanceledError' || error.name === 'AbortError') {
      const abortError = new Error('Request was cancelled');
      abortError.name = 'AbortError';
      throw abortError;
    }
    throw error.response?.data || { message: 'Failed to analyze scenario' };
  }
};

// Batch analyze multiple dental scenarios
export const analyzeBatchScenarios = async (scenariosArray, signal) => {
  try {
    const response = await apiInstance.post('/api/analyze-batch', {
      scenarios: scenariosArray
    }, {
      signal: signal // Pass the AbortController signal
    });
    return response.data;
  } catch (error) {
    // If request was aborted, rethrow the AbortError
    if (error.name === 'CanceledError' || error.name === 'AbortError') {
      const abortError = new Error('Request was cancelled');
      abortError.name = 'AbortError';
      throw abortError;
    }
    throw error.response?.data || { message: 'Failed to analyze scenarios in batch' };
  }
};

// Submit selected codes service
export const submitSelectedCodes = async (selectedCodes, recordId) => {
  try {
    const response = await apiInstance.post('/api/store-code-status', {
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
    console.log(`Submitting answers for record ID: ${recordId}`);
    console.log('Answers data:', answers);
    
    const response = await apiInstance.post(`/api/answer-questions/${recordId}`, {
      answers: JSON.stringify(answers)
    });
    
    console.log('Response received:', response.data);
    return response.data;
  } catch (error) {
    console.error('Error in submitQuestionAnswers:', error.response || error);
    throw error.response?.data || { message: 'Failed to submit answers: ' + (error.message || 'Unknown error') };
  }
};

// Add custom code service
export const addCustomCode = async (code, scenario, recordId) => {
  try {
    const response = await apiInstance.post('/api/add-custom-code', {
      code,
      scenario,
      record_id: recordId
    });
    return response.data;
  } catch (error) {
    throw error.response?.data || { message: 'Failed to add custom code' };
  }
};