import { FaCogs, FaCopy, FaSpinner, FaPlus, FaChevronDown, FaChevronUp, FaSave, FaQuestionCircle, FaTrophy, FaFileUpload } from 'react-icons/fa';
import { analyzeDentalScenario, addCustomCode, submitSelectedCodes } from '../../interceptors/services.js';
import { useState, useEffect, useRef } from 'react';
import PropTypes from 'prop-types';
import Questioner from './Questioner.jsx';
import { useTheme } from '../../context/ThemeContext';
import Loader from '../Modal/Loading.jsx';
import { message } from 'antd';
import { driver } from 'driver.js';
import 'driver.js/dist/driver.css';
import '../../styles/driverjs.css';
import TourConfetti from '../Tour/TourConfetti';
import { useAuth } from '../../context/AuthContext';
import { updateTourStatus } from '../../interceptors/services';
import { useNavigate } from 'react-router-dom';

// Helper function to escape regex special characters
const escapeRegex = (string) => {
  // Escape characters with special meaning in regex.
  // Handles cases like '.' in ICD codes (e.g., K08.89)
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); // $& means the whole matched string
}

// Add this animated welcome component
const AnimatedWelcome = ({ isVisible, onClose }) => {
  if (!isVisible) return null;
  
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 backdrop-blur-sm">
      <div className="bg-gradient-to-br from-white to-blue-50 dark:from-gray-800 dark:to-gray-900 p-8 rounded-xl shadow-2xl max-w-lg w-full mx-4 transform animate-[fadeInScale_0.6s_ease-out]">
        <div className="text-center">
          <div className="flex justify-center mb-6">
            <div className="w-24 h-24 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-full flex items-center justify-center mb-4 animate-pulse">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 text-white animate-[spin_3s_linear_infinite]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905a3.61 3.61 0 01-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5" />
              </svg>
            </div>
          </div>
          <h2 className="text-3xl font-bold mb-4 text-[var(--color-text-primary)] bg-gradient-to-r from-blue-500 to-indigo-600 bg-clip-text text-transparent animate-[pulse_2s_ease-in-out_infinite]">
            Welcome to Dental Coding Assistant
          </h2>
          <p className="text-[var(--color-text-secondary)] mb-6 leading-relaxed">
            You&apos;re now ready to use all the powerful features of our AI-powered coding tool.
            Our system will help you analyze dental scenarios and generate accurate billing codes.
          </p>
          <div className="flex flex-wrap justify-center gap-4">
            <button
              onClick={onClose}
              className="px-6 py-3 bg-gradient-to-r from-[var(--color-primary)] to-blue-600 text-white rounded-lg hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1"
            >
              Get Started
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

AnimatedWelcome.propTypes = {
  isVisible: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired
};

const Home = () => {
  useTheme();
  const navigate = useNavigate();
  const { user } = useAuth(); // Get user data from auth context
  const [scenario, setScenario] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [selectedCodes, setSelectedCodes] = useState({ accepted: [], denied: [] });
  const [showQuestioner, setShowQuestioner] = useState(false);
  const [newCode, setNewCode] = useState('');
  const [loadingProgress, setLoadingProgress] = useState(0);
  const [activeCodeDetail, setActiveCodeDetail] = useState(null);
  const [isAddingCode, setIsAddingCode] = useState(false);
  const [expandedHistoryRows, setExpandedHistoryRows] = useState({});
  const [allCodeDetailsMap, setAllCodeDetailsMap] = useState({});
  const [showFullCdtExplanation, setShowFullCdtExplanation] = useState(false);
  const [showFullIcdExplanation, setShowFullIcdExplanation] = useState(false);
  const [customCodes, setCustomCodes] = useState({ cdt: [], icd: [] }); // State for custom codes
  const [isSubmittingCodes, setIsSubmittingCodes] = useState(false);
  const [showTour, setShowTour] = useState(false);
  const [showConfetti, setShowConfetti] = useState(false);
  const [showCompletionModal, setShowCompletionModal] = useState(false);
  const [showWelcomeMessage, setShowWelcomeMessage] = useState(false);
  const driverRef = useRef(null);

  // Check if there are questions in the result
  useEffect(() => {
    if (result && result.questioner_data && result.questioner_data.has_questions) {
      setShowQuestioner(true);
    } else {
      setShowQuestioner(false);
    }
  }, [result]);

  // Fake progress simulation
  useEffect(() => {
    let progressInterval;
    
    if (loading) {
      setLoadingProgress(0);
      const totalTime = 550000; // 5.5 minutes in milliseconds
      const intervalTime = 1000; // Update every second
      const increments = totalTime / intervalTime;
      const incrementAmount = 100 / increments;
      
      progressInterval = setInterval(() => {
        setLoadingProgress(prevProgress => {
          const newProgress = prevProgress + incrementAmount;
          // Cap at 95% so it doesn't look complete before the actual data arrives
          return newProgress >= 95 ? 95 : newProgress;
        });
      }, intervalTime);
    } else {
      // Reset progress when loading is complete
      setLoadingProgress(0);
    }
    
    return () => {
      if (progressInterval) clearInterval(progressInterval);
    };
  }, [loading]);

  // Listen for the newAnalysis event from Navbar
  useEffect(() => {
    const resetForm = (event) => {
      console.log("New analysis event received, resetting form", event.detail);
      setScenario('');
      setResult(null);
      setSelectedCodes({ accepted: [], denied: [] });
      setNewCode('');
      setActiveCodeDetail(null);
    };

    window.addEventListener('newAnalysis', resetForm);
    
    return () => {
      window.removeEventListener('newAnalysis', resetForm);
    };
  }, []);

  // Consolidate all code details into a map for easier lookup
  useEffect(() => {
    const detailsMap = {};
    if (!result) {
      setAllCodeDetailsMap({});
      return;
    }

    // 1. Process CDT Topic Activation Results for detailed explanations
    if (result.cdt_topic_activation_results && Array.isArray(result.cdt_topic_activation_results)) {
      result.cdt_topic_activation_results.forEach(topic => {
        const topicName = topic.topic || 'Unknown Topic';
        if (topic.raw_result?.subtopics_data && Array.isArray(topic.raw_result.subtopics_data)) {
          topic.raw_result.subtopics_data.forEach(subtopic => {
            const subtopicName = subtopic.topic || 'Unknown Subtopic';
            // Check the new structure with parsed_result
            if (subtopic.parsed_result && Array.isArray(subtopic.parsed_result)) {
               subtopic.parsed_result.forEach(parsedEntry => {
                  if (parsedEntry?.specific_codes && Array.isArray(parsedEntry.specific_codes)) {
                     parsedEntry.specific_codes.forEach(code => {
                        if (code && !detailsMap[code]) { // Prioritize first explanation found
                           detailsMap[code] = {
                              code: code,
                              type: 'CDT',
                              explanation: parsedEntry.explanation || 'No explanation provided.',
                              doubt: parsedEntry.doubt || 'None',
                              topic: topicName,
                              subtopic: subtopicName
                           };
                        }
                     });
                  }
               });
            }
          });
        }
      });
    }

    // 2. Process ICD Topic Activation Result
    const icdTopic = result.icd_topic_activation_results;
    if (icdTopic?.raw_result?.code && icdTopic.raw_result.code !== 'none') {
       const code = icdTopic.raw_result.code;
       if (!detailsMap[code]) {
          detailsMap[code] = {
             code: code,
             type: 'ICD-10',
             explanation: icdTopic.raw_result.explanation || 'No explanation provided.',
             doubt: icdTopic.raw_result.doubt || 'None',
             topic: icdTopic.topic || 'ICD Topic',
             subtopic: null
          };
       }
    }

    // 3. Add info for codes from Inspector results if not already mapped
    const inspectorCdtCodes = result.inspector_results?.cdt?.codes || [];
    const inspectorIcdCodes = result.inspector_results?.icd?.codes || [];
    const inspectorCdtExplanation = result.inspector_results?.cdt?.explanation || '';
    const inspectorIcdExplanation = result.inspector_results?.icd?.explanation || '';

    // Function to extract explanation for a specific code from the inspector string
    const getInspectorExplanation = (code, explanationString) => {
      // Escape characters with special meaning in regex.
      const escapedCode = escapeRegex(code);
      // Create regex to match the code explanation
      try {
        // Use a simpler regex pattern that's less prone to escaping issues
        const regex = new RegExp(`- \\*\\*${escapedCode}(?:\\s*\\([^)]*\\))?\\*\\*:\\s*Selected\\.\\s*(.*?)(?=\\s*-\\s*\\*\\*|$)`, 'i');
        const match = explanationString.match(regex);
        return match ? match[1].trim() : 'Explanation from final inspection result.'; // Fallback explanation
      } catch (e) {
        console.warn(`Failed to parse explanation for code ${code}:`, e);
        return 'Explanation unavailable due to parsing error.';
      }
    };

    inspectorCdtCodes.forEach(code => {
      if (code && !detailsMap[code]) {
        detailsMap[code] = {
          code: code,
          type: 'CDT',
          explanation: getInspectorExplanation(code, inspectorCdtExplanation),
          doubt: 'N/A',
          topic: 'Final Selection (Inspector)',
          subtopic: null
        };
      }
    });

    inspectorIcdCodes.forEach(code => {
      if (code && !detailsMap[code]) {
        detailsMap[code] = {
          code: code,
          type: 'ICD-10',
          // ICD inspector explanation might be general, not per-code
          explanation: inspectorIcdExplanation || 'Explanation from final inspection result.',
          doubt: 'N/A',
          topic: 'Final Selection (Inspector)',
          subtopic: null
        };
      }
    });

    // 4. Add rejected codes from inspector if not present
    const rejectedCdt = result.inspector_results?.cdt?.rejected_codes || [];
    const rejectedIcd = result.inspector_results?.icd?.rejected_codes || [];

     rejectedCdt.forEach(code => {
       if (code && !detailsMap[code]) {
         detailsMap[code] = {
           code: code,
           type: 'CDT',
           explanation: 'Code was suggested but rejected during final inspection.',
           doubt: 'N/A',
           topic: 'Rejected Suggestion',
           subtopic: null
         };
       }
     });
     rejectedIcd.forEach(code => {
       if (code && !detailsMap[code]) {
         detailsMap[code] = {
           code: code,
           type: 'ICD-10',
           explanation: 'Code was suggested but rejected during final inspection.',
           doubt: 'N/A',
           topic: 'Rejected Suggestion',
           subtopic: null
         };
       }
     });

    console.log("Generated allCodeDetailsMap from result:", detailsMap);
    setAllCodeDetailsMap(detailsMap);
  }, [result]);

  // Initialize Driver.js
  useEffect(() => {
    // Create a new Driver instance with customized options
    driverRef.current = driver({
      className: 'custom-driver-js',
      animate: true,
      opacity: 0.75,
      padding: 5,
      allowClose: true,
      overlayClickNext: false,
      showProgress: true,
      stagePadding: 10,
      disableActiveInteraction: false, // Allow interaction with highlighted elements
      onHighlightStarted: (element) => {
        // Add a subtle animation to highlighted element
        if (element) {
          element.style.transition = 'transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out';
          element.style.transform = 'scale(1.03)';
          element.style.boxShadow = '0 0 0 5px rgba(var(--color-primary-rgb), 0.3)';
        }
      },
      onHighlighted: (element) => {
        // Pulse animation for the highlighted element
        if (element) {
          element.animate([
            { boxShadow: '0 0 0 5px rgba(var(--color-primary-rgb), 0.3)' },
            { boxShadow: '0 0 0 8px rgba(var(--color-primary-rgb), 0.1)' },
            { boxShadow: '0 0 0 5px rgba(var(--color-primary-rgb), 0.3)' }
          ], {
            duration: 1500,
            iterations: Infinity
          });
        }
      },
      onDeselected: (element) => {
        if (element) {
          element.style.transform = 'scale(1)';
          element.style.boxShadow = 'none';
          
          // Stop any ongoing animations
          element.getAnimations().forEach(animation => {
            animation.cancel();
          });
        }
      },
      onDestroyed: () => {
        setShowTour(false);
        
        // Check if this was a normal completion (not a skip)
        const hasCompletedTour = localStorage.getItem('hasCompletedTour');
        if (!hasCompletedTour) {
          localStorage.setItem('hasCompletedTour', 'true');
          setShowConfetti(true);
          
          // Show welcome message after a short delay
          setTimeout(() => {
            setShowWelcomeMessage(true);
          }, 800);
        }
      }
    });

    // Check if user has seen the tour
    const checkTourStatus = () => {
      // If user exists and has_seen_tour is false, show the tour
      if (user && user.has_seen_tour === false) {
        setTimeout(() => {
          setShowTour(true);
        }, 1000); // Wait 1 second before starting the tour
      }
    };
    
    checkTourStatus();
  }, [user]);

  // Start the tour when showTour changes
  useEffect(() => {
    if (showTour && driverRef.current) {
      startTour();
    }
  }, [showTour]);

  // Define the tour steps with enhanced descriptions
  const startTour = () => {
    if (!driverRef.current) return;

    const steps = [
      {
        element: '#tour-header',
        popover: {
          title: '👋 Welcome to the Dental Coding Assistant',
          description: 'This premium AI-powered tool analyzes dental scenarios and generates accurate billing codes. Let\'s explore its powerful features!',
          side: "bottom",
          align: 'center'
        }
      },
      {
        element: '#tour-input-notes',
        popover: {
          title: '📝 Clinical Notes Input',
          description: 'Enter your patient\'s clinical notes in this area. Our advanced AI will analyze the text to identify relevant procedures and conditions.',
          side: "top",
          align: 'start'
        }
      },
      {
        element: '#tour-pdf-upload',
        popover: {
          title: '📄 PDF Document Upload',
          description: 'Save time by directly uploading PDF documents. Our system will extract and analyze the clinical notes automatically.',
          side: "top",
          align: 'center'
        }
      },
      {
        element: '#tour-process-btn',
        popover: {
          title: '⚙️ Process Input',
          description: 'Click here to start the AI analysis. Our system will identify applicable CDT and ICD-10 codes based on the clinical scenario.',
          side: "right",
          align: 'start'
        }
      },
      {
        element: '#tour-final-codes',
        popover: {
          title: '✅ Final Codes',
          description: 'Generated codes appear here. Click on any code to accept or reject it. Accepted codes will be highlighted in green, rejected in red.',
          side: "left",
          align: 'center'
        }
      },
      {
        element: '#tour-custom-code',
        popover: {
          title: '➕ Custom Code Analysis',
          description: 'Need to check a specific code? Add it here, and our AI will analyze if it applies to the current scenario, providing detailed reasoning.',
          side: "top",
          align: 'center'
        }
      },
      {
        element: '#tour-explanation',
        popover: {
          title: '📋 Comprehensive Explanation',
          description: 'Review the AI\'s detailed rationale for code selection. This helps you understand why certain codes were recommended.',
          side: "top",
          align: 'center'
        }
      },
      {
        element: '#tour-code-details',
        popover: {
          title: '🔍 Code Details',
          description: 'Click any code to see its detailed information in this panel, including explanations of why it applies to the current scenario.',
          side: "top",
          align: 'center'
        }
      },
      {
        element: '#tour-history',
        popover: {
          title: '📊 Code Generation History',
          description: 'Track all codes generated for the current analysis session, with clear explanations for each selection.',
          side: "top",
          align: 'start'
        }
      },
      {
        element: '#tour-submit-btn',
        popover: {
          title: '💾 Submit Your Selections',
          description: 'When you\'re satisfied with your code selections, click here to submit and save them to the system.',
          side: "left",
          align: 'center'
        }
      }
    ];

    // Create and start the tour
    driverRef.current.setSteps(steps);
    driverRef.current.drive();
    
    // Update tour status in the backend after starting the tour
    updateTourStatus(true)
      .then(() => {
        console.log('Tour status updated successfully');
      })
      .catch(error => {
        console.error('Failed to update tour status:', error);
      });
  };

  // Function to restart the tour anytime
  const restartTour = () => {
    setShowConfetti(false);
    setShowCompletionModal(false);
    setShowTour(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    setSelectedCodes({ accepted: [], denied: [] });

    try {
      const response = await analyzeDentalScenario({ scenario });
      console.log('Analysis results received:', response);
      console.log('Record ID:', response?.record_id);
      setResult(response);
      message.success('Analysis complete!');
    } catch (err) {
      console.error('Error analyzing scenario:', err);
      message.error('Analysis failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleCodeSelection = (code, action) => {
    setSelectedCodes(prev => {
      const newState = { ...prev };
      
      // Remove code from both lists if it exists
      newState.accepted = newState.accepted.filter(c => c !== code);
      newState.denied = newState.denied.filter(c => c !== code);
      
      // Add to appropriate list
      if (action === 'accept') {
        newState.accepted.push(code);
      } else if (action === 'deny') {
        newState.denied.push(code);
      }
      
      return newState;
    });
  };

  const handleQuestionerClose = () => {
    setShowQuestioner(false);
  };

  const handleQuestionerSuccess = (response) => {
    // If response is an array (batch), check if ALL were successful
    const allSuccess = Array.isArray(response)
      ? response.every(r => r.response && r.response.status === 'success')
      : response && response.status === 'success';

    if (allSuccess) {
       // For batch, we might need to update the result state based on multiple responses.
       // For now, let's assume a single response structure or handle the first successful one for simplicity.
      const mainResponse = Array.isArray(response) ? response.find(r => r.response && r.response.status === 'success')?.response : response;
      if (mainResponse) {
          setResult(mainResponse); // Update result with the data returned AFTER answering questions
      }
    } else {
      // Handle single or batch error
      // const errorMsg = Array.isArray(response) // Removed unused errorMsg assignment
      //   ? response.find(r => r.response && r.response.status === 'error')?.response?.message || 'An error occurred in batch processing.'
      //   : response?.message || 'Failed to process answers';
      // Don't hide the questioner modal on error
    }
  };


  const handleAddCustomCode = async () => {
    if (!newCode.trim()) {
      message.warning("Please enter a code.");
      return;
    }

    const codeType = document.getElementById('codeType').value; // Read the selected code type

    // Check if code already exists (client-side check before API call)
    if (selectedCodes.accepted.includes(newCode) || selectedCodes.denied.includes(newCode)) {
       message.warning(`${newCode} has already been processed.`);
       setNewCode('');
       return;
    }

    setIsAddingCode(true);
    try {
      // Ensure result and record_id exist before proceeding
      if (!result?.record_id) {
        message.error("Cannot add custom code without a processed scenario record ID.");
        setIsAddingCode(false);
        return;
      }

      const response = await addCustomCode(newCode, scenario, result.record_id, codeType);
      console.log("Add Custom Code API response:", response);

      // OPTIONAL: Update UI based on response.data if backend returns updated state
      // For now, just add it client-side assuming success
      if (response.status === 'success' && response.data?.code_data) {
        const { code, isApplicable, explanation, doubt } = response.data.code_data;

        // Update selection state
        setSelectedCodes(prev => ({
          ...prev,
          accepted: isApplicable ? [...prev.accepted.filter(c => c !== code), code] : prev.accepted.filter(c => c !== code),
          denied: !isApplicable ? [...prev.denied.filter(c => c !== code), code] : prev.denied.filter(c => c !== code)
        }));

        // Update the details map state with the new custom code info
        setAllCodeDetailsMap(prevMap => ({
          ...prevMap,
          [code]: {
            code: code,
            type: codeType === 'ICD' ? 'ICD-10' : 'CDT', // Use the type read from dropdown
            explanation: explanation || 'Custom code analysis result.', // Use the explanation from API
            doubt: doubt || 'N/A',
            topic: 'Custom Code',
            subtopic: null,
            isApplicable: isApplicable, // Store applicability
            custom: true // Mark as custom code
          }
        }));

        // Add to custom codes state
        setCustomCodes(prevCustom => {
          const newCustom = { ...prevCustom };
          const targetList = codeType === 'ICD' ? 'icd' : 'cdt';
          // Avoid duplicates in custom list
          if (!newCustom[targetList].includes(code)) {
            newCustom[targetList] = [...newCustom[targetList], code];
          }
          return newCustom;
        });

        setActiveCodeDetail(code); // Show details for the new code
        message.success(response.message || `Processed custom code: ${code}`);
        setNewCode('');
      } else {
        message.error(response.message || 'Failed to process custom code analysis.');
      }
    } catch (apiError) {
      console.error("Error calling addCustomCode API:", apiError);
      message.error(apiError.message || 'An error occurred while adding the custom code.');
    } finally {
      setIsAddingCode(false);
    }
  };

  // Helper function to count code occurrences
  const countCodes = (codes) => {
    return codes.reduce((acc, code) => {
      acc[code] = (acc[code] || 0) + 1;
      return acc;
    }, {});
  };

  const handleSubmitCodes = async () => {
    if (!result?.record_id) {
      message.error('Cannot submit codes without a processed scenario record ID.');
      return;
    }

    if (selectedCodes.accepted.length === 0) {
      message.warning('Please select at least one code to submit.');
      return;
    }

    // Separate codes into CDT and ICD categories
    const acceptedCdtCodes = selectedCodes.accepted.filter(code => code.startsWith('D'));
    const acceptedIcdCodes = selectedCodes.accepted.filter(code => !code.startsWith('D'));
    
    const deniedCdtCodes = selectedCodes.denied.filter(code => code.startsWith('D'));
    const deniedIcdCodes = selectedCodes.denied.filter(code => !code.startsWith('D'));

    // Create properly structured payload
    const payload = {
      cdt_codes: acceptedCdtCodes,
      rejected_cdt_codes: deniedCdtCodes,
      icd_codes: acceptedIcdCodes,
      rejected_icd_codes: deniedIcdCodes
    };

    console.log('Submitting codes with structured payload:', payload);
    
    setIsSubmittingCodes(true);
    try {
      const response = await submitSelectedCodes(payload, result.record_id);
      console.log('Submit codes response:', response);
      message.success('Codes submitted successfully!');
    } catch (error) {
      console.error('Error submitting codes:', error);
      message.error(error.message || 'Failed to submit codes. Please try again.');
    } finally {
      setIsSubmittingCodes(false);
    }
  };

  return (
    <div className="flex-1 p-4 md:p-8 bg-[var(--color-bg-primary)] text-[var(--color-text-primary)]">
      {/* Tour Confetti Effect */}
      <TourConfetti isActive={showConfetti} />
      
      {/* Animated Welcome Message */}
      <AnimatedWelcome 
        isVisible={showWelcomeMessage} 
        onClose={() => setShowWelcomeMessage(false)} 
      />
      
      {/* Tour Completion Modal - hide this if we're using the welcome message instead */}
      {false && showCompletionModal && (
        <div className="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center z-50 backdrop-blur-sm">
          <div className="bg-[var(--color-bg-secondary)] p-6 rounded-xl shadow-2xl max-w-md w-full mx-4 transform tour-completion-modal">
            <div className="text-center">
              <div className="w-20 h-20 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-full mx-auto flex items-center justify-center mb-4">
                <FaTrophy className="text-3xl text-white trophy-icon" />
              </div>
              <h2 className="text-2xl font-bold mb-2 text-[var(--color-text-primary)]">Tour Completed!</h2>
              <p className="text-[var(--color-text-secondary)] mb-6">
                You&apos;re now ready to use all the powerful features of the Dental Coding Assistant.
                Need to review the tour again? You can restart it anytime!
              </p>
              <div className="flex justify-center gap-4">
                <button
                  onClick={() => setShowCompletionModal(false)}
                  className="px-6 py-2 border border-[var(--color-border)] rounded-lg hover:bg-[var(--color-bg-primary)] transition-colors text-[var(--color-text-primary)]"
                >
                  Get Started
                </button>
                <button
                  onClick={restartTour}
                  className="px-6 py-2 bg-gradient-to-r from-[var(--color-primary)] to-blue-600 text-white rounded-lg hover:opacity-90 transition-opacity"
                >
                  Restart Tour
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
      
      {/* Help Button for Tour */}
      <div className="fixed bottom-6 right-6 z-40 flex flex-col items-end gap-3">
        <button
          onClick={restartTour}
          className="bg-gradient-to-r from-[var(--color-primary)] to-blue-600 hover:from-blue-600 hover:to-[var(--color-primary)] text-white p-3 rounded-full shadow-lg hover:shadow-xl transition-all duration-300 group"
          title="Start Tour"
        >
          <FaQuestionCircle className="text-xl group-hover:animate-bounce" />
        </button>
      </div>
      
      {/* Main Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Input Section */}
        <div id="tour-header" className="bg-[var(--color-bg-secondary)] p-6 rounded-xl shadow-lg col-span-1 md:col-span-2">
          <h3 className="text-lg font-bold tracking-tight mb-4 text-[var(--color-text-primary)]">Input Clinical Notes</h3>
          <div className="mb-4">
            <label className="block text-[var(--color-text-secondary)] mb-2 text-sm font-medium">Raw Text Input</label>
            <textarea
              id="tour-input-notes"
              value={scenario}
              onChange={(e) => setScenario(e.target.value)}
              className="w-full border rounded-lg p-3 bg-[var(--color-input-bg)] text-[var(--color-text-primary)] border-[var(--color-border)] focus:ring-2 focus:ring-[var(--color-primary)] text-sm font-light leading-relaxed"
              rows="5"
              placeholder="Enter clinical notes (e.g., Patient has tooth decay in molar, requires filling)"
            />
          </div>
          <div className="mb-4">
            <label className="block text-[var(--color-text-secondary)] mb-2 text-sm font-medium">Upload PDF</label>
            <div 
              id="tour-pdf-upload"
              onClick={() => navigate('/extractor')}
              className="border-2 border-dashed border-[var(--color-border)] p-6 rounded-lg text-center hover:border-[var(--color-primary)] transition-colors cursor-pointer flex flex-col items-center justify-center"
            >
              <FaFileUpload className="text-2xl text-[var(--color-text-secondary)] mb-2" />
              <p className="text-[var(--color-text-secondary)] text-sm font-light leading-relaxed">
                Click to go to PDF Extractor
              </p>
            </div>
          </div>
          <button
            id="tour-process-btn"
            onClick={handleSubmit}
            disabled={loading}
            className="bg-[var(--color-primary)] hover:bg-[var(--color-primary-hover)] text-white px-4 py-2 text-sm rounded-lg hover:scale-105 hover:shadow-lg focus:ring-2 focus:ring-[var(--color-primary)] font-medium transition-all duration-200"
          >
            {loading ? (
              <>
                <FaSpinner className="animate-spin inline mr-2" />
                Processing...
              </>
            ) : (
              <>
                <FaCogs className="inline mr-2" />
                Process Input
              </>
            )}
          </button>
        </div>

        {/* Final Codes Section - Add id for tour */}
        <div id="tour-final-codes" className="bg-[var(--color-bg-secondary)] p-6 rounded-xl shadow-lg hover:shadow-xl transition-all duration-200 space-y-6">
          {/* Header: Title and Copy Button */}
          <div className="flex justify-between items-center">
            <h3 className="text-lg font-bold tracking-tight text-[var(--color-text-primary)]">Final Codes</h3>
            <div className="flex space-x-2">
              <button
                onClick={() => {
                  // Get all accepted codes, including both inspector results and custom codes
                  const finalAcceptedCdt = [
                    ...(result?.inspector_results?.cdt?.codes || []).filter(code => selectedCodes.accepted.includes(code)),
                    ...customCodes.cdt.filter(code => selectedCodes.accepted.includes(code))
                  ];
                  
                  const finalAcceptedIcd = [
                    ...(result?.inspector_results?.icd?.codes || []).filter(code => selectedCodes.accepted.includes(code)),
                    ...customCodes.icd.filter(code => selectedCodes.accepted.includes(code))
                  ];
                  
                  const allAccepted = [...finalAcceptedCdt, ...finalAcceptedIcd];
                  if (allAccepted.length === 0) {
                    message.warning('No accepted codes to copy.');
                    return;
                  }
                  const textToCopy = allAccepted.join(', ');
                  navigator.clipboard.writeText(textToCopy)
                    .then(() => message.success(`Copied: ${textToCopy}`))
                    .catch(() => message.error('Failed to copy codes.'));
                }}
                disabled={!selectedCodes.accepted.length}
                className="bg-[var(--color-primary)] hover:bg-[var(--color-primary-hover)] text-white px-3 py-1 text-sm rounded-lg hover:scale-105 hover:shadow-lg focus:ring-2 focus:ring-[var(--color-primary)] flex items-center font-medium disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <FaCopy className="mr-2 md:mr-0 lg:mr-2" /> <span className="hidden md:hidden lg:inline">Copy Selected</span>
              </button>
              <button
                onClick={handleSubmitCodes}
                disabled={isSubmittingCodes || !result?.record_id || selectedCodes.accepted.length === 0}
                className="bg-green-600 hover:bg-green-700 text-white px-3 py-1 text-sm rounded-lg hover:scale-105 hover:shadow-lg focus:ring-2 focus:ring-green-500 flex items-center font-medium disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isSubmittingCodes ? (
                  <>
                    <FaSpinner className="animate-spin mr-2 md:mr-0 lg:mr-2" /> 
                    <span className="hidden md:hidden lg:inline">Submitting...</span>
                  </>
                ) : (
                  <>
                    <FaSave className="mr-2 md:mr-0 lg:mr-2" /> 
                    <span className="hidden md:hidden lg:inline">Submit</span>
                  </>
                )}
              </button>
            </div>
          </div>

          {/* Custom Code Input Form - Add id for tour*/}
          <div id="tour-custom-code" className="mb-4">
            <h4 className="text-sm font-semibold text-[var(--color-text-secondary)] mb-2">Add Custom Code</h4>
            <div className="flex flex-col sm:flex-row flex-wrap gap-2">
              <input
                type="text"
                value={newCode}
                onChange={(e) => setNewCode(e.target.value)}
                className="flex-1 border rounded-lg p-2 text-sm bg-[var(--color-input-bg)] text-[var(--color-text-primary)] border-[var(--color-border)] focus:ring-2 focus:ring-[var(--color-primary)] font-light leading-relaxed"
                placeholder="Enter code (e.g., D0120)"
              />
              <select
                id="codeType"
                className="border rounded-lg p-2 text-sm bg-[var(--color-input-bg)] text-[var(--color-text-primary)] border-[var(--color-border)] focus:ring-2 focus:ring-[var(--color-primary)] font-light leading-relaxed"
              >
                <option value="CDT">CDT</option>
                <option value="ICD">ICD-10</option>
              </select>
              <button
                onClick={handleAddCustomCode}
                className="inline-flex items-center justify-center bg-[var(--color-primary)] hover:bg-[var(--color-primary-hover)] text-white px-4 py-2 text-xs rounded-lg hover:scale-105 focus:outline-none focus:ring-2 focus:ring-offset-1 focus:ring-[var(--color-primary)] font-medium transition-all duration-200 disabled:opacity-60 disabled:cursor-not-allowed min-w-[60px]"
                disabled={isAddingCode || loading}
              >
                {isAddingCode ? (
                  <FaSpinner className="animate-spin h-3 w-3" />
                ) : (
                  <>
                    <FaPlus className="-ml-1 mr-1 h-3 w-3" /> Add
                  </>
                )}
              </button>
            </div>
          </div>

          {/* Code Output */}
          <div className="space-y-4">
            {/* CDT Codes */}
            <div className="border border-[var(--color-border)] bg-[var(--color-input-bg)] p-4 rounded-lg shadow-md">
              <div className="flex justify-between items-center mb-2">
                <h4 className="text-lg font-semibold text-[var(--color-text-primary)]">CDT Codes</h4>
                <button
                  onClick={() => {
                    const acceptedCdtCodes = [
                      ...(result?.inspector_results?.cdt?.codes || []).filter(code => selectedCodes.accepted.includes(code)),
                      ...customCodes.cdt.filter(code => selectedCodes.accepted.includes(code))
                    ];
                    
                    if (acceptedCdtCodes.length === 0) {
                      message.warning('No accepted CDT codes to copy.');
                      return;
                    }
                    const textToCopy = acceptedCdtCodes.join(', ');
                    navigator.clipboard.writeText(textToCopy)
                      .then(() => message.success(`Copied CDT: ${textToCopy}`))
                      .catch(() => message.error('Failed to copy CDT codes.'));
                  }}
                  disabled={!selectedCodes.accepted.some(code => code.startsWith('D') || customCodes.cdt.includes(code))}
                  className="text-[var(--color-text-secondary)] hover:text-[var(--color-primary)] hover:scale-105 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed p-1"
                  aria-label="Copy Accepted CDT Codes"
                >
                  <FaCopy />
                </button>
              </div>
              <div className="flex flex-wrap gap-2">
                {result?.inspector_results?.cdt?.codes && Object.entries(countCodes(result.inspector_results.cdt.codes)).map(([code, count], index) => (
                  <span
                    key={`${code}-${index}`}
                    onClick={() => {
                      handleCodeSelection(code, selectedCodes.accepted.includes(code) ? 'deny' : 'accept');
                      setActiveCodeDetail(code);
                    }}
                    className={`cursor-pointer px-2 py-1 rounded-full text-xs transition-all duration-200 hover:scale-105 hover:shadow-lg border
                      ${
                        selectedCodes.accepted.includes(code)
                          ? 'bg-green-100 dark:bg-green-900/60 text-green-900 dark:text-green-200 border-green-300 dark:border-green-700'
                          : selectedCodes.denied.includes(code)
                          ? 'bg-red-100 dark:bg-red-900/60 text-red-900 dark:text-red-200 border-red-300 dark:border-red-700'
                          : 'bg-[var(--color-input-bg)] text-[var(--color-text-secondary)] border-[var(--color-border)]'
                      }`}
                  >
                    {code}{count > 1 ? ` (${count} times)` : ''}
                  </span>
                ))}
                {/* Render Custom CDT Codes */}
                {customCodes.cdt.map((code, index) => (
                  <span
                    key={`custom-cdt-${code}-${index}`}
                    onClick={() => {
                      handleCodeSelection(code, selectedCodes.accepted.includes(code) ? 'deny' : 'accept');
                      setActiveCodeDetail(code);
                    }}
                    className={`cursor-pointer px-2 py-1 rounded-full text-xs transition-all duration-200 hover:scale-105 hover:shadow-lg border
                      bg-yellow-100 dark:bg-yellow-900/60 text-yellow-900 dark:text-yellow-200 border-yellow-300 dark:border-yellow-700 // Custom style
                      ${
                        selectedCodes.accepted.includes(code)
                          ? '!bg-green-100 dark:!bg-green-900/60 !text-green-900 dark:!text-green-200 !border-green-300 dark:!border-green-700' // Override if accepted
                          : selectedCodes.denied.includes(code)
                          ? '!bg-red-100 dark:!bg-red-900/60 !text-red-900 dark:!text-red-200 !border-red-300 dark:!border-red-700' // Override if denied
                          : '' // Default custom style if neither accepted/denied yet
                      }`}
                  >
                    {code} ✨
                  </span>
                ))}
              </div>
            </div>

            {/* ICD Codes */}
            <div className="border border-[var(--color-border)] bg-[var(--color-input-bg)] p-4 rounded-lg shadow-md">
              <div className="flex justify-between items-center mb-2">
                <h4 className="text-lg font-semibold text-[var(--color-text-primary)]">ICD-10 Codes</h4>
                <button
                  onClick={() => {
                    const acceptedIcdCodes = [
                      ...(result?.inspector_results?.icd?.codes || []).filter(code => selectedCodes.accepted.includes(code)),
                      ...customCodes.icd.filter(code => selectedCodes.accepted.includes(code))
                    ];
                    
                    if (acceptedIcdCodes.length === 0) {
                      message.warning('No accepted ICD-10 codes to copy.');
                      return;
                    }
                    const textToCopy = acceptedIcdCodes.join(', ');
                    navigator.clipboard.writeText(textToCopy)
                      .then(() => message.success(`Copied ICD-10: ${textToCopy}`))
                      .catch(() => message.error('Failed to copy ICD-10 codes.'));
                  }}
                  disabled={!selectedCodes.accepted.some(code => !code.startsWith('D') || customCodes.icd.includes(code))}
                  className="text-[var(--color-text-secondary)] hover:text-[var(--color-primary)] hover:scale-105 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed p-1"
                  aria-label="Copy Accepted ICD-10 Codes"
                >
                  <FaCopy />
                </button>
              </div>
              <div className="flex flex-wrap gap-2">
                {result?.inspector_results?.icd?.codes.map((code, index) => (
                  <span
                    key={`icd-code-${index}-${code}`}
                    onClick={() => {
                      handleCodeSelection(code, selectedCodes.accepted.includes(code) ? 'deny' : 'accept');
                      setActiveCodeDetail(code);
                    }}
                    className={`cursor-pointer px-2 py-1 rounded-full text-xs transition-all duration-200 hover:scale-105 hover:shadow-lg border
                      ${
                        selectedCodes.accepted.includes(code)
                          ? 'bg-green-100 dark:bg-green-900/60 text-green-900 dark:text-green-200 border-green-300 dark:border-green-700'
                          : selectedCodes.denied.includes(code)
                          ? 'bg-red-100 dark:bg-red-900/60 text-red-900 dark:text-red-200 border-red-300 dark:border-red-700'
                          : 'bg-[var(--color-input-bg)] text-[var(--color-text-secondary)] border-[var(--color-border)]'
                      }`}
                  >
                    {code}
                  </span>
                ))}
                {/* Render Custom ICD Codes */}
                 {customCodes.icd.map((code, index) => (
                  <span
                    key={`custom-icd-${code}-${index}`}
                    onClick={() => {
                      handleCodeSelection(code, selectedCodes.accepted.includes(code) ? 'deny' : 'accept');
                      setActiveCodeDetail(code);
                    }}
                    className={`cursor-pointer px-2 py-1 rounded-full text-xs transition-all duration-200 hover:scale-105 hover:shadow-lg border
                      bg-yellow-100 dark:bg-yellow-900/60 text-yellow-900 dark:text-yellow-200 border-yellow-300 dark:border-yellow-700 // Custom style
                      ${
                        selectedCodes.accepted.includes(code)
                          ? '!bg-green-100 dark:!bg-green-900/60 !text-green-900 dark:!text-green-200 !border-green-300 dark:!border-green-700' // Override if accepted
                          : selectedCodes.denied.includes(code)
                          ? '!bg-red-100 dark:!bg-red-900/60 !text-red-900 dark:!text-red-200 !border-red-300 dark:!border-red-700' // Override if denied
                          : '' // Default custom style if neither accepted/denied yet
                      }`}
                  >
                    {code} ✨
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Inspector Explanation Section - Add id for tour */}
        <div id="tour-explanation" className="bg-[var(--color-bg-secondary)] p-6 rounded-xl shadow-lg hover:shadow-xl transition-all duration-200 col-span-1 md:col-span-3 space-y-4">
          <h3 className="text-lg font-bold tracking-tight text-[var(--color-text-primary)]">Final Explanation</h3>
          {/* CDT Explanation */}
          {result?.inspector_results?.cdt?.explanation ? (
            <div className="border border-[var(--color-border)] bg-[var(--color-input-bg)] p-4 rounded-lg shadow-inner">
              <h4 className="text-md font-semibold text-[var(--color-text-primary)] mb-2">CDT Explanation</h4>
              <p className="text-sm font-light leading-relaxed text-[var(--color-text-primary)] whitespace-pre-wrap">
                {showFullCdtExplanation
                  ? result.inspector_results.cdt.explanation
                  : `${result.inspector_results.cdt.explanation.substring(0, 300)}${result.inspector_results.cdt.explanation.length > 300 ? '...' : ''}`}
              </p>
              {result.inspector_results.cdt.explanation.length > 300 && (
                <button
                  onClick={() => setShowFullCdtExplanation(!showFullCdtExplanation)}
                  className="text-[var(--color-primary)] hover:text-[var(--color-primary-hover)] hover:underline font-medium text-xs mt-2 inline-flex items-center"
                >
                  {showFullCdtExplanation ? 'Read Less' : 'Read More'}
                  {showFullCdtExplanation ? <FaChevronUp className="ml-1 h-3 w-3" /> : <FaChevronDown className="ml-1 h-3 w-3" />}
                </button>
              )}
            </div>
          ) : (
            !result?.inspector_results?.icd?.explanation && <p className="text-[var(--color-text-secondary)] text-sm">Final explanation details will appear here after processing.</p>
          )}
          {/* ICD Explanation */}
          {result?.inspector_results?.icd?.explanation && (
            <div className="border border-[var(--color-border)] bg-[var(--color-input-bg)] p-4 rounded-lg shadow-inner">
              <h4 className="text-md font-semibold text-[var(--color-text-primary)] mb-2">ICD-10 Explanation</h4>
               <p className="text-sm font-light leading-relaxed text-[var(--color-text-primary)] whitespace-pre-wrap">
                 {showFullIcdExplanation
                   ? result.inspector_results.icd.explanation
                   : `${result.inspector_results.icd.explanation.substring(0, 300)}${result.inspector_results.icd.explanation.length > 300 ? '...' : ''}`}
               </p>
               {result.inspector_results.icd.explanation.length > 300 && (
                 <button
                   onClick={() => setShowFullIcdExplanation(!showFullIcdExplanation)}
                   className="text-[var(--color-primary)] hover:text-[var(--color-primary-hover)] hover:underline font-medium text-xs mt-2 inline-flex items-center"
                 >
                   {showFullIcdExplanation ? 'Read Less' : 'Read More'}
                   {showFullIcdExplanation ? <FaChevronUp className="ml-1 h-3 w-3" /> : <FaChevronDown className="ml-1 h-3 w-3" />}
                 </button>
               )}
            </div>
          )}
        </div>

        {/* Code Details Section - Add id for tour */}
        <div id="tour-code-details" className="bg-[var(--color-bg-secondary)] p-6 rounded-xl shadow-lg hover:shadow-xl transition-all duration-200 col-span-1 md:col-span-3">
          <h3 className="text-lg font-bold tracking-tight mb-4 text-[var(--color-text-primary)]">Code Details</h3>
          <div className="border border-[var(--color-border)] bg-[var(--color-input-bg)] p-4 rounded-lg shadow-inner min-h-[100px] text-sm font-light leading-relaxed text-[var(--color-text-primary)]">
            {activeCodeDetail && allCodeDetailsMap[activeCodeDetail] ? (
              (() => { // Use IIFE to handle conditional rendering logic
                const details = allCodeDetailsMap[activeCodeDetail];
                if (details.custom) {
                  // Custom code formatting
                  const explanation = details.explanation || '';
                  const applicable = details.isApplicable;
                  // Basic parsing assuming format: "...- **Applicable?** Yes/No - **Reason**: ..."
                  const reasonMatch = explanation.match(/- \*\*Reason\*\*:\s*(.*)/s);
                  const reason = reasonMatch ? reasonMatch[1].trim() : explanation; // Fallback to full explanation

                  return (
                    <div className="space-y-2">
                      <p><strong className="font-medium text-[var(--color-text-secondary)]">Code:</strong> {details.code} ✨</p>
                      <p><strong className="font-medium text-[var(--color-text-secondary)]">Type:</strong> {details.type} (Custom)</p>
                      <p>
                        <strong className="font-medium text-[var(--color-text-secondary)]">Applicable: </strong>
                        <span className={applicable ? 'text-green-600 dark:text-green-400 font-semibold' : 'text-red-600 dark:text-red-400 font-semibold'}>
                          {applicable ? 'Yes' : 'No'}
                        </span>
                      </p>
                      <p><strong className="font-medium text-[var(--color-text-secondary)]">Reason:</strong> {reason}</p>
                    </div>
                  );
                } else {
                  // Standard code formatting
                  return (
                    <div className="space-y-2">
                      <p><strong className="font-medium text-[var(--color-text-secondary)]">Code:</strong> {details.code}</p>
                      <p><strong className="font-medium text-[var(--color-text-secondary)]">Type:</strong> {details.type}</p>
                      <p><strong className="font-medium text-[var(--color-text-secondary)]">Explanation:</strong> {details.explanation}</p>
                    </div>
                  );
                }
              })()
            ) : (
              <p className="text-[var(--color-text-secondary)]">Click a code in the &apos;Final Codes&apos; section or &apos;View Details&apos; in the summary table to see details here.</p>
            )}
          </div>
        </div>

        {/* Recent Codes Dashboard - Add id for tour */}
        <div id="tour-history" className="bg-[var(--color-bg-secondary)] p-6 rounded-xl shadow-lg col-span-1 md:col-span-3">
          <h3 className="text-lg font-bold tracking-tight mb-4 text-[var(--color-text-primary)]">Final Code Generation History</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead>
                <tr className="text-[var(--color-text-secondary)] font-medium">
                  <th className="p-2">Code</th>
                  <th className="p-2">Type</th>
                  <th className="p-2">Description</th>
                  <th className="p-2">Actions</th>
                </tr>
              </thead>
              <tbody className="font-bold text-[var(--color-text-primary)] leading-relaxed">
                {result?.inspector_results?.cdt?.codes.map((code, index) => {
                  const details = allCodeDetailsMap[code] || { type: 'CDT', explanation: 'Details not found in map.' }; // Add fallback type
                  const rowKey = `history-cdt-${code}-${index}`; // Ensure unique keys if code repeats
                  const isExpanded = expandedHistoryRows[rowKey] || false;
                  const explanation = details.explanation || 'N/A';
                  const needsReadMore = explanation.length > 100;
                  return (
                    <tr key={rowKey} className="hover:bg-[var(--color-bg-primary)] transition-colors duration-150">
                      <td className="p-2 font-medium">{code}</td>
                      <td className="p-2">{details.type}</td>
                      <td className="p-2 text-xs font-light max-w-md">
                        {needsReadMore && !isExpanded ? (
                          <>
                            {explanation.substring(0, 100)}...
                            <button
                              onClick={() => setExpandedHistoryRows(prev => ({ ...prev, [rowKey]: true }))}
                              className="text-blue-500 dark:text-blue-400 hover:underline ml-1 text-xs"
                            >
                              Read More
                            </button>
                          </>
                        ) : (
                          <>
                            {explanation}
                            {needsReadMore && isExpanded && (
                              <button
                                onClick={() => setExpandedHistoryRows(prev => ({ ...prev, [rowKey]: false }))}
                                className="text-blue-500 dark:text-blue-400 hover:underline ml-1 text-xs"
                              >
                                Read Less
                              </button>
                            )}
                          </>
                        )}
                      </td>
                      <td className="p-2">
                        <button
                          className="text-[var(--color-primary)] hover:text-[var(--color-primary-hover)] hover:underline font-medium text-xs"
                          onClick={() => setActiveCodeDetail(code)}
                        >
                          View Details
                        </button>
                      </td>
                    </tr>
                  );
                })}
                {result?.inspector_results?.icd?.codes.map((code, index) => {
                  const details = allCodeDetailsMap[code] || { type: 'ICD-10', explanation: 'Details not found in map.' }; // Add fallback type
                  const rowKey = `history-icd-${code}-${index}`; // Ensure unique keys
                  const isExpanded = expandedHistoryRows[rowKey] || false;
                  const explanation = details.explanation || 'N/A';
                  const needsReadMore = explanation.length > 100;
                  return (
                    <tr key={rowKey} className="hover:bg-[var(--color-bg-primary)] transition-colors duration-150">
                      <td className="p-2 font-medium">{code}</td>
                      <td className="p-2">{details.type}</td>
                      <td className="p-2 text-xs font-light max-w-md">
                        {needsReadMore && !isExpanded ? (
                          <>
                            {explanation.substring(0, 100)}...
                            <button
                              onClick={() => setExpandedHistoryRows(prev => ({ ...prev, [rowKey]: true }))}
                              className="text-blue-500 dark:text-blue-400 hover:underline ml-1 text-xs"
                            >
                              Read More
                            </button>
                          </>
                        ) : (
                          <>
                            {explanation}
                            {needsReadMore && isExpanded && (
                              <button
                                onClick={() => setExpandedHistoryRows(prev => ({ ...prev, [rowKey]: false }))}
                                className="text-blue-500 dark:text-blue-400 hover:underline ml-1 text-xs"
                              >
                                Read Less
                              </button>
                            )}
                          </>
                        )}
                      </td>
                      <td className="p-2">
                        <button
                          className="text-[var(--color-primary)] hover:text-[var(--color-primary-hover)] hover:underline font-medium text-xs"
                          onClick={() => setActiveCodeDetail(code)}
                        >
                          View Details
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Questioner Modal */}
      {result && (
        <Questioner
          isVisible={showQuestioner}
          onClose={handleQuestionerClose}
          questions={{
            cdt_questions: result.questioner_data?.cdt_questions?.questions || [],
            icd_questions: result.questioner_data?.icd_questions?.questions || []
          }}
          recordId={result.record_id || ''}
          onSubmitSuccess={handleQuestionerSuccess}
        />
      )}

      {/* Loading Overlay */}
      {loading && (
        <div className="fixed inset-0 bg-black bg-opacity-70 flex flex-col items-center justify-center z-50 backdrop-blur-md">
          <div className="bg-gradient-to-b from-blue-900 to-gray-900 p-10 rounded-xl shadow-2xl max-w-lg w-full mx-4">
            <div className="flex justify-center">
              <div className="w-24 h-24">
                <Loader />
              </div>
            </div>
            <h3 className="text-white text-2xl font-bold mt-6 text-center">Analyzing your scenario...</h3>
            <div className="w-full bg-blue-800/30 h-2 my-4 rounded-full overflow-hidden">
              <div
                className="bg-gradient-to-r from-blue-500 to-blue-300 h-full rounded-full transition-all duration-1000 ease-linear"
                style={{ width: `${loadingProgress}%` }}
              />
            </div>
            <p className="text-blue-100 mt-3 text-center text-sm">({Math.round(loadingProgress)}% complete)</p>
            <p className="text-blue-100 mt-4 text-center">
              Our AI typically takes about 5 minutes to think. While you wait, you can start a new analysis in a separate tab.
            </p>
            <div className="flex justify-center mt-6">
              <button
                onClick={() => window.open(window.location.href, '_blank')}
                className="flex items-center px-4 py-2 bg-blue-700 hover:bg-blue-600 text-white rounded-md transition-colors"
              >
                <FaPlus className="mr-2" />
                New Analysis in New Tab
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Home;