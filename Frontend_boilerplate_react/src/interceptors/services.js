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