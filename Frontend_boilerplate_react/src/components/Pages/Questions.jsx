import { useState, useRef, useEffect } from 'react';
import { FaTooth, FaPlusCircle, FaMinusCircle, FaPaperPlane, FaRobot, FaCopy, FaSpinner, FaExclamationTriangle, FaStop } from 'react-icons/fa';
import { analyzeDentalScenario, analyzeBatchScenarios } from '../../interceptors/services.js';
import { useTheme } from '../../context/ThemeContext';
import Questioner from './Questioner';

const Questions = () => {
  const { isDark } = useTheme();
  const [questions, setQuestions] = useState([{ id: 1, text: '', result: null, loading: false, error: null }]);
  const [nextId, setNextId] = useState(2);
  const [batchLoading, setBatchLoading] = useState(false);
  const [globalError, setGlobalError] = useState(null);
  const abortControllerRef = useRef({});
  
  // Keep track of active processing requests
  const [activeRequests, setActiveRequests] = useState(0);

  // State for Questioner Modal
  const [isQuestionerVisible, setIsQuestionerVisible] = useState(false);
  const [currentQuestionerData, setCurrentQuestionerData] = useState(null);
  const [currentRecordId, setCurrentRecordId] = useState(null);
  const [questionPendingQueue, setQuestionPendingQueue] = useState([]);
  
  // Check if there are questions that need answering in any of the results
  useEffect(() => {
    // Only check if the questioner isn't already visible
    if (!isQuestionerVisible) {
      // Look through all questions for questioner_data
      const questionWithQuestioner = questions.find(q => 
        q.result?.data?.questioner_data?.has_questions &&
        !q.processedQuestioner // Track if we've already processed this questioner
      );
      
      if (questionWithQuestioner) {
        console.log(`Found questions needing answers for question ID ${questionWithQuestioner.id}`);
        setCurrentQuestionerData(questionWithQuestioner.result.data.questioner_data);
        setCurrentRecordId(questionWithQuestioner.result.data.record_id);
        setIsQuestionerVisible(true);
        
        // Mark this question as having its questioner processed
        setQuestions(prevQuestions => prevQuestions.map(q => 
          q.id === questionWithQuestioner.id 
            ? { ...q, processedQuestioner: true } 
            : q
        ));
      } else if (questionPendingQueue.length > 0) {
        // Process the next item in the queue
        const nextInQueue = questionPendingQueue[0];
        console.log(`Processing next questioner from queue for record ID: ${nextInQueue.recordId}`);
        
        setCurrentQuestionerData(nextInQueue.questionerData);
        setCurrentRecordId(nextInQueue.recordId);
        setIsQuestionerVisible(true);
        
        // Remove this item from the queue
        setQuestionPendingQueue(prevQueue => prevQueue.slice(1));
      }
    }
  }, [questions, isQuestionerVisible, questionPendingQueue]);
  
  // Clean up abort controllers when component unmounts
  useEffect(() => {
    return () => {
      // Cancel all pending requests on unmount
      Object.values(abortControllerRef.current).forEach(controller => {
        if (controller) {
          try {
            controller.abort();
          } catch (e) {
            console.error('Error aborting controller:', e);
          }
        }
      });
    };
  }, []);

  const handleQuestionChange = (id, value) => {
    setQuestions(questions.map(q => 
      q.id === id ? { ...q, text: value } : q
    ));
  };

  const addQuestion = () => {
    setQuestions([...questions, { id: nextId, text: '', result: null, loading: false, error: null }]);
    setNextId(nextId + 1);
  };

  const removeQuestion = (id) => {
    if (questions.length > 1) {
      // Cancel any pending request for this question
      if (abortControllerRef.current[id]) {
        try {
          abortControllerRef.current[id].abort();
          delete abortControllerRef.current[id];
        } catch (e) {
          console.error('Error aborting controller for question:', id, e);
        }
      }
      setQuestions(questions.filter(q => q.id !== id));
    }
  };

  // Cancel the current batch processing
  const cancelProcessing = () => {
    // Abort all controllers
    Object.values(abortControllerRef.current).forEach(controller => {
      if (controller) {
        try {
          controller.abort();
        } catch (e) {
          console.error('Error aborting controller:', e);
        }
      }
    });
    
    // Clear all controllers
    abortControllerRef.current = {};
    
    // Reset loading states
    setBatchLoading(false);
    setQuestions(questions.map(q => ({
      ...q,
      loading: false
    })));
    
    setActiveRequests(0);
    setGlobalError("Processing was cancelled");
  };

  // Individual question analysis - made to support true parallelism
  const analyzeQuestion = async (id) => {
    const question = questions.find(q => q.id === id);
    if (!question || !question.text.trim()) return;

    // Set loading state immediately to give visual feedback
    setQuestions(prevQuestions => 
      prevQuestions.map(q => 
        q.id === id ? { ...q, loading: true, error: null } : q
      )
    );
    
    setGlobalError(null);
    setActiveRequests(prev => prev + 1);

    try {
      // Create a new AbortController for this specific request
      const abortController = new AbortController();
      abortControllerRef.current[id] = abortController;
      
      console.log(`Starting analysis for question ${id}...`);
      
      const response = await analyzeDentalScenario({ 
        scenario: question.text 
      }, abortController.signal);
      
      // Remove the controller after completion
      delete abortControllerRef.current[id];
      
      console.log(`Completed analysis for question ${id}`);

      // Process successful response
      if (response?.status === 'success' && response?.data) {
        setQuestions(prevQuestions => prevQuestions.map(q => 
          q.id === id ? { ...q, result: response, loading: false } : q
        ));

        // Check for questions and add to queue or show immediately
        if (response.data.questioner_data?.has_questions) {
          console.log("Questions found for record:", response.data.record_id);
          
          if (isQuestionerVisible) {
            // If questioner is already visible, add to queue
            console.log(`Questioner already visible, adding record ${response.data.record_id} to queue`);
            setQuestionPendingQueue(prevQueue => [
              ...prevQueue, 
              { recordId: response.data.record_id, questionerData: response.data.questioner_data }
            ]);
          } else {
            // If questioner isn't visible, show immediately
            setCurrentQuestionerData(response.data.questioner_data);
            setCurrentRecordId(response.data.record_id);
            setIsQuestionerVisible(true);
            
            // Mark this question as having its questioner processed
            setQuestions(prevQuestions => prevQuestions.map(q => 
              q.id === id ? { ...q, processedQuestioner: true } : q
            ));
          }
        } else {
          console.log("No questions needed for record:", response.data.record_id);
        }
      } else {
        // Handle non-success status within the response
        throw new Error(response?.message || 'Analysis failed with non-success status');
      }
    } catch (err) {
      // Check if request was aborted
      if (err.name === 'AbortError') {
        console.log(`Request for question ${id} was cancelled`);
        return;
      }
      
      // Handle rate limit errors
      const errorMessage = err.message || 'Failed to analyze';
      const isRateLimit = errorMessage.includes('rate limit') || 
                         errorMessage.includes('quota') || 
                         errorMessage.includes('429');
      
      setQuestions(prevQuestions => prevQuestions.map(q => 
        q.id === id ? { 
          ...q, 
          error: isRateLimit 
            ? "API rate limit reached. Please try again in a few moments." 
            : errorMessage,
          loading: false 
        } : q
      ));
      
      console.error(`Error analyzing question ${id}:`, err);
    } finally {
      setActiveRequests(prev => prev - 1);
    }
  };

  // Enhanced batch analysis to improve parallelism
  const analyzeAllQuestions = async () => {
    // Filter questions that have text
    const questionsToProcess = questions.filter(q => q.text.trim() !== '');
    if (questionsToProcess.length === 0) return;

    // Option 1: Use the batch API endpoint (controlled parallelism)
    // Comment out this if statement and uncomment the code below for individual parallel requests
    if (questionsToProcess.length > 1) {
      // Use the batch API
      processBatch(questionsToProcess);
    } else {
      // For a single question, just use the regular analyze
      const questionId = questionsToProcess[0].id;
      analyzeQuestion(questionId);
    }
    
    // Option 2: Use individual requests for maximum parallelism
    // Uncomment this section and comment out the if-statement above to use this approach
    /*
    // Set loading states
    setQuestions(prevQuestions => 
      prevQuestions.map(q => 
        q.text.trim() !== '' ? { ...q, loading: true, error: null } : q
      )
    );
    
    // Fire off all requests in parallel
    questionsToProcess.forEach(question => {
      // Don't await here - let them all run in parallel
      analyzeQuestion(question.id);
    });
    */
  };
  
  // Process using the batch API endpoint
  const processBatch = async (questionsToProcess) => {
    // Set loading state for all questions being processed
    setBatchLoading(true);
    setQuestions(prevQuestions => 
      prevQuestions.map(q => 
        q.text.trim() !== '' ? { ...q, loading: true, error: null } : q
      )
    );
    
    setGlobalError(null);
    setActiveRequests(prev => prev + questionsToProcess.length);

    try {
      // Create a new AbortController for this batch request
      const batchId = 'batch-' + Date.now();
      const abortController = new AbortController();
      abortControllerRef.current[batchId] = abortController;
      
      // Extract just the text values for the batch API
      const scenariosArray = questionsToProcess.map(q => q.text);
      const response = await analyzeBatchScenarios(
        scenariosArray,
        abortController.signal
      );
      
      // Remove the controller after completion
      delete abortControllerRef.current[batchId];
      
      if (response.status === 'success' && response.batch_results) {
        // Update each question with its corresponding result
        const updatedQuestions = [...questions];
        
        questionsToProcess.forEach((question, index) => {
          const resultIndex = updatedQuestions.findIndex(q => q.id === question.id);
          if (resultIndex !== -1 && response.batch_results[index]) {
            const result = response.batch_results[index];
            
            // Check if this individual result has an error
            if (result.status === 'error') {
              updatedQuestions[resultIndex].error = result.message;
              updatedQuestions[resultIndex].result = null;
            } else if (result.status === 'success' && result.data) {
              updatedQuestions[resultIndex].result = result;
              updatedQuestions[resultIndex].error = null;

              // Check for questions from batch result
              if (result.data.questioner_data?.has_questions) {
                 // Add to queue for processing one by one
                 setQuestionPendingQueue(prevQueue => [
                   ...prevQueue,
                   { recordId: result.data.record_id, questionerData: result.data.questioner_data }
                 ]);
                 console.log(`Added record ${result.data.record_id} from batch to questioner queue`);
              } else {
                 console.log("No questions needed for batch record:", result.data.record_id);
              }
            } else {
              // Handle unexpected result structure
              updatedQuestions[resultIndex].error = 'Unexpected response structure from batch';
              updatedQuestions[resultIndex].result = null;
            }
            
            updatedQuestions[resultIndex].loading = false;
          }
        });
        
        setQuestions(updatedQuestions);
      } else {
        throw new Error('Failed to process batch analysis');
      }
    } catch (err) {
      // Check if request was aborted
      if (err.name === 'AbortError') {
        console.log('Batch request was cancelled');
        return;
      }
      
      // Handle rate limit errors
      const errorMessage = err.message || 'Failed to analyze in batch';
      const isRateLimit = errorMessage.includes('rate limit') || 
                         errorMessage.includes('quota') || 
                         errorMessage.includes('429');
      
      const displayError = isRateLimit 
        ? "API rate limit reached. Please try fewer questions at a time or wait a moment before trying again." 
        : errorMessage;
      
      setGlobalError(displayError);
      
      // Set error for all questions being processed
      setQuestions(prevQuestions => 
        prevQuestions.map(q => 
          q.text.trim() !== '' ? { ...q, error: displayError, loading: false } : q
        )
      );
    } finally {
      setBatchLoading(false);
      setActiveRequests(prev => prev - questionsToProcess.length);
    }
  };

  // Handle successful submission of answers from Questioner modal
  const handleQuestionerSubmitSuccess = (response) => {
    if (response?.status === 'success' && response?.data && currentRecordId) {
      // Find the question in the state that corresponds to the submitted answers
      setQuestions(prevQuestions => prevQuestions.map(q => {
        // Check if the result exists and matches the record ID
        if (q.result?.data?.record_id === currentRecordId) {
          // Create a deep copy to avoid mutation issues
          const updatedResult = JSON.parse(JSON.stringify(q.result));
          // Update the inspector_results within the result object
          if (updatedResult.data) {
             updatedResult.data.inspector_results = response.data.inspector_results;
             // Optionally update questioner_data as well if needed
             updatedResult.data.questioner_data = response.data.questioner_data;
          } 
          return { ...q, result: updatedResult };
        }
        return q;
      }));
      console.log("Updated results after questioner submission for record:", currentRecordId);
    } else {
      console.error("Failed to update results after questioner submission:", response);
      // Optionally show an error message to the user
    }
    
    // Reset questioner state regardless of success/failure of update
    setIsQuestionerVisible(false);
    setCurrentQuestionerData(null);
    setCurrentRecordId(null);
  };

  const handleCopyResults = (id) => {
    const question = questions.find(q => q.id === id);
    if (!question?.result?.data?.inspector_results) return;
    
    const cdtCodes = question.result.data.inspector_results.cdt?.codes || [];
    const icdCodes = question.result.data.inspector_results.icd?.codes || [];
    
    let textToCopy = `Question: ${question.text}\n\nCDT Codes: ${cdtCodes.join(', ')}\nICD Codes: ${icdCodes.join(', ')}`;
    
    navigator.clipboard.writeText(textToCopy).then(() => {
      alert('Results copied to clipboard!');
    }).catch(err => {
      console.error('Failed to copy results: ', err);
    });
  };

  const renderResults = (question) => {
    if (!question.result?.data?.inspector_results) return null;

    const cdtCodes = question.result.data.inspector_results.cdt?.codes || [];
    const icdCodes = question.result.data.inspector_results.icd?.codes || [];
    const cdtExplanation = question.result.data.inspector_results.cdt?.explanation || '';
    const icdExplanation = question.result.data.inspector_results.icd?.explanation || '';

    return (
      <div className={`mt-4 p-4 ${isDark ? 'bg-blue-900/30 border-blue-700' : 'bg-blue-50 border-blue-200'} rounded-lg border relative`}>
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center">
            <FaRobot className={`${isDark ? 'text-blue-400' : 'text-blue-500'} mr-2`} />
            <h3 className={`text-lg font-semibold ${isDark ? 'text-blue-400' : 'text-blue-700'}`}>Results</h3>
          </div>
          <button
            onClick={() => handleCopyResults(question.id)}
            className={`${isDark ? 'text-blue-400 hover:text-blue-300' : 'text-blue-500 hover:text-blue-700'} transition-colors`}
          >
            <FaCopy className="inline mr-1" /> Copy
          </button>
        </div>
        
        <div className="mb-4">
          <h4 className={`font-medium ${isDark ? 'text-gray-200' : 'text-gray-700'} mb-2`}>CDT Codes:</h4>
          <div className="flex flex-wrap gap-2">
            {cdtCodes.length > 0 ? cdtCodes.map((code, index) => (
              <span 
                key={`cdt-code-${index}-${code}`}
                className={`px-3 py-1 rounded-full text-sm ${
                  isDark ? 'bg-blue-800/60 text-blue-200' : 'bg-blue-100 text-blue-800'
                }`}
              >
                {code}
              </span>
            )) : (
              <span className="text-sm text-gray-500">No CDT codes found</span>
            )}
          </div>
          <p className={`text-sm ${isDark ? 'text-gray-300' : 'text-gray-600'} mt-2`}>{cdtExplanation}</p>
        </div>

        <div className="mb-2">
          <h4 className={`font-medium ${isDark ? 'text-gray-200' : 'text-gray-700'} mb-2`}>ICD Codes:</h4>
          <div className="flex flex-wrap gap-2">
            {icdCodes.length > 0 ? icdCodes.map((code, index) => (
              <span 
                key={`icd-code-${index}-${code}`}
                className={`px-3 py-1 rounded-full text-sm ${
                  isDark ? 'bg-purple-900/60 text-purple-200' : 'bg-purple-100 text-purple-800'
                }`}
              >
                {code}
              </span>
            )) : (
              <span className="text-sm text-gray-500">No ICD codes found</span>
            )}
          </div>
          <p className={`text-sm ${isDark ? 'text-gray-300' : 'text-gray-600'} mt-2`}>{icdExplanation}</p>
        </div>
        
        {question.result?.data?.questioner_data?.has_questions && (
          <div className={`mt-2 p-2 ${isDark ? 'bg-yellow-800/30' : 'bg-yellow-100'} rounded-lg border border-yellow-400`}>
            <p className={`text-sm ${isDark ? 'text-yellow-200' : 'text-yellow-800'}`}>
              This scenario required additional questions that were processed{question.processedQuestioner ? '' : ' or are pending'}.
            </p>
          </div>
        )}
      </div>
    );
  };

  // Count questions with text
  const getValidQuestionsCount = () => {
    return questions.filter(q => q.text.trim() !== '').length;
  };

  // Count pending questioners (in queue plus visible ones)
  const getPendingQuestionersCount = () => {
    return questionPendingQueue.length + (isQuestionerVisible ? 1 : 0);
  };

  return (
    <div className="flex-grow flex justify-center p-4">
      <div className={`w-full max-w-4xl ${isDark ? 'bg-gray-800' : 'bg-white'} rounded-lg shadow-lg p-6 transition-colors`}>
        <div className={`${isDark ? 'bg-blue-900' : 'bg-blue-500'} text-white p-4 rounded-lg mb-6 flex justify-between items-center`}>
          <h2 className="text-xl md:text-2xl font-semibold flex items-center">
            <FaTooth className="mr-2" /> Multiple Dental Scenarios
            {activeRequests > 0 && (
              <span className="ml-2 text-sm bg-green-500 px-2 py-1 rounded-full">
                {activeRequests} Active {activeRequests === 1 ? 'Request' : 'Requests'}
              </span>
            )}
            {getPendingQuestionersCount() > 0 && (
              <span className="ml-2 text-sm bg-yellow-500 px-2 py-1 rounded-full">
                {getPendingQuestionersCount()} Pending {getPendingQuestionersCount() === 1 ? 'Questioner' : 'Questioners'}
              </span>
            )}
          </h2>
          <div className="flex space-x-2">
            {batchLoading ? (
              <button 
                onClick={cancelProcessing}
                className={`${isDark ? 'bg-red-700 hover:bg-red-600' : 'bg-red-600 hover:bg-red-500'} 
                text-white px-3 py-2 rounded-lg transition-colors flex items-center`}
              >
                <FaStop className="inline mr-1" />
                Cancel
              </button>
            ) : (
              <button 
                onClick={analyzeAllQuestions}
                className={`${
                  batchLoading || getValidQuestionsCount() === 0
                    ? (isDark ? 'bg-gray-700' : 'bg-gray-400') 
                    : (isDark ? 'bg-green-700 hover:bg-green-600' : 'bg-green-600 hover:bg-green-500')
                } text-white px-3 py-2 rounded-lg transition-colors flex items-center`}
                disabled={batchLoading || getValidQuestionsCount() === 0}
              >
                {batchLoading ? (
                  <>
                    <FaSpinner className="inline mr-1 animate-spin" />
                    Processing...
                  </>
                ) : (
                  <>
                    <FaPaperPlane className="inline mr-1" />
                    Analyze All
                  </>
                )}
              </button>
            )}
            <button 
              onClick={addQuestion}
              className={`${isDark ? 'bg-blue-700 hover:bg-blue-600' : 'bg-blue-600 hover:bg-blue-500'} 
                text-white p-2 rounded-full transition-colors flex items-center`}
              disabled={batchLoading}
            >
              <FaPlusCircle className="mr-1" /> Add Question
            </button>
          </div>
        </div>

        {globalError && (
          <div className={`mb-4 p-4 rounded-lg ${isDark ? 'bg-red-900/30' : 'bg-red-100'} flex items-start`}>
            <FaExclamationTriangle className={`mt-1 ${isDark ? 'text-red-400' : 'text-red-600'} mr-2`} />
            <div>
              <h3 className={`font-bold ${isDark ? 'text-red-300' : 'text-red-700'} mb-1`}>Error</h3>
              <p className={`${isDark ? 'text-red-200' : 'text-red-600'}`}>{globalError}</p>
              <p className="text-sm mt-1 opacity-80">For better performance, try processing fewer questions at once.</p>
            </div>
          </div>
        )}

        <div className="space-y-6">
          {questions.map((question) => (
            <div 
              key={question.id} 
              className={`p-4 rounded-lg border ${
                isDark ? 'bg-gray-700 border-gray-600' : 'bg-gray-50 border-gray-200'
              }`}
            >
              <div className="flex justify-between items-center mb-3">
                <h3 className={`font-semibold ${isDark ? 'text-gray-200' : 'text-gray-700'}`}>
                  Question {question.id}
                  {question.result?.data?.questioner_data?.has_questions && (
                    <span className={`ml-2 text-xs px-2 py-1 rounded-full ${
                      isDark ? 'bg-yellow-800/60 text-yellow-200' : 'bg-yellow-100 text-yellow-800'
                    }`}>
                      Has Questions
                    </span>
                  )}
                </h3>
                {questions.length > 1 && (
                  <button 
                    onClick={() => removeQuestion(question.id)}
                    className={`${isDark ? 'text-red-400 hover:text-red-300' : 'text-red-500 hover:text-red-600'} 
                      transition-colors`}
                    disabled={batchLoading}
                  >
                    <FaMinusCircle />
                  </button>
                )}
              </div>
              
              <div className="mb-3">
                <textarea
                  placeholder="Describe the dental procedure or diagnosis..."
                  className={`w-full p-3 border ${
                    isDark ? 'bg-gray-800 border-gray-600 text-gray-100' : 'bg-white border-gray-300 text-gray-900'
                  } rounded-lg focus:outline-none ${
                    isDark ? 'focus:border-blue-400' : 'focus:border-blue-500'
                  } text-sm md:text-base transition-colors`}
                  rows="4"
                  value={question.text}
                  onChange={(e) => handleQuestionChange(question.id, e.target.value)}
                  disabled={batchLoading || question.loading}
                ></textarea>
              </div>
              
              <div className="flex justify-end">
                <button
                  onClick={() => analyzeQuestion(question.id)}
                  disabled={question.loading || !question.text.trim() || batchLoading}
                  className={`${
                    question.loading || !question.text.trim() || batchLoading
                      ? (isDark ? 'bg-gray-600' : 'bg-gray-400') 
                      : (isDark ? 'bg-blue-700 hover:bg-blue-600' : 'bg-blue-600 hover:bg-blue-700')
                  } text-white px-4 py-2 rounded-lg shadow-md transition-all duration-300 flex items-center`}
                >
                  {question.loading ? (
                    <>
                      <FaSpinner className="inline mr-2 animate-spin" />
                      Analyzing...
                    </>
                  ) : (
                    <>
                      <FaPaperPlane className="inline mr-2" />
                      Analyze
                    </>
                  )}
                </button>
              </div>
              
              {question.error && (
                <div className={`mt-4 p-3 rounded-lg ${isDark ? 'bg-red-900/30 text-red-200' : 'bg-red-100 text-red-700'}`}>
                  {question.error}
                </div>
              )}
              
              {renderResults(question)}
            </div>
          ))}
        </div>

        {/* Questioner Modal */} 
        {isQuestionerVisible && currentQuestionerData && currentRecordId && (
          <Questioner 
            isVisible={isQuestionerVisible}
            onClose={() => {
              console.log("Questioner closed by user");
              setIsQuestionerVisible(false); 
              setCurrentQuestionerData(null); 
              setCurrentRecordId(null);
            }}
            questions={{
              cdt_questions: (currentQuestionerData.cdt_questions?.questions || []).map(q => ({
                ...q,
                id: q.id || `cdt-${Math.random().toString(36).substr(2, 9)}` // Ensure every question has an id
              })),
              icd_questions: (currentQuestionerData.icd_questions?.questions || []).map(q => ({
                ...q,
                id: q.id || `icd-${Math.random().toString(36).substr(2, 9)}` // Ensure every question has an id
              }))
            }}
            recordId={currentRecordId}
            onSubmitSuccess={handleQuestionerSubmitSuccess}
          />
        )}

      </div>
    </div>
  );
};

export default Questions; 