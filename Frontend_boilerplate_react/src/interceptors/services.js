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
    // selectedCodes is expected to have { accepted: [...], denied: [...] } structure
    // Transform it to match the backend model CodeStatusRequest
    const payload = {
      record_id: recordId,
      cdt_codes: selectedCodes.accepted || [], // Map accepted to cdt_codes
      rejected_cdt_codes: selectedCodes.denied || [], // Map denied to rejected_cdt_codes
      icd_codes: [], // Send empty list if frontend doesn't handle ICD yet
      rejected_icd_codes: [] // Send empty list if frontend doesn't handle ICD yet
    };

    // Log the payload being sent
    console.log("Sending payload to /api/store-code-status:", payload);

    const response = await apiInstance.post('/api/store-code-status', payload); // Send the transformed payload
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
    const response = await apiInstance.get(`/api/user/${userId}/activity`, {
      signal: signal // Pass the AbortController signal
    });
    console.log(`services.js: Received activity for user ${userId}:`, response.data);
    // Adjust the expected response structure based on your backend
    // Example: { user: { name, email, ... }, activity: [ { action, timestamp, ... }, ... ] }
    return response.data;
  } catch (error) {
    console.error(`Get User Activity (ID: ${userId}) error:`, error);
    if (error.name === 'CanceledError' || error.name === 'AbortError') {
      const abortError = new Error('Request was cancelled');
      abortError.name = 'AbortError';
      throw abortError;
    }
    // Rethrow specific backend error or a generic one
    throw error.response?.data || { message: `Failed to fetch activity for user ${userId}`, detail: 'Could not connect or permission denied' };
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