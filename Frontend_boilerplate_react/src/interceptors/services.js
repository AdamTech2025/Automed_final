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
export const submitSelectedCodes = async (payload, recordId) => {
  try {
    // Prepare the API request payload
    const apiPayload = {
      record_id: recordId,
      cdt_codes: payload.cdt_codes || [],
      rejected_cdt_codes: payload.rejected_cdt_codes || [],
      icd_codes: payload.icd_codes || [],
      rejected_icd_codes: payload.rejected_icd_codes || []
    };

    // Log the payload being sent
    console.log("Sending payload to /api/store-code-status:", apiPayload);

    const response = await apiInstance.post('/api/store-code-status', apiPayload);
    return response.data;
  } catch (error) {
    console.error("Error in submitSelectedCodes:", error.response || error);
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
export const addCustomCode = async (code, scenario, recordId, codeType) => {
  try {
    const response = await apiInstance.post('/api/add-custom-code', {
      code,
      scenario,
      record_id: recordId,
      code_type: codeType
    });
    return response.data;
  } catch (error) {
    throw error.response?.data || { message: 'Failed to add custom code' };
  }
};

// --- Authentication Services ---

export const sendSignupOtp = async (userData) => {
  try {
    // userData should contain { name, email, phone }
    const response = await apiInstance.post('/api/auth/signup/send-otp', userData);
    return response.data; // Expected: { message: "...", user_id: "..." }
  } catch (error) {
    // Throw the specific error message from the backend if available
    throw error.response?.data || { message: 'Failed to send OTP' };
  }
};

export const verifySignupOtp = async (verificationData) => {
  try {
    // verificationData should contain { email, otp }
    const response = await apiInstance.post('/api/auth/signup/verify-otp', verificationData);
    return response.data; // Expected: { message: "...", user_id: "..." }
  } catch (error) {
    throw error.response?.data || { message: 'Failed to verify OTP' };
  }
};

// Placeholder for Login service (implement when backend route is ready)
export const loginUser = async (credentials) => {
  try {
    console.log("services.js: Attempting login for:", credentials.email);
    // credentials should contain { email, password }
    const response = await apiInstance.post('/api/auth/login', credentials);
    console.log("services.js: Received API response:", response.data);
    // Expected response: { access_token: "...", token_type: "bearer", name: "...", email: "..." }
    
    // Store the token and user details upon successful login
    if (response.data && response.data.access_token) {
      console.log("services.js: Access token found. Storing data...");
      localStorage.setItem('accessToken', response.data.access_token);
      console.log("services.js: Stored accessToken.");
      localStorage.setItem('user', JSON.stringify({ 
        name: response.data.name, 
        email: response.data.email 
      }));
      console.log("services.js: Stored user data:", { name: response.data.name, email: response.data.email });
    } else {
      console.warn("services.js: No access token found in response.");
    }
    
    return response.data; 
  } catch (error) {
     console.error("Login error:", error);
    // Throw a structured error similar to other services
    // Use detail if available (FastAPI validation errors often use this)
    throw error.response?.data || { message: 'Login failed', detail: 'Could not connect or unexpected error' };
  }
};

// --- Admin Services ---

export const getAllUsersActivity = async (signal) => {
  try {
    console.log("services.js: Attempting to fetch all user activity (Admin)");
    const response = await apiInstance.get('/api/admin/all-users', {
      signal: signal // Pass the AbortController signal
    });
    console.log("services.js: Received all users activity response:", response.data);
    // Expected response: { users: [ { id, name, email, phone, is_email_verified, created_at, role, analysis_count }, ... ] }
    return response.data;
  } catch (error) {
    console.error("Get All Users Activity error:", error);
    if (error.name === 'CanceledError' || error.name === 'AbortError') {
      const abortError = new Error('Request was cancelled');
      abortError.name = 'AbortError';
      throw abortError;
    }
    // Rethrow specific backend error or a generic one
    throw error.response?.data || { message: 'Failed to fetch user activity', detail: 'Could not connect or permission denied' };
  }
};

// Get activity for a specific user
export const getUserActivity = async (userId, signal) => {
  try {
    console.log(`services.js: Attempting to fetch activity for user ID: ${userId}`);
    const response = await apiInstance.get(`/api/admin/user/${userId}/activity`, {
      signal: signal // Pass the AbortController signal
    });
    console.log(`services.js: Received activity for user ${userId}:`, response.data);
    return response.data;
  } catch (error) {
    // Don't log or propagate canceled request errors
    if (error.name === 'CanceledError' || error.name === 'AbortError') {
      console.log(`Request for user ${userId} was canceled due to component unmount or navigation`);
      const abortError = new Error('Request was cancelled');
      abortError.name = 'AbortError';
      throw abortError;
    }
    
    // Log and propagate other errors
    console.error(`Get User Activity (ID: ${userId}) error:`, error);
    throw error.response?.data || { message: `Failed to fetch activity for user ${userId}`, detail: 'Could not connect or permission denied' };
  }
};

// --- Admin Prompt Management Services ---

export const getTopicsPrompts = async (signal) => {
  try {
    console.log("services.js: Attempting to fetch all topic prompts (Admin)");
    const response = await apiInstance.get('api/prompts/topics_prompts', {
      signal: signal // Pass the AbortController signal
    });
    console.log("services.js: Received topic prompts response:", response.data);
    // Expected response structure: { topics: [ { id, name, template, version, created_at }, ... ] }
    return response.data;
  } catch (error) {
    console.error("Get Topics Prompts error:", error);
    if (error.name === 'CanceledError' || error.name === 'AbortError') {
      const abortError = new Error('Request was cancelled');
      abortError.name = 'AbortError';
      throw abortError;
    }
    // Rethrow specific backend error or a generic one
    throw error.response?.data || { message: 'Failed to fetch topic prompts', detail: 'Could not connect or permission denied' };
  }
};

export const updateTopicPrompt = async (topicId, template, signal) => {
  try {
    console.log(`services.js: Attempting to update prompt for topic ID: ${topicId}`);
    const response = await apiInstance.put(`/api/prompts/topics_prompts/${topicId}`, 
      { template: template }, // Send only the template in the body
      {
        signal: signal // Pass the AbortController signal
      }
    );
    console.log(`services.js: Received update response for topic ${topicId}:`, response.data);
    // Expected response could be the updated topic or a success message
    return response.data; 
  } catch (error) {
    console.error(`Update Topic Prompt (ID: ${topicId}) error:`, error);
    if (error.name === 'CanceledError' || error.name === 'AbortError') {
      const abortError = new Error('Request was cancelled');
      abortError.name = 'AbortError';
      throw abortError;
    }
    // Rethrow specific backend error or a generic one
    throw error.response?.data || { message: `Failed to update prompt for topic ${topicId}`, detail: 'Could not connect or permission denied' };
  }
};

// File upload and extraction service
export const uploadAndExtract = async (file) => {
  try {
    const formData = new FormData();
    formData.append('file', file);

    const response = await apiInstance.post('/api/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    console.error('Upload error:', error);
    throw error.response?.data || { message: 'Failed to process file' };
  }
};

// Update user rules (Admin)
export const updateUserRules = async (userId, rules, signal) => {
  try {
    console.log(`services.js: Attempting to update rules for user ID: ${userId}`);
    const response = await apiInstance.post(`/api/admin/user/${userId}/update-rules`, 
      { rules }, // Send rules in the request body
      {
        signal: signal // Pass the AbortController signal
      }
    );
    console.log(`services.js: Successfully updated rules for user ${userId}`);
    return response.data;
  } catch (error) {
    console.error(`Update User Rules (ID: ${userId}) error:`, error);
    if (error.name === 'CanceledError' || error.name === 'AbortError') {
      const abortError = new Error('Request was cancelled');
      abortError.name = 'AbortError';
      throw abortError;
    }
    throw error.response?.data || { message: `Failed to update rules for user ${userId}`, detail: 'Could not connect or permission denied' };
  }
};