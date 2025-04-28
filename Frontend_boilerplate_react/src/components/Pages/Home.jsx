import { FaTooth, FaCogs, FaCheck, FaTimes, FaPaperPlane, FaRobot, FaCopy, FaSpinner, FaPlus, FaBars, FaMoon, FaSun, FaSearch, FaHome, FaUserInjured, FaFileAlt, FaDollarSign } from 'react-icons/fa';
import { analyzeDentalScenario, submitSelectedCodes, addCustomCode } from '../../interceptors/services.js';
import { useState, useEffect, useMemo } from 'react';
import Questioner from './Questioner.jsx';
import { useTheme } from '../../context/ThemeContext';
import Loader from '../Modal/Loading.jsx';

const Home = () => {
  const { isDark, toggleTheme } = useTheme();
  const [scenario, setScenario] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [selectedCodes, setSelectedCodes] = useState({ accepted: [], denied: [] });
  const [submitting, setSubmitting] = useState(false);
  const [showQuestioner, setShowQuestioner] = useState(false);
  const [expandedTopics, setExpandedTopics] = useState({});
  const [newCode, setNewCode] = useState('');
  const [loadingProgress, setLoadingProgress] = useState(0);
  const [sidebarVisible, setSidebarVisible] = useState(true);
  const [showProfileDropdown, setShowProfileDropdown] = useState(false);
  const [uploadedFile, setUploadedFile] = useState(null);
  const [uploadProgress, setUploadProgress] = useState(0);

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
      setError(null);
      setSelectedCodes({ accepted: [], denied: [] });
      setExpandedTopics({});
      setNewCode('');
    };

    window.addEventListener('newAnalysis', resetForm);
    
    return () => {
      window.removeEventListener('newAnalysis', resetForm);
    };
  }, []);

  // Transform CDT_subtopic array into the object format needed by the component
  const formattedSubtopicData = useMemo(() => {
    if (!result?.CDT_subtopic) {
      return {};
    }
    
    console.log("Raw CDT_subtopic data:", result.CDT_subtopic);
    const formatted = {};
    
    result.CDT_subtopic.forEach(topic => {
      // Use a combination of topic name and code range as the key if possible
      const key = `${topic.topic || 'Unknown'} (${topic.code_range || 'N/A'})`;
      const allCodes = [];
      
      // First try to extract specific codes from subtopics_data
      if (topic.raw_result && topic.raw_result.subtopics_data && Array.isArray(topic.raw_result.subtopics_data)) {
        topic.raw_result.subtopics_data.forEach(subtopic => {
          // The raw_result can be an array or an object with raw_result property
          let rawResultsToProcess = [];
          
          if (Array.isArray(subtopic.raw_result)) {
            // Direct array of results
            rawResultsToProcess = subtopic.raw_result;
          } else if (typeof subtopic.raw_result === 'object' && subtopic.raw_result !== null) {
            // Get any specific entries that might contain codes
            rawResultsToProcess = [subtopic.raw_result];
          }
            
          rawResultsToProcess.forEach(codeEntry => {
            // Check if this is a direct entry with specific_codes
            if (codeEntry && Array.isArray(codeEntry.specific_codes) && codeEntry.specific_codes.length > 0) {
              codeEntry.specific_codes.forEach(code => {
                if (code) {
                  allCodes.push({
                    code: code,
                    explanation: codeEntry.explanation || 'No explanation provided',
                    doubt: codeEntry.doubt || 'None'
                  });
                }
              });
            }
          });
        });
      }
      
      // If we found specific codes, use them
      if (allCodes.length > 0) {
        console.log(`Found ${allCodes.length} specific codes for ${key}`);
        formatted[key] = allCodes;
      }
      // Fall back to the original codes array if present and no specific codes found
      else if (Array.isArray(topic.codes) && topic.codes.length > 0) {
        console.log(`Using fallback codes for ${key}: ${topic.codes.length} codes`);
        formatted[key] = topic.codes;
      }
    });
    
    console.log("Final formatted subtopic data:", formatted);
    return formatted;
  }, [result?.CDT_subtopic]);

  // Add a formatted ICD topic data state (after the formattedSubtopicData useMemo)
  const formattedICDTopicData = useMemo(() => {
    if (!result?.ICD_topic_result) {
      return null;
    }
    
    const icdTopicResult = result.ICD_topic_result;
    
    // Create a topic key similar to CDT topics format
    const categoryNumber = icdTopicResult.code_range || "N/A";
    const topicKey = `${icdTopicResult.topic || 'Unknown'} (${categoryNumber})`;
    
    // Format the ICD topic data to have a similar structure to CDT topics
    let formattedICDData = {};
    
    // Access data from raw_result if it exists, otherwise check direct properties
    const rawResult = icdTopicResult.raw_result || {};
    const code = rawResult.code || icdTopicResult.code;
    const explanation = rawResult.explanation || icdTopicResult.explanation || 'No explanation provided';
    const doubt = rawResult.doubt || icdTopicResult.doubt || 'None';
    const rawData = rawResult.raw_data || rawResult.raw_result || '';
    
    // Create a codes array with a single entry if the code exists
    if (code) {
      formattedICDData[topicKey] = [{
        code: code,
        explanation: explanation,
        doubt: doubt,
        raw_data: rawData
      }];
    } else {
      // Still create an entry for "No applicable code" but with clear indication
      formattedICDData[topicKey] = [{
        code: 'none', // explicitly set to 'none' to match topic service response
        explanation: explanation,
        doubt: doubt,
        raw_data: rawData
      }];
    }
    
    return formattedICDData;
  }, [result?.ICD_topic_result]);

  // Initialize expanded topics state based on the formatted data
  useEffect(() => {
    const initialExpandedState = {};
    
    // Handle CDT subtopics
    if (formattedSubtopicData && Object.keys(formattedSubtopicData).length > 0) {
      console.log("Formatted Subtopics data:", formattedSubtopicData);
      Object.keys(formattedSubtopicData).forEach(topicKey => {
        initialExpandedState[topicKey] = false;
      });
    }
    
    // Also handle ICD topic
    if (formattedICDTopicData && Object.keys(formattedICDTopicData).length > 0) {
      console.log("Formatted ICD Topic data:", formattedICDTopicData);
      Object.keys(formattedICDTopicData).forEach(topicKey => {
        initialExpandedState[topicKey] = false; // Default to collapsed
      });
    }
    
    if (Object.keys(initialExpandedState).length > 0) {
      setExpandedTopics(initialExpandedState);
    } else {
      setExpandedTopics({}); // Reset if no data
    }
  }, [formattedSubtopicData, formattedICDTopicData]); // Add dependency on ICD data

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);
    setSelectedCodes({ accepted: [], denied: [] });

    try {
      const response = await analyzeDentalScenario({ scenario });
      console.log('Analysis results received:', response);
      console.log('Record ID:', response?.record_id);
      setResult(response);
    } catch (err) {
      console.error('Error analyzing scenario:', err);
      setError(err.message || 'An error occurred while analyzing the scenario');
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
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

  const handleSubmitCodes = async () => {
    setSubmitting(true);
    try {
      await submitSelectedCodes(selectedCodes, result.record_id);
      // Reset form after successful submission
      setScenario('');
      setResult(null);
      setSelectedCodes({ accepted: [], denied: [] });
    } catch (err) {
      setError(err.message || 'Failed to submit selected codes');
    } finally {
      setSubmitting(false);
    }
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
      const errorMsg = Array.isArray(response)
        ? response.find(r => r.response && r.response.status === 'error')?.response?.message || 'An error occurred in batch processing.'
        : response?.message || 'Failed to process answers';
      setError(errorMsg);
      // Don't hide the questioner modal on error
    }
  };

  const toggleTopic = (topicKey) => {
    console.log(`Toggling topic: ${topicKey}, current state:`, expandedTopics[topicKey]);
    setExpandedTopics(prev => {
      const newState = { ...prev };
      newState[topicKey] = !prev[topicKey];
      console.log(`New expanded state for ${topicKey}:`, newState[topicKey]);
      return newState;
    });
  };

  const handleCopyCodes = () => {
    if (!result?.inspector_results) return;
    
    // Get the actual inspector results object (already direct)
    const inspectorData = result.inspector_results;
    
    const cdtCodes = inspectorData.cdt?.codes || [];
    const icdCodes = inspectorData.icd?.codes || [];
    
    let textToCopy = `CDT Codes: ${cdtCodes.join(', ')}\nICD Codes: ${icdCodes.join(', ')}`;
    
    navigator.clipboard.writeText(textToCopy).then(() => {
      alert('Codes copied to clipboard!');
    }).catch(err => {
      console.error('Failed to copy codes: ', err);
    });
  };

  const scrollToCode = (code) => {
    // Find the topic containing the code using formattedSubtopicData
    let foundTopicKey = null;
    let codeIndex = -1;
    
    console.log("Looking for code:", code);
    console.log("Available topics:", Object.keys(formattedSubtopicData));
    
    // Search through the formatted data
    if (formattedSubtopicData) {
      Object.keys(formattedSubtopicData).forEach(topicKey => {
        const topicCodes = formattedSubtopicData[topicKey];
        if (topicCodes && Array.isArray(topicCodes)) {
          topicCodes.forEach((codeData, index) => {
            // Check both direct code equality and specific_codes arrays
            const codeMatch = 
              (codeData && codeData.code === code) || 
              (codeData && Array.isArray(codeData.specific_codes) && codeData.specific_codes.includes(code));
              
            if (codeMatch) {
              console.log(`Found code ${code} in topic ${topicKey}`);
              foundTopicKey = topicKey;
              codeIndex = index;
            }
          });
        }
      });
    }

    if (foundTopicKey) {
      console.log(`Found code ${code} in topic ${foundTopicKey} at index ${codeIndex}`);
      
      // Expand the topic if it's not already expanded
      if (!expandedTopics[foundTopicKey]) {
        setExpandedTopics(prev => ({
          ...prev,
          [foundTopicKey]: true
        }));
      }

      // Wait a short time for the expansion animation to complete before scrolling
      setTimeout(() => {
        // Scroll to the code
        const element = document.getElementById(`code-${code}`);
        if (element) {
          element.scrollIntoView({ behavior: 'smooth', block: 'center' });
          // Add a brief highlight effect
          element.classList.add('bg-yellow-100');
          setTimeout(() => {
            element.classList.remove('bg-red-100');
          }, 1500);
        } else {
          console.log(`Could not find element with ID code-${code}`);
        }
      }, 300);
    } else {
      console.log(`Could not find topic containing code ${code}`);
    }
  };

  const renderInspectorResults = () => {
    if (!result?.inspector_results) return null;

    const inspectorData = result.inspector_results;
    const cdtCodes = inspectorData.cdt?.codes || [];
    const icdCodes = inspectorData.icd?.codes || [];

    return (
      <div className={`mt-8 p-4 ${isDark ? 'bg-blue-900/30 border-blue-700' : 'bg-blue-50 border-blue-200'} rounded-lg border ai-final-analysis-content relative`}>
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center">
            <FaRobot className={`${isDark ? 'text-blue-400' : 'text-blue-500'} mr-2`} />
            <h3 className={`text-sm font-semibold ${isDark ? 'text-blue-400' : 'text-blue-700'}`}>AI Final Analysis</h3>
          </div>
          <button
            onClick={handleCopyCodes}
            className={`${isDark ? 'text-blue-400 hover:text-blue-300' : 'text-blue-500 hover:text-blue-700'} transition-colors`}
          >
            <FaCopy className="inline mr-1" /> Copy Codes
          </button>
        </div>
        
        <div className="mb-4">
          <h4 className={`font-medium ${isDark ? 'text-gray-200' : 'text-gray-700'} mb-2 text-sm`}>CDT Codes:</h4>
          <div className="flex flex-wrap gap-2">
            {cdtCodes.map((code, index) => {
              const isAccepted = selectedCodes.accepted.includes(code);
              const isDenied = selectedCodes.denied.includes(code);
              
              return (
                <span 
                  key={`${code}-${index}`}
                  onClick={() => scrollToCode(code)}
                  className={`cursor-pointer px-2 py-1 rounded-full text-xs transition-all duration-200 ${
                    isAccepted 
                      ? (isDark ? 'bg-green-900/60 text-green-200 border-green-700' : 'bg-green-100 text-green-800 border border-green-300') 
                      : isDenied 
                        ? (isDark ? 'bg-red-900/60 text-red-200 border-red-700' : 'bg-red-100 text-red-800 border border-red-300')
                        : (isDark ? 'bg-blue-800/60 text-blue-200' : 'bg-blue-100 text-blue-800')
                  }`}
                >
                  {code}
                </span>
              );
            })}
          </div>
          <p className={`text-xs ${isDark ? 'text-gray-300' : 'text-gray-600'} mt-2`}>{inspectorData.cdt?.explanation}</p>
        </div>

        <div className="mb-4">
          <h4 className={`font-medium ${isDark ? 'text-gray-200' : 'text-gray-700'} mb-2 text-sm`}>ICD Codes:</h4>
          <div className="flex flex-wrap gap-2">
            {icdCodes.map((code, index) => (
              <span 
                key={`icd-code-${index}-${code}`}
                className={`px-2 py-1 rounded-full text-xs ${
                  isDark ? 'bg-purple-900/60 text-purple-200' : 'bg-purple-100 text-purple-800'
                }`}
              >
                {code}
              </span>
            ))}
          </div>
          <p className={`text-xs ${isDark ? 'text-gray-300' : 'text-gray-600'} mt-2`}>{inspectorData.icd?.explanation}</p>
        </div>
      </div>
    );
  };

  // Add a function to render the selected codes section
  const renderSelectedCodes = () => {
    if (selectedCodes.accepted.length === 0) return null;
    
    const handleCopySelectedCodes = (type = 'all') => {
      const cdtCodes = result?.inspector_results?.cdt?.codes || [];
      const icdCodes = result?.inspector_results?.icd?.codes || [];
      
      let textToCopy = '';
      
      if (type === 'cdt') {
        const selectedCDT = selectedCodes.accepted.filter(code => cdtCodes.includes(code));
        textToCopy = selectedCDT.join(', ');
      } else if (type === 'icd') {
        const selectedICD = selectedCodes.accepted.filter(code => icdCodes.includes(code));
        textToCopy = selectedICD.join(', ');
      } else {
        const selectedCDT = selectedCodes.accepted.filter(code => cdtCodes.includes(code));
        const selectedICD = selectedCodes.accepted.filter(code => icdCodes.includes(code));
        textToCopy = `CDT Codes: ${selectedCDT.join(', ')}\nICD Codes: ${selectedICD.join(', ')}`;
      }
      
      navigator.clipboard.writeText(textToCopy).then(() => {
        alert('Selected codes copied to clipboard!');
      }).catch(err => {
        console.error('Failed to copy codes: ', err);
      });
    };
    
    return (
      <div className={`mt-8 p-4 ${isDark ? 'bg-gray-800 border-gray-700' : 'bg-gray-50 border-gray-200'} rounded-lg border`}>
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold">Your Selections</h3>
          <button
            onClick={() => handleCopySelectedCodes()}
            className={`${isDark ? 'text-blue-400 hover:text-blue-300' : 'text-blue-500 hover:text-blue-700'} transition-colors flex items-center`}
          >
            <FaCopy className="mr-1" /> Copy All
          </button>
        </div>
        
        {selectedCodes.accepted.length > 0 && (
          <div>
            <h4 className={`font-medium ${isDark ? 'text-green-400' : 'text-green-700'} mb-2`}>Accepted Codes:</h4>
            <div className="flex flex-wrap gap-2">
              {selectedCodes.accepted.map((code, index) => (
                <span 
                  key={`accepted-${index}-${code}`}
                  className={`px-3 py-1 rounded-full text-sm ${
                    isDark ? 'bg-green-900/60 text-green-200 border border-green-700' : 'bg-green-100 text-green-800 border border-green-300'
                  }`}
                >
                  {code}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    );
  };

  const handleAddCustomCode = async () => {
    if (!newCode.trim()) {
      setError("Please enter a valid code");
      return;
    }

    const codeType = document.getElementById('codeType').value; // Get the selected code type
    const codes = result?.inspector_results?.[codeType.toLowerCase()]?.codes || [];
    
    if (codes.includes(newCode)) {
      setError("This code already exists");
      return;
    }

    try {
      // Update the inspector results with the new code
      const updatedResult = { ...result };
      updatedResult.inspector_results[codeType.toLowerCase()].codes.push(newCode);
      setResult(updatedResult);
      setNewCode('');
      
      // Automatically select the new code
      handleCodeSelection(newCode, 'accept');
    } catch (err) {
      setError(err.message || 'Failed to add custom code');
    }
  };

  // Add a function to render the ICD topic section
  const renderICDCodeSection = (topicKey) => {
    if (!formattedICDTopicData?.[topicKey]) return null;
    
    const topicData = formattedICDTopicData[topicKey];
    const isExpanded = expandedTopics[topicKey];
    
    // Extract name from the key (assuming format "Name (Range)")
    const topicName = topicKey.split('(')[0].trim();
    
    return (
      <div className="mb-6">
        <div 
          className={`flex items-center justify-between p-4 ${
            isDark ? 'bg-purple-900/30' : 'bg-purple-50'
          } rounded-lg cursor-pointer hover:${isDark ? 'bg-purple-800/30' : 'bg-purple-100'} transition-colors`}
          onClick={() => toggleTopic(topicKey)}
        >
          <h3 className="text-lg font-semibold">ICD-10: {topicName}</h3>
          <div className="transform transition-transform duration-300">
            {isExpanded ? '▼' : '▶'}
          </div>
        </div>
        
        <div className={`overflow-hidden transition-all duration-300 ease-in-out ${
          isExpanded ? 'max-h-[2000px] opacity-100' : 'max-h-0 opacity-0'
        }`}>
          {topicData.map((codeData, index) => {
            // For ICD data, we also show entries with code 'none' to display explanations
            // about why no code was applicable
            const isNoCode = !codeData.code || codeData.code === 'none' || codeData.code.toLowerCase() === 'none';
            
            return (
              <div 
                key={`icd-topic-${index}-${topicKey}`}
                className={`mt-4 transition-all duration-300 ease-in-out ${
                  isDark ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'
                }`}
              >
                <div 
                  className="p-4 rounded-lg shadow-sm border transition-colors duration-300"
                >
                  <div className="flex justify-between items-center mb-2">
                    <span className={`font-mono px-2 py-1 rounded ${
                      isNoCode 
                        ? (isDark ? 'bg-gray-700 text-gray-300' : 'bg-gray-100 text-gray-600') 
                        : (isDark ? 'bg-purple-900 text-purple-200' : 'bg-purple-100 text-purple-800')
                    }`}>
                      {isNoCode ? 'No applicable ICD-10 code' : codeData.code}
                    </span>
                  </div>
                  <p className={`text-sm mb-1 ${isDark ? 'text-gray-300' : 'text-gray-600'}`}>
                    <span className="font-medium">Explanation:</span> {codeData.explanation || 'N/A'}
                  </p>
                  <p className={`text-sm ${isDark ? 'text-gray-300' : 'text-gray-600'}`}>
                    <span className="font-medium">Doubt:</span> {codeData.doubt || 'N/A'}
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    );
  };

  const handleFileUpload = (file) => {
    setUploadedFile(file);
    let progress = 0;
    const interval = setInterval(() => {
      progress += 10;
      setUploadProgress(progress);
      if (progress >= 100) {
        clearInterval(interval);
        setUploadProgress(0);
        handleSubmit(new Event('submit')); // Simulate form submission
      }
    }, 200);
  };

  return (
    <div className="flex min-h-screen">
      {/* Sidebar - removed fixed positioning */}
      <div className={`w-64 ${isDark ? 'bg-slate-700' : 'bg-blue-100'} text-gray-800 dark:text-gray-200 transition-transform duration-300 ${
        sidebarVisible ? '' : 'hidden'
      }`}>
        <div className="sticky top-0 h-screen overflow-y-auto">
          <div className="flex flex-col h-full">
            <div className="flex items-center justify-between p-4">
              <h1 className="text-2xl font-bold tracking-tight">RCM Pro</h1>
              <button onClick={() => setSidebarVisible(false)} className="text-gray-800 dark:text-gray-200">
                <FaTimes />
              </button>
            </div>
            <nav className="flex-1 p-4">
              <ul className="space-y-4">
                <li>
                  <a href="#" className="flex items-center p-2 rounded hover:bg-blue-200 dark:hover:bg-slate-600 font-medium leading-relaxed">
                    <FaHome className="mr-2" /> Dashboard
                  </a>
                </li>
                <li>
                  <a href="#" className="flex items-center p-2 rounded hover:bg-blue-200 dark:hover:bg-slate-600 font-medium leading-relaxed">
                    <FaUserInjured className="mr-2" /> Patients
                  </a>
                </li>
                <li>
                  <a href="#" className="flex items-center p-2 rounded hover:bg-blue-200 dark:hover:bg-slate-600 font-medium leading-relaxed">
                    <FaFileAlt className="mr-2" /> Coding
                  </a>
                </li>
                <li>
                  <a href="#" className="flex items-center p-2 rounded hover:bg-blue-200 dark:hover:bg-slate-600 font-medium leading-relaxed">
                    <FaDollarSign className="mr-2" /> Billing
                  </a>
                </li>
              </ul>
            </nav>
            <div className="p-4 mt-auto">
              <button 
                onClick={toggleTheme}
                className="flex items-center p-2 rounded hover:bg-blue-200 dark:hover:bg-slate-600 font-medium leading-relaxed w-full"
              >
                {isDark ? <FaSun className="mr-2" /> : <FaMoon className="mr-2" />}
                {isDark ? 'Light Mode' : 'Dark Mode'}
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content - adjusted margin */}
      <div className="flex-1">
        {/* Header */}
        <header className="sticky top-0 bg-white dark:bg-slate-800 z-10 flex justify-between items-center p-4 shadow-md">
          <div className="flex items-center space-x-4">
            <button onClick={() => setSidebarVisible(!sidebarVisible)} className="text-gray-800 dark:text-gray-200">
              <FaBars className="text-xl" />
            </button>
            <h2 className="text-xl font-bold tracking-tight text-gray-800 dark:text-gray-200">Medical Coding Suite</h2>
          </div>
        </header>

        {/* Main Grid - added padding */}
        <div className="p-4 md:p-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Input Section */}
            <div className={`${isDark ? 'bg-slate-600' : 'bg-gray-200'} p-6 rounded-xl shadow-lg col-span-1 md:col-span-2`}>
              <h3 className="text-lg font-bold tracking-tight mb-4 text-gray-800 dark:text-gray-200">Input Clinical Notes</h3>
              <div className="mb-4">
                <label className={`block ${isDark ? 'text-gray-300' : 'text-gray-700'} mb-2 text-sm font-medium`}>Raw Text Input</label>
                <textarea
                  value={scenario}
                  onChange={(e) => setScenario(e.target.value)}
                  className={`w-full border rounded-lg p-3 ${
                    isDark ? 'bg-slate-700 text-gray-200 border-slate-500' : 'bg-gray-100 text-gray-900 border-gray-300'
                  } focus:ring-2 focus:ring-blue-400 text-sm font-light leading-relaxed`}
                  rows="5"
                  placeholder="Enter clinical notes (e.g., Patient has tooth decay in molar, requires filling)"
                />
              </div>
              <div className="mb-4">
                <label className={`block ${isDark ? 'text-gray-300' : 'text-gray-700'} mb-2 text-sm font-medium`}>Upload PDF</label>
                <div 
                  className={`border-2 border-dashed ${
                    isDark ? 'border-slate-500' : 'border-gray-300'
                  } p-6 rounded-lg text-center hover:border-blue-400 transition-colors`}
                  onDragOver={(e) => e.preventDefault()}
                  onDrop={(e) => {
                    e.preventDefault();
                    const file = e.dataTransfer.files[0];
                    if (file && file.type === 'application/pdf') {
                      handleFileUpload(file);
                    }
                  }}
                >
                  <input
                    type="file"
                    accept=".pdf"
                    className="hidden"
                    onChange={(e) => {
                      const file = e.target.files?.[0];
                      if (file) handleFileUpload(file);
                    }}
                  />
                  <p className={`${isDark ? 'text-gray-400' : 'text-gray-500'} text-sm font-light leading-relaxed`}>
                    Drag and drop a PDF or <span className="text-blue-400 cursor-pointer hover:underline">browse</span>
                  </p>
                  {uploadedFile && (
                    <p className={`${isDark ? 'text-gray-400' : 'text-gray-500'} mt-2 text-sm font-light`}>
                      {uploadedFile.name}
                    </p>
                  )}
                  {uploadProgress > 0 && uploadProgress < 100 && (
                    <div className="w-full bg-gray-300 dark:bg-slate-500 rounded-full h-2 mt-2">
                      <div
                        className="bg-blue-400 h-2 rounded-full"
                        style={{ width: `${uploadProgress}%` }}
                      />
                    </div>
                  )}
                </div>
              </div>
              <button
                onClick={handleSubmit}
                disabled={loading}
                className={`${
                  isDark ? 'bg-gradient-to-r from-teal-400 to-teal-500' : 'bg-gradient-to-r from-blue-400 to-blue-500'
                } text-white px-4 py-2 text-sm rounded-lg hover:scale-105 hover:shadow-lg focus:ring-2 focus:ring-blue-400 font-medium transition-all duration-200`}
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

            {/* Final Codes Section */}
            <div className={`${isDark ? 'bg-slate-600' : 'bg-gray-200'} p-6 rounded-xl shadow-lg hover:shadow-xl transition-all duration-200`}>
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-lg font-bold tracking-tight text-gray-800 dark:text-gray-200">Final Codes</h3>
                <button
                  onClick={() => handleCopySelectedCodes()}
                  className={`${
                    isDark ? 'bg-gradient-to-r from-teal-400 to-teal-500' : 'bg-gradient-to-r from-blue-400 to-blue-500'
                  } text-white px-3 py-1 text-sm rounded-lg hover:scale-105 hover:shadow-lg focus:ring-2 focus:ring-blue-400 flex items-center font-medium`}
                >
                  <FaCopy className="mr-2" /> Copy Selected
                </button>
              </div>

              {/* Custom Code Input Form */}
              <div className="mb-4">
                <h4 className={`text-sm font-semibold ${isDark ? 'text-gray-300' : 'text-gray-700'} mb-2`}>Add Custom Code</h4>
                <div className="flex flex-col sm:flex-row gap-2">
                  <input
                    type="text"
                    value={newCode}
                    onChange={(e) => setNewCode(e.target.value)}
                    className={`flex-1 border rounded-lg p-2 text-sm ${
                      isDark ? 'bg-slate-700 text-gray-200 border-slate-500' : 'bg-gray-100 text-gray-900 border-gray-300'
                    } focus:ring-2 focus:ring-blue-400 font-light leading-relaxed`}
                    placeholder="Enter code (e.g., D0120)"
                  />
                  <select
                    id="codeType"
                    className={`border rounded-lg p-2 text-sm ${
                      isDark ? 'bg-slate-700 text-gray-200 border-slate-500' : 'bg-gray-100 text-gray-900 border-gray-300'
                    } focus:ring-2 focus:ring-blue-400 font-light leading-relaxed`}
                  >
                    <option value="CDT">CDT</option>
                    <option value="ICD">ICD-10</option>
                  </select>
                  <button
                    onClick={handleAddCustomCode}
                    className={`${
                      isDark ? 'bg-gradient-to-r from-teal-400 to-teal-500' : 'bg-gradient-to-r from-blue-400 to-blue-500'
                    } text-white px-3 py-1 text-sm rounded-lg hover:scale-105 hover:shadow-lg focus:ring-2 focus:ring-blue-400 font-medium`}
                  >
                    Add
                  </button>
                </div>
              </div>

              {/* Code Output */}
              <div className="space-y-4">
                {/* CDT Codes */}
                <div className={`border ${
                  isDark ? 'border-slate-500 bg-slate-700' : 'border-gray-300 bg-gray-100'
                } p-4 rounded-lg shadow-md`}>
                  <div className="flex justify-between items-center mb-2">
                    <h4 className={`text-lg font-semibold ${isDark ? 'text-gray-300' : 'text-gray-700'}`}>CDT Codes</h4>
                    <button
                      onClick={() => handleCopySelectedCodes('cdt')}
                      className={`${isDark ? 'text-gray-400 hover:text-blue-400' : 'text-gray-500 hover:text-blue-400'} hover:scale-105 transition-all duration-200`}
                    >
                      <FaCopy />
                    </button>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {result?.inspector_results?.cdt?.codes.map((code, index) => (
                      <span
                        key={`${code}-${index}`}
                        onClick={() => handleCodeSelection(code, selectedCodes.accepted.includes(code) ? 'deny' : 'accept')}
                        className={`cursor-pointer px-2 py-1 rounded-full text-xs transition-all duration-200 hover:scale-105 ${
                          selectedCodes.accepted.includes(code)
                            ? (isDark ? 'bg-green-900/60 text-green-200 border-green-700' : 'bg-green-100 text-green-800 border border-green-300')
                            : selectedCodes.denied.includes(code)
                            ? (isDark ? 'bg-red-900/60 text-red-200 border-red-700' : 'bg-red-100 text-red-800 border border-red-300')
                            : (isDark ? 'bg-blue-800/60 text-blue-200' : 'bg-blue-100 text-blue-800')
                        } hover:shadow-lg`}
                      >
                        {code}
                      </span>
                    ))}
                  </div>
                </div>

                {/* ICD Codes */}
                <div className={`border ${
                  isDark ? 'border-slate-500 bg-slate-700' : 'border-gray-300 bg-gray-100'
                } p-4 rounded-lg shadow-md`}>
                  <div className="flex justify-between items-center mb-2">
                    <h4 className={`text-lg font-semibold ${isDark ? 'text-gray-300' : 'text-gray-700'}`}>ICD-10 Codes</h4>
                    <button
                      onClick={() => handleCopySelectedCodes('icd')}
                      className={`${isDark ? 'text-gray-400 hover:text-blue-400' : 'text-gray-500 hover:text-blue-400'} hover:scale-105 transition-all duration-200`}
                    >
                      <FaCopy />
                    </button>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {result?.inspector_results?.icd?.codes.map((code, index) => (
                      <span
                        key={`icd-code-${index}-${code}`}
                        onClick={() => handleCodeSelection(code, selectedCodes.accepted.includes(code) ? 'deny' : 'accept')}
                        className={`cursor-pointer px-2 py-1 rounded-full text-xs transition-all duration-200 hover:scale-105 ${
                          selectedCodes.accepted.includes(code)
                            ? (isDark ? 'bg-green-900/60 text-green-200 border-green-700' : 'bg-green-100 text-green-800 border border-green-300')
                            : selectedCodes.denied.includes(code)
                            ? (isDark ? 'bg-red-900/60 text-red-200 border-red-700' : 'bg-red-100 text-red-800 border border-red-300')
                            : (isDark ? 'bg-purple-900/60 text-purple-200' : 'bg-purple-100 text-purple-800')
                        } hover:shadow-lg`}
                      >
                        {code}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* Code Details Section */}
            <div className={`${isDark ? 'bg-slate-600' : 'bg-gray-200'} p-6 rounded-xl shadow-lg hover:shadow-xl transition-all duration-200 col-span-1 md:col-span-3`}>
              <h3 className="text-lg font-bold tracking-tight mb-4 text-gray-800 dark:text-gray-200">Code Details</h3>
              <div className={`border ${
                isDark ? 'border-slate-500 bg-slate-700' : 'border-gray-300 bg-gray-100'
              } p-4 rounded-lg shadow-md font-bold leading-relaxed text-gray-800 dark:text-gray-200`}>
                Click a code above to view details...
              </div>
            </div>

            {/* Recent Codes Dashboard */}
            <div className={`${isDark ? 'bg-slate-600' : 'bg-gray-200'} p-6 rounded-xl shadow-lg col-span-1 md:col-span-3`}>
              <h3 className="text-lg font-bold tracking-tight mb-4 text-gray-800 dark:text-green-200">Final Code Generation History</h3>
              <div className="overflow-x-auto">
                <table className="w-full text-left">
                  <thead>
                    <tr className={`${isDark ? 'text-gray-400' : 'text-gray-600'} font-medium`}>
                      <th className="p-2">Code</th>
                      <th className="p-2">Type</th>
                      <th className="p-2">Description</th>
                      <th className="p-2">Actions</th>
                    </tr>
                  </thead>
                  <tbody className={`font-bold ${isDark ? 'text-gray-200' : 'text-gray-800'} leading-relaxed`}>
                    {result?.inspector_results?.cdt?.codes.map((code) => (
                      <tr key={code} className={`border-t ${isDark ? 'border-slate-500' : 'border-gray-300'}`}>
                        <td className="p-2">{code}</td>
                        <td className="p-2">CDT</td>
                        <td className="p-2">{/* Add description from your data */}</td>
                        <td className="p-2">
                          <button className={`text-blue-400 hover:text-blue-500 font-medium`} onClick={() => scrollToCode(code)}>
                            View
                          </button>
                          <button className="text-green-400 hover:text-green-500 ml-2 font-medium">
                            Add to Claim
                          </button>
                        </td>
                      </tr>
                    ))}
                    {result?.inspector_results?.icd?.codes.map((code) => (
                      <tr key={code} className={`border-t ${isDark ? 'border-slate-500' : 'border-gray-300'}`}>
                        <td className="p-2">{code}</td>
                        <td className="p-2">ICD-10</td>
                        <td className="p-2">{/* Add description from your data */}</td>
                        <td className="p-2">
                          <button className={`text-blue-400 hover:text-blue-500 font-medium`}>View</button>
                          <button className="text-green-400 hover:text-green-500 ml-2 font-medium">
                            Add to Claim
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
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