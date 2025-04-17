import { useState, useRef, useEffect } from 'react';
import { FaTooth, FaPlusCircle, FaMinusCircle, FaPaperPlane, FaRobot, FaCopy, FaSpinner, FaExclamationTriangle, FaStop, FaCheck, FaTimes, FaCogs } from 'react-icons/fa';
import { analyzeDentalScenario, analyzeBatchScenarios, addCustomCode } from '../../interceptors/services.js';
import { useTheme } from '../../context/ThemeContext';
import Questioner from './Questioner';

const Questions = () => {
  const { isDark } = useTheme();
  const [questions, setQuestions] = useState([{ id: 1, text: '', result: null, loading: false, error: null, processedQuestioner: false }]);
  const [nextId, setNextId] = useState(2);
  const [batchLoading, setBatchLoading] = useState(false);
  const [globalError, setGlobalError] = useState(null);
  const abortControllerRef = useRef({});
  
  // Keep track of active processing requests
  const [activeRequests, setActiveRequests] = useState(0);

  // State for Questioner Modal
  const [isQuestionerVisible, setIsQuestionerVisible] = useState(false);
  const [currentQuestionerData, setCurrentQuestionerData] = useState(null);
  const [questionPendingQueue, setQuestionPendingQueue] = useState([]);

  // State for code selection per question
  const [selectedCodes, setSelectedCodes] = useState({});
  const [newCodeInputs, setNewCodeInputs] = useState({});
  const [customCodeLoading, setCustomCodeLoading] = useState({});

  // Check if there are questions that need answering in any of the results
  useEffect(() => {
    // Only check if the questioner isn't already visible
    if (!isQuestionerVisible) {
      // Process all questions at once instead of one by one
      const needsQuestioning = questions.filter(q => 
        q.result?.data?.questioner_data?.has_questions &&
        !q.processedQuestioner // Track if we've already processed this questioner
      );
      
      if (needsQuestioning.length > 0) {
        console.log(`Found ${needsQuestioning.length} scenarios needing answers`);
        
        // Combine all questions into a single questioner data object
        const combinedQuestionerData = {
          cdt_questions: {
            questions: [],
            explanation: "",
            has_questions: false
          },
          icd_questions: {
            questions: [],
            explanation: "",
            has_questions: false
          },
          has_questions: false,
          scenarios: []
        };
        
        // Collect record IDs that need questioning
        const recordIds = [];
        
        needsQuestioning.forEach(q => {
          const questionerData = q.result.data.questioner_data;
          const recordId = q.result.data.record_id;
          const questionId = q.id;
          
          // Add scenario info to track which questions belong to which scenario
          combinedQuestionerData.scenarios.push({
            recordId,
            questionId,
            text: q.text
          });
          
          // Add CDT questions with scenario identifier
          if (questionerData.cdt_questions?.questions?.length > 0) {
            combinedQuestionerData.cdt_questions.has_questions = true;
            combinedQuestionerData.has_questions = true;
            
            // Ensure correct object structure for Questioner component
            questionerData.cdt_questions.questions.forEach((questionItem, index) => {
              const baseId = `cdt-${recordId}-${index}`;
              let questionObj;
              if (typeof questionItem === 'string') {
                // If backend sends a string, create object with 'question' prop
                questionObj = {
                  question: questionItem, // Use 'question' property name
                  id: baseId,
                  scenarioId: questionId, // Frontend question ID acts as scenario ID here
                  recordId: recordId     // Backend record ID
                };
              } else {
                // If backend sends an object, ensure 'question' prop exists and IDs are correct
                questionObj = {
                  ...questionItem,
                  question: questionItem.question || questionItem.text || "Missing question text", // Use 'question', fallback to 'text'
                  id: questionItem.id || baseId, // Use provided ID or generate one
                  scenarioId: questionId, // Ensure frontend scenario ID is set
                  recordId: recordId     // Ensure backend record ID is set
                };
              }
              combinedQuestionerData.cdt_questions.questions.push(questionObj);
            });
          }
          
          // Add ICD questions with scenario identifier
          if (questionerData.icd_questions?.questions?.length > 0) {
            combinedQuestionerData.icd_questions.has_questions = true;
            combinedQuestionerData.has_questions = true;
            
            // Ensure correct object structure for Questioner component
            questionerData.icd_questions.questions.forEach((questionItem, index) => {
              const baseId = `icd-${recordId}-${index}`;
               let questionObj;
              if (typeof questionItem === 'string') {
                 // If backend sends a string, create object with 'question' prop
                questionObj = {
                  question: questionItem, // Use 'question' property name
                  id: baseId,
                  scenarioId: questionId, // Frontend question ID acts as scenario ID here
                  recordId: recordId     // Backend record ID
                };
              } else {
                 // If backend sends an object, ensure 'question' prop exists and IDs are correct
                questionObj = {
                  ...questionItem,
                  question: questionItem.question || questionItem.text || "Missing question text", // Use 'question', fallback to 'text'
                  id: questionItem.id || baseId, // Use provided ID or generate one
                  scenarioId: questionId, // Ensure frontend scenario ID is set
                  recordId: recordId     // Ensure backend record ID is set
                };
              }
              combinedQuestionerData.icd_questions.questions.push(questionObj);
            });
          }
          
          recordIds.push(recordId);
        });
        
        // Mark all questions as processed to prevent showing them again
        setQuestions(prevQuestions => prevQuestions.map(q => 
          needsQuestioning.some(nq => nq.id === q.id)
            ? { ...q, processedQuestioner: true } 
            : q
        ));
        
        // Set combined data for the questioner
        setCurrentQuestionerData(combinedQuestionerData);
        setIsQuestionerVisible(true);
        
        // Clear the pending queue since we're handling all questions at once
        setQuestionPendingQueue([]);
      } else if (questionPendingQueue.length > 0) {
        // Process the next item in the queue (keeping this for backward compatibility)
        const nextInQueue = questionPendingQueue[0];
        console.log(`Processing next questioner from queue for record ID: ${nextInQueue.recordId}`);
        
        setCurrentQuestionerData(nextInQueue.questionerData);
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
    const newQuestionId = nextId;
    setQuestions([...questions, { id: newQuestionId, text: '', result: null, loading: false, error: null, processedQuestioner: false }]);
    setNextId(newQuestionId + 1);
    // Initialize state for the new question
    setSelectedCodes(prev => ({ ...prev, [newQuestionId]: { accepted: [], denied: [] } }));
    setNewCodeInputs(prev => ({ ...prev, [newQuestionId]: '' }));
    setCustomCodeLoading(prev => ({ ...prev, [newQuestionId]: false }));
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
      // Clean up state for the removed question
      setSelectedCodes(prev => { const newState = { ...prev }; delete newState[id]; return newState; });
      setNewCodeInputs(prev => { const newState = { ...prev }; delete newState[id]; return newState; });
      setCustomCodeLoading(prev => { const newState = { ...prev }; delete newState[id]; return newState; });
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

    // Reset state for this question before analysis
    setSelectedCodes(prev => ({ ...prev, [id]: { accepted: [], denied: [] } }));
    setNewCodeInputs(prev => ({ ...prev, [id]: '' }));
    setCustomCodeLoading(prev => ({ ...prev, [id]: false }));

    // Set loading state immediately to give visual feedback
    setQuestions(prevQuestions =>
      prevQuestions.map(q =>
        q.id === id ? { ...q, loading: true, error: null, result: null, processedQuestioner: false } : q // Reset result and processed flag
      )
    );
    
    setGlobalError(null);
    setActiveRequests(prev => prev + 1);

    let wasAborted = false; // Flag to check if aborted
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

        // Initialize selected codes based on inspector results (if any)
        const inspectorCodes = response.data.inspector_results?.cdt?.codes || [];
        setSelectedCodes(prev => ({
          ...prev,
          [id]: { accepted: inspectorCodes, denied: [] } // Pre-accept codes from inspector
        }));


        // Check for questions and add to queue or show immediately (using combined logic)
        if (response.data.questioner_data?.has_questions) {
          console.log("Questions found for record:", response.data.record_id);
          // Mark this question as processed to prevent immediate trigger (useEffect handles it)
           setQuestions(prevQuestions => prevQuestions.map(q =>
             q.id === id ? { ...q, processedQuestioner: false } : q // Let useEffect handle combining
           ));
        } else {
          console.log("No questions needed for record:", response.data.record_id);
        }
      } else {
        // Handle non-success status within the response
        throw new Error(response?.message || 'Analysis failed with non-success status');
      }
    } catch (err) {
      if (err.name === 'AbortError') {
        wasAborted = true;
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
      // Ensure controller is cleaned up even if error occurred before delete in try block
      if (abortControllerRef.current[id]) {
         console.warn(`Controller cleanup needed in finally for ${id}`);
         delete abortControllerRef.current[id];
      }
      // Decrement count if the operation wasn't aborted
      if (!wasAborted) {
          setActiveRequests(prev => Math.max(0, prev - 1));
      }
    }
  };

  // Enhanced batch analysis to improve parallelism
  const analyzeAllQuestions = async () => {
    // Filter questions that have text
    const questionsToProcess = questions.filter(q => q.text.trim() !== '');
    if (questionsToProcess.length === 0) return;

    // Reset state for all questions being processed
    questionsToProcess.forEach(q => {
       setSelectedCodes(prev => ({ ...prev, [q.id]: { accepted: [], denied: [] } }));
       setNewCodeInputs(prev => ({ ...prev, [q.id]: '' }));
       setCustomCodeLoading(prev => ({ ...prev, [q.id]: false }));
    });

    // Use the batch API endpoint (controlled parallelism)
    processBatch(questionsToProcess);
  };
  
  // Process using the batch API endpoint
  const processBatch = async (questionsToProcess) => {
    // Set loading state for all questions being processed
    setBatchLoading(true);
    setQuestions(prevQuestions =>
      prevQuestions.map(q =>
        questionsToProcess.some(qp => qp.id === q.id)
          ? { ...q, loading: true, error: null, result: null, processedQuestioner: false } // Reset result and processed flag
          : q
      )
    );
    
    setGlobalError(null);
    setActiveRequests(prev => prev + questionsToProcess.length); // Increment for each question in batch

    const batchId = 'batch-' + Date.now();
    let wasAbortedBatch = false; // Flag for batch abortion

    try {
      // Create a new AbortController for this batch request
      const abortController = new AbortController();
      abortControllerRef.current[batchId] = abortController;
      
      // Extract just the text values for the batch API
      const scenariosArray = questionsToProcess.map(q => q.text);
      const response = await analyzeBatchScenarios(
        scenariosArray,
        abortController.signal
      );
      
      // Remove the controller after successful API call completion
      delete abortControllerRef.current[batchId];
      
      if (response.status === 'success' && response.batch_results) {
        // Update each question with its corresponding result
        const updatedQuestions = [...questions];

        questionsToProcess.forEach((processedQuestion, index) => {
          const resultIndex = updatedQuestions.findIndex(q => q.id === processedQuestion.id);
          if (resultIndex !== -1 && response.batch_results[index]) {
            const resultData = response.batch_results[index];
            const questionId = processedQuestion.id;

            updatedQuestions[resultIndex].loading = false; // Set loading false for this question

            // Check if this individual result has an error
            if (resultData.status === 'error') {
              updatedQuestions[resultIndex].error = resultData.message || 'Failed in batch';
              updatedQuestions[resultIndex].result = null;
            } else if (resultData.status === 'success' && resultData.data) {
              updatedQuestions[resultIndex].result = resultData; // Store the whole item {status: 'success', data: {...}}
              updatedQuestions[resultIndex].error = null;

              // Initialize selected codes based on inspector results
              const inspectorCodes = resultData.data.inspector_results?.cdt?.codes || [];
              setSelectedCodes(prev => ({
                ...prev,
                [questionId]: { accepted: inspectorCodes, denied: [] } // Pre-accept codes
              }));

              // Check for questions from batch result
              if (resultData.data.questioner_data?.has_questions) {
                 updatedQuestions[resultIndex].processedQuestioner = false; // Mark for useEffect check
                 console.log(`Questions potentially needed for batch record: ${resultData.data.record_id}`);
              } else {
                 console.log("No questions needed for batch record:", resultData.data.record_id);
                 updatedQuestions[resultIndex].processedQuestioner = true; // Mark as processed if no questions
              }
            } else {
              // Handle unexpected result structure
              updatedQuestions[resultIndex].error = 'Unexpected response structure from batch';
              updatedQuestions[resultIndex].result = null;
            }
          }
        });
        
        setQuestions(updatedQuestions);

      } else {
        throw new Error(response.message || 'Failed to process batch analysis or invalid response format');
      }
    } catch (err) {
      if (err.name === 'AbortError') {
        wasAbortedBatch = true;
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
      
      // Set error and stop loading for all questions being processed
      setQuestions(prevQuestions =>
        prevQuestions.map(q =>
          questionsToProcess.some(qp => qp.id === q.id)
            ? { ...q, error: displayError, loading: false }
            : q
        )
      );
    } finally {
      setBatchLoading(false);
       // Ensure controller is cleaned up
       if (abortControllerRef.current[batchId]) {
           console.warn(`Controller cleanup needed in finally for ${batchId}`);
           delete abortControllerRef.current[batchId];
       }
      // Decrement count if the operation wasn't aborted
      if (!wasAbortedBatch) {
          setActiveRequests(prev => Math.max(0, prev - questionsToProcess.length));
      }
    }
  };

  // Handle code selection (accept/deny) for a specific question
  const handleCodeSelection = (questionId, code, action) => {
    setSelectedCodes(prev => {
      // Ensure the entry for this questionId exists
      const currentSelection = prev[questionId] || { accepted: [], denied: [] };
      const newState = { ...prev };
      
      // Create new arrays for accepted/denied for this specific question
      let newAccepted = [...currentSelection.accepted];
      let newDenied = [...currentSelection.denied];
      
      // Remove code from both lists if it exists
      newAccepted = newAccepted.filter(c => c !== code);
      newDenied = newDenied.filter(c => c !== code);
      
      // Add to appropriate list
      if (action === 'accept') {
        newAccepted.push(code);
      } else if (action === 'deny') {
        newDenied.push(code);
      }
      
      // Update the state for this specific questionId
      newState[questionId] = { accepted: newAccepted, denied: newDenied };
      
      return newState;
    });
  };

  // Handle input change for custom code
  const handleNewCodeChange = (questionId, value) => {
    setNewCodeInputs(prev => ({
      ...prev,
      [questionId]: value
    }));
  };

  // Handle adding a custom code for a specific question
  const handleAddCode = async (questionId) => {
    const question = questions.find(q => q.id === questionId);
    const newCode = newCodeInputs[questionId];
    
    if (!question || !newCode?.trim()) {
      setGlobalError("Please enter a valid code for the selected question.");
      return;
    }
    
    const recordId = question.result?.data?.record_id;
    const scenarioText = question.text;

    if (!recordId) {
      setGlobalError("No active analysis session for this question. Please analyze first.");
      return;
    }

    setCustomCodeLoading(prev => ({ ...prev, [questionId]: true }));
    setGlobalError(null); // Clear global error

    try {
      const response = await addCustomCode(newCode, scenarioText, recordId);
      console.log(`Custom code response for question ${questionId}:`, response);
      
      if (response.status === 'success' && response.inspector_results) {
        // Update the result state for this specific question
        setQuestions(prevQuestions => prevQuestions.map(q => {
          if (q.id === questionId) {
            // Create a deep copy to avoid mutation issues
            const updatedResult = JSON.parse(JSON.stringify(q.result));
            // Update the inspector_results within the result object
            if (updatedResult.data) {
               updatedResult.data.inspector_results = response.inspector_results;
            }
            return { ...q, result: updatedResult };
          }
          return q;
        }));
        
        // Auto-select based on applicability
        if (response.is_applicable) {
          handleCodeSelection(questionId, newCode, 'accept');
        } else {
           handleCodeSelection(questionId, newCode, 'deny'); // Deny if not applicable
        }

        // Clear the input
        setNewCodeInputs(prev => ({ ...prev, [questionId]: '' }));

      } else {
        throw new Error(response.message || "Received invalid response format from add custom code");
      }
    } catch (err) {
      console.error(`Error adding custom code for question ${questionId}:`, err);
      // Set error specific to the question or globally
      setQuestions(prev => prev.map(q => q.id === questionId ? { ...q, error: err.message || 'Failed to add custom code' } : q));
      // setGlobalError(err.message || 'Failed to add custom code');
    } finally {
      setCustomCodeLoading(prev => ({ ...prev, [questionId]: false }));
    }
  };


  // Handle successful submission of answers from Questioner modal
  const handleQuestionerSubmitSuccess = (structuredResponses) => {
    console.log("Received structured responses from Questioner:", structuredResponses);
    if (!Array.isArray(structuredResponses)) {
      console.error("Invalid payload from Questioner: expected an array.");
      structuredResponses = []; // Prevent errors
    }
    
    // Create a Set of updated question IDs to avoid duplicate state updates if mapping is complex
    const updatedQuestionIds = new Set();
    let overallError = null;

    // Use a functional update for setQuestions to ensure we work with the latest state
    setQuestions(prevQuestions => {
        // Create a mutable copy of the previous questions
        let newQuestions = [...prevQuestions];

        structuredResponses.forEach(structuredResponse => {
            const { response, recordId, scenarioIds } = structuredResponse;

            if (response?.status === 'success' && response?.data && Array.isArray(scenarioIds)) {
                // Find all frontend questions that match the scenarioIds for this recordId
                scenarioIds.forEach(scenarioId => {
                    const questionIndex = newQuestions.findIndex(q => q.id === scenarioId);

                    if (questionIndex !== -1) {
                         console.log(`Updating question ID ${scenarioId} with data from record ${recordId}`);
                         const existingQuestion = newQuestions[questionIndex];
                         
                         // Create a deep copy of the result to update safely
                         // Ensure existing result and data structure exist before copying
                         let updatedResultData = {};
                         if (existingQuestion.result?.data) {
                              try {
                                   updatedResultData = JSON.parse(JSON.stringify(existingQuestion.result.data));
                              } catch(parseError) {
                                   console.error("Failed to parse existing result data for question:", scenarioId, parseError);
                                   updatedResultData = {}; // Start fresh if parsing fails
                              }
                         } else {
                              console.warn("Existing result.data not found for question:", scenarioId, "Creating structure.");
                              // Create base structure if it doesn't exist
                              updatedResultData = { record_id: recordId }; 
                         }
                         
                         // Update inspector_results and questioner_data
                         updatedResultData.inspector_results = response.data.inspector_results;
                         updatedResultData.questioner_data = response.data.questioner_data;
                         
                         // Update the specific question in the newQuestions array
                         newQuestions[questionIndex] = {
                           ...existingQuestion,
                           result: {
                               ...existingQuestion.result, // Keep other potential top-level result props
                               data: updatedResultData // Set the updated data
                           },
                           processedQuestioner: true // Mark as processed
                         };
                         
                         // Initialize selected codes based on new inspector results
                         const inspectorCodes = response.data.inspector_results?.cdt?.codes || [];
                         setSelectedCodes(prevSelected => ({
                           ...prevSelected,
                           [scenarioId]: { accepted: inspectorCodes, denied: [] }
                         }));

                        updatedQuestionIds.add(scenarioId); // Track which IDs were updated

                    } else {
                         console.warn(`Could not find frontend question with scenarioId: ${scenarioId} to update.`);
                    }
                });
            } else {
                // Handle failed submission for this recordId
                const errorMsg = `Failed to process answers for record ${recordId || 'unknown'}: ${response?.message || 'Unknown error'}`;
                console.error("Error in structured response:", errorMsg, structuredResponse);
                overallError = overallError ? `${overallError}\n${errorMsg}` : errorMsg;
                // Optionally mark associated questions with an error state?
                 if (Array.isArray(scenarioIds)) {
                      newQuestions = newQuestions.map(q => 
                           scenarioIds.includes(q.id) 
                              ? { ...q, error: response?.message || 'Answer submission failed', processedQuestioner: true } 
                              : q
                      );
                 }
            }
        });

       // Return the modified array for the state update
       return newQuestions;
    });

    // Show global error if any submissions failed
    if (overallError) {
         setGlobalError(overallError);
    }
    
    // Reset questioner state
    setIsQuestionerVisible(false);
    setCurrentQuestionerData(null);
  };

  // Modified to copy only accepted codes for the specific question
  const handleCopyResults = (id) => {
    const accepted = selectedCodes[id]?.accepted || [];
    if (accepted.length === 0) {
       alert('No accepted codes to copy.');
       return;
    }

    const question = questions.find(q => q.id === id);
    
    let textToCopy = `Question: ${question?.text || 'N/A'}

Accepted CDT Codes: ${accepted.join(', ')}`;
    // Optionally add accepted ICD codes if managed similarly
    
    navigator.clipboard.writeText(textToCopy).then(() => {
      alert('Accepted codes copied to clipboard!');
    }).catch(err => {
      console.error('Failed to copy results: ', err);
    });
  };

  // Render results section for a single question, including selection controls
  const renderResults = (question) => {
    const questionId = question.id; // ID for state access
    if (!question.result?.data?.inspector_results) return null;

    const inspectorData = question.result.data.inspector_results;
    const cdtCodes = inspectorData.cdt?.codes || [];
    const icdCodes = inspectorData.icd?.codes || []; // Keep displaying ICD for context
    const cdtExplanation = inspectorData.cdt?.explanation || '';
    const icdExplanation = inspectorData.icd?.explanation || ''; // Keep displaying ICD explanation

    const currentSelected = selectedCodes[questionId] || { accepted: [], denied: [] };

    return (
      <div className={`mt-4 p-4 ${isDark ? 'bg-blue-900/30 border-blue-700' : 'bg-blue-50 border-blue-200'} rounded-lg border relative`}>
        {/* Header and Copy Button */}
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center">
            <FaRobot className={`${isDark ? 'text-blue-400' : 'text-blue-500'} mr-2`} />
            <h3 className={`text-lg font-semibold ${isDark ? 'text-blue-400' : 'text-blue-700'}`}>Results</h3>
          </div>
          <button
            onClick={() => handleCopyResults(questionId)} // Pass question ID
            className={`${isDark ? 'text-blue-400 hover:text-blue-300' : 'text-blue-500 hover:text-blue-700'} transition-colors flex items-center text-sm`}
            disabled={currentSelected.accepted.length === 0} // Disable if no accepted codes
          >
            <FaCopy className="inline mr-1" /> Copy Accepted
          </button>
        </div>
        
        {/* CDT Codes Section */}
        <div className="mb-4">
          <h4 className={`font-medium ${isDark ? 'text-gray-200' : 'text-gray-700'} mb-2`}>CDT Codes:</h4>
          <div className="flex flex-wrap gap-2">
            {cdtCodes.length > 0 ? cdtCodes.map((code, index) => {
              const isAccepted = currentSelected.accepted.includes(code);
              const isDenied = currentSelected.denied.includes(code);
              
              return (
                <div
                  key={`cdt-code-${questionId}-${index}-${code}`}
                  className={`relative group px-3 py-1 rounded-full text-sm transition-all duration-200 cursor-pointer border ${
                    isAccepted
                      ? (isDark ? 'bg-green-900/60 text-green-200 border-green-700' : 'bg-green-100 text-green-800 border-green-300')
                      : isDenied
                        ? (isDark ? 'bg-red-900/60 text-red-200 border-red-700' : 'bg-red-100 text-red-800 border-red-300')
                        : (isDark ? 'bg-blue-800/60 text-blue-200 border-blue-700' : 'bg-blue-100 text-blue-800 border-blue-300')
                  }`}
                >
                  {code}
                  {/* Hover Icons */}
                  <div className="absolute inset-0 flex items-center justify-center space-x-1 bg-black bg-opacity-50 rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-200">
                    <button
                      title="Accept"
                      onClick={(e) => { e.stopPropagation(); handleCodeSelection(questionId, code, 'accept'); }}
                      className={`p-1 rounded-full ${isAccepted ? 'bg-green-500' : 'bg-gray-600 hover:bg-green-500'} text-white text-xs`}
                    >
                      <FaCheck />
                    </button>
                    <button
                      title="Reject"
                      onClick={(e) => { e.stopPropagation(); handleCodeSelection(questionId, code, 'deny'); }}
                       className={`p-1 rounded-full ${isDenied ? 'bg-red-500' : 'bg-gray-600 hover:bg-red-500'} text-white text-xs`}
                    >
                      <FaTimes />
                    </button>
                  </div>
                </div>
              );
            }) : (
              <span className="text-sm text-gray-500">No CDT codes found</span>
            )}
          </div>
          {cdtExplanation && <p className={`text-sm ${isDark ? 'text-gray-300' : 'text-gray-600'} mt-2 whitespace-pre-wrap`}>{cdtExplanation}</p>}
        </div>

        {/* ICD Codes Section (Display only, no selection) */}
        <div className="mb-2">
          <h4 className={`font-medium ${isDark ? 'text-gray-200' : 'text-gray-700'} mb-2`}>ICD Codes:</h4>
          <div className="flex flex-wrap gap-2">
            {icdCodes.length > 0 ? icdCodes.map((code, index) => (
              <span
                key={`icd-code-${questionId}-${index}-${code}`}
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
           {icdExplanation && <p className={`text-sm ${isDark ? 'text-gray-300' : 'text-gray-600'} mt-2 whitespace-pre-wrap`}>{icdExplanation}</p>}
        </div>
        
        {/* Questioner Pending Indicator */}
        {question.result?.data?.questioner_data?.has_questions && !question.processedQuestioner && (
          <div className={`mt-2 p-2 ${isDark ? 'bg-yellow-800/30' : 'bg-yellow-100'} rounded-lg border border-yellow-400`}>
            <p className={`text-sm ${isDark ? 'text-yellow-200' : 'text-yellow-800'}`}>
              This scenario requires additional questions (pending display).
            </p>
          </div>
        )}

        {/* Add Custom Code Section */}
         <div className={`mt-6 pt-4 border-t ${isDark ? 'border-gray-600' : 'border-gray-300'}`}>
           <h4 className="text-md font-semibold mb-3">Add Custom CDT Code</h4>
           <div className="flex items-center mb-2">
             <input
               type="text"
               placeholder="Enter CDT code (e.g., D1120)"
               className={`flex-grow p-2 border ${
                 isDark ? 'bg-gray-800 border-gray-600 text-gray-100' : 'bg-white border-gray-300 text-gray-900'
               } rounded-lg focus:outline-none ${
                 isDark ? 'focus:border-blue-400' : 'focus:border-blue-500'
               } text-sm`}
               value={newCodeInputs[questionId] || ''}
               onChange={(e) => handleNewCodeChange(questionId, e.target.value)}
               disabled={customCodeLoading[questionId] || question.loading}
             />
             <button
               onClick={() => handleAddCode(questionId)}
               className={`ml-2 px-4 py-2 ${
                 isDark ? 'bg-blue-700 hover:bg-blue-600' : 'bg-blue-600 hover:bg-blue-700'
               } text-white rounded-lg shadow-md transition-all duration-300 disabled:${
                 isDark ? 'bg-gray-700' : 'bg-gray-400'
               } flex items-center text-sm`}
               disabled={customCodeLoading[questionId] || question.loading || !newCodeInputs[questionId]?.trim() || !question.result?.data?.record_id}
             >
               {customCodeLoading[questionId] ? (
                 <>
                   <FaSpinner className="inline mr-1 animate-spin" />
                   Analyzing...
                 </>
               ) : (
                 <>
                    <FaCogs className="inline mr-1" />
                    Analyze Code
                  </>
               )}
             </button>
           </div>
           <p className={`text-xs ${isDark ? 'text-gray-400' : 'text-gray-500'} mt-1`}>
             Add a custom CDT code to check its applicability.
           </p>
         </div>
      </div>
    );
  };

  // Count questions with text
  const getValidQuestionsCount = () => {
    return questions.filter(q => q.text.trim() !== '').length;
  };

  // Count pending questioners (in queue)
  const getPendingQuestionersCount = () => {
     // Count based on questions state directly instead of queue
     return questions.filter(q =>
       q.result?.data?.questioner_data?.has_questions && !q.processedQuestioner
     ).length;
  };

  return (
    <div className="flex-grow flex justify-center p-4">
      <div className={`w-full max-w-4xl ${isDark ? 'bg-gray-800' : 'bg-white'} rounded-lg shadow-lg p-6 transition-colors`}>
        {/* Header */}
        <div className={`${isDark ? 'bg-blue-900' : 'bg-blue-500'} text-white p-4 rounded-lg mb-6 flex flex-wrap justify-between items-center gap-2`}>
          <h2 className="text-xl md:text-2xl font-semibold flex items-center flex-wrap gap-x-2">
            <FaTooth className="mr-1" /> Multiple Dental Scenarios
            {activeRequests > 0 && (
              <span className="text-sm bg-green-500 px-2 py-0.5 rounded-full whitespace-nowrap">
                {activeRequests} Active
              </span>
            )}
            {getPendingQuestionersCount() > 0 && (
              <span className="text-sm bg-yellow-500 text-black px-2 py-0.5 rounded-full whitespace-nowrap">
                {getPendingQuestionersCount()} Pending Qs
              </span>
            )}
          </h2>
          <div className="flex space-x-2">
             {/* Cancel Button */}
            {(batchLoading || activeRequests > 0) && (
              <button
                onClick={cancelProcessing}
                className={`${isDark ? 'bg-red-700 hover:bg-red-600' : 'bg-red-600 hover:bg-red-500'}
                text-white px-3 py-2 rounded-lg transition-colors flex items-center text-sm`}
                title="Cancel all ongoing analyses"
              >
                <FaStop className="inline mr-1" />
                Cancel All
              </button>
            )}
             {/* Analyze All Button */}
            <button
              onClick={analyzeAllQuestions}
              className={`${
                batchLoading || activeRequests > 0 || getValidQuestionsCount() === 0
                  ? (isDark ? 'bg-gray-700 text-gray-400' : 'bg-gray-400 text-gray-700')
                  : (isDark ? 'bg-green-700 hover:bg-green-600' : 'bg-green-600 hover:bg-green-500')
              } text-white px-3 py-2 rounded-lg transition-colors flex items-center text-sm`}
              disabled={batchLoading || activeRequests > 0 || getValidQuestionsCount() === 0}
            >
              {batchLoading ? (
                <>
                  <FaSpinner className="inline mr-1 animate-spin" />
                  Processing...
                </>
              ) : (
                <>
                  <FaPaperPlane className="inline mr-1" />
                  Analyze All ({getValidQuestionsCount()})
                </>
              )}
            </button>
             {/* Add Question Button */}
            <button
              onClick={addQuestion}
              className={`${isDark ? 'bg-blue-700 hover:bg-blue-600' : 'bg-blue-600 hover:bg-blue-500'}
                text-white p-2 rounded-full transition-colors flex items-center`}
              disabled={batchLoading || activeRequests > 0}
              title="Add another question input"
            >
              <FaPlusCircle />
            </button>
          </div>
        </div>

        {/* Global Error */}
        {globalError && (
          <div className={`mb-4 p-4 rounded-lg ${isDark ? 'bg-red-900/30' : 'bg-red-100'} flex items-start`}>
            <FaExclamationTriangle className={`mt-1 ${isDark ? 'text-red-400' : 'text-red-600'} mr-2 flex-shrink-0`} />
            <div>
              <h3 className={`font-bold ${isDark ? 'text-red-300' : 'text-red-700'} mb-1`}>Error</h3>
              <p className={`${isDark ? 'text-red-200' : 'text-red-600'}`}>{globalError}</p>
              {globalError.includes('rate limit') && <p className="text-sm mt-1 opacity-80">Try fewer questions or wait before trying again.</p>}
            </div>
             <button onClick={() => setGlobalError(null)} className={`ml-auto text-sm ${isDark ? 'text-gray-400 hover:text-gray-200' : 'text-gray-600 hover:text-gray-800'}`}>&times;</button>
          </div>
        )}

        {/* Questions List */}
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
                  {question.result?.data?.questioner_data?.has_questions && !question.processedQuestioner && (
                    <span title="Requires answers" className={`ml-2 text-xs px-1.5 py-0.5 rounded-full ${
                      isDark ? 'bg-yellow-800/60 text-yellow-200' : 'bg-yellow-100 text-yellow-800'
                    }`}>
                      <FaExclamationTriangle className="inline mb-px" /> Qs
                    </span>
                  )}
                </h3>
                {questions.length > 1 && (
                  <button
                    onClick={() => removeQuestion(question.id)}
                    className={`${isDark ? 'text-red-400 hover:text-red-300' : 'text-red-500 hover:text-red-600'}
                      transition-colors`}
                    disabled={batchLoading || question.loading || activeRequests > 0} // Disable if any activity
                    title="Remove this question"
                  >
                    <FaMinusCircle />
                  </button>
                )}
              </div>
              
              {/* Text Area */}
              <div className="mb-3 relative">
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
                  disabled={batchLoading || question.loading || activeRequests > 0} // Disable if any activity
                ></textarea>
                 {/* Loading Spinner */}
                 {question.loading && (
                     <div className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-30 rounded-lg">
                         <FaSpinner className={`animate-spin text-3xl ${isDark ? 'text-blue-300' : 'text-blue-500'}`} />
                     </div>
                 )}
              </div>
              
              {/* Individual Analyze Button (Hidden if batch processing) */}
              {!batchLoading && activeRequests === 0 && (
                  <div className="flex justify-end">
                    <button
                      onClick={() => analyzeQuestion(question.id)}
                      disabled={!question.text.trim()}
                      className={`${
                        !question.text.trim()
                          ? (isDark ? 'bg-gray-600 text-gray-400' : 'bg-gray-400 text-gray-700')
                          : (isDark ? 'bg-blue-700 hover:bg-blue-600' : 'bg-blue-600 hover:bg-blue-700')
                      } text-white px-4 py-2 rounded-lg shadow-md transition-all duration-300 flex items-center text-sm`}
                    >
                      <FaPaperPlane className="inline mr-2" />
                      Analyze This
                    </button>
                  </div>
              )}
              
              {/* Individual Error */}
              {question.error && !globalError && ( // Show only if no global error
                <div className={`mt-4 p-3 rounded-lg ${isDark ? 'bg-red-900/30 text-red-200' : 'bg-red-100 text-red-700'}`}>
                  Error: {question.error}
                </div>
              )}
              
              {/* Render Results Section */}
              {renderResults(question)}
            </div>
          ))}
        </div>

        {/* Questioner Modal */}
        {isQuestionerVisible && currentQuestionerData && ( // Removed currentRecordId check
          <Questioner
            isVisible={isQuestionerVisible}
            onClose={() => {
              console.log("Questioner closed by user");
              setIsQuestionerVisible(false);
              setCurrentQuestionerData(null);
              // Mark any associated questions as processed so modal doesn't re-appear immediately if closed without submit
               setQuestions(prevQuestions => prevQuestions.map(q =>
                 currentQuestionerData.scenarios.some(s => s.questionId === q.id)
                   ? { ...q, processedQuestioner: true }
                   : q
               ));
            }}
            questions={{
              cdt_questions: currentQuestionerData.cdt_questions?.questions || [],
              icd_questions: currentQuestionerData.icd_questions?.questions || []
            }}
            // recordId prop removed as it's handled internally now
            onSubmitSuccess={handleQuestionerSubmitSuccess}
            scenarios={currentQuestionerData.scenarios || []}
          />
        )}

      </div>
    </div>
  );
};

export default Questions; 