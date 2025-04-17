import { useState } from "react";
import { submitQuestionAnswers } from "../../interceptors/services";
import { useTheme } from '../../context/ThemeContext';
import PropTypes from 'prop-types';

const Questioner = ({ isVisible, onClose, questions, onSubmitSuccess, scenarios }) => {
  const { isDark } = useTheme();
  const [answers, setAnswers] = useState({
    cdt: {},
    icd: {}
  });
  const [loading, setLoading] = useState(false);
  const [currentSection, setCurrentSection] = useState('cdt');
  const [error, setError] = useState(null);
  const [expandedScenarios, setExpandedScenarios] = useState({});

  // Ensure questions arrays exist and handle any potential undefined IDs
  const cdtQuestionsArray = Array.isArray(questions.cdt_questions) ? questions.cdt_questions : [];
  const icdQuestionsArray = Array.isArray(questions.icd_questions) ? questions.icd_questions : [];

  // Filter out questions with "none" as the id, and ensure id exists before checking
  const filteredCdtQuestions = cdtQuestionsArray.filter(q => q && q.id && q.id !== "none" && typeof q.id === 'string' && q.id.toLowerCase() !== "none");
  const filteredIcdQuestions = icdQuestionsArray.filter(q => q && q.id && q.id !== "none" && typeof q.id === 'string' && q.id.toLowerCase() !== "none");

  // Group questions by scenario
  const groupQuestionsByScenario = (questionsArray) => {
    const grouped = {};
    
    questionsArray.forEach(q => {
      const scenarioId = q.scenarioId;
      if (!grouped[scenarioId]) {
        grouped[scenarioId] = [];
      }
      grouped[scenarioId].push(q);
    });
    
    return grouped;
  };
  
  const cdtQuestionsGrouped = groupQuestionsByScenario(filteredCdtQuestions);
  const icdQuestionsGrouped = groupQuestionsByScenario(filteredIcdQuestions);

  const handleAnswerChange = (section, questionId, value) => {
    setAnswers(prev => ({
      ...prev,
      [section]: {
        ...prev[section],
        [questionId]: value
      }
    }));
  };

  const toggleScenarioExpand = (scenarioId) => {
    setExpandedScenarios(prev => ({
      ...prev,
      [scenarioId]: !prev[scenarioId]
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    
    try {
      // Group answers by record ID
      const answersByRecordId = {};
      
      // Process CDT answers
      Object.entries(answers.cdt).forEach(([questionId, value]) => {
        // Find the corresponding question to get its recordId
        const question = filteredCdtQuestions.find(q => q.id === questionId);
        if (question && question.recordId) {
          if (!answersByRecordId[question.recordId]) {
            answersByRecordId[question.recordId] = {
              cdt_answers: [],
              icd_answers: []
            };
          }
          
          answersByRecordId[question.recordId].cdt_answers.push({
            id: questionId,
            answer: value
          });
        }
      });
      
      // Process ICD answers
      Object.entries(answers.icd).forEach(([questionId, value]) => {
        // Find the corresponding question to get its recordId
        const question = filteredIcdQuestions.find(q => q.id === questionId);
        if (question && question.recordId) {
          if (!answersByRecordId[question.recordId]) {
            answersByRecordId[question.recordId] = {
              cdt_answers: [],
              icd_answers: []
            };
          }
          
          answersByRecordId[question.recordId].icd_answers.push({
            id: questionId,
            answer: value
          });
        }
      });
      
      // Submit answers for each record ID and collect responses
      const submitPromises = Object.entries(answersByRecordId).map(async ([recordId, payload]) => {
        const response = await submitQuestionAnswers(payload, recordId);
        // Add recordId to response for identification
        if (response) {
          response.recordId = recordId;
        }
        return response;
      });
      
      const responses = await Promise.all(submitPromises);
      onSubmitSuccess(responses);
      
      // If all successful, close the modal
      if (responses.every(r => r && r.status === 'success')) {
        onClose();
      }
    } catch (err) {
      setError(err.message || 'Failed to submit answers');
      console.error("Error submitting answers:", err);
    } finally {
      setLoading(false);
    }
  };

  const isFormComplete = () => {
    // For each scenario, check if all questions have been answered
    const allQuestionsAnswered = () => {
      let complete = true;
      
      // Check CDT questions using the filtered array
      if (filteredCdtQuestions.length === 0 && filteredIcdQuestions.length === 0) {
        return false; // No questions to answer
      }

      filteredCdtQuestions.forEach(q => {
        if (!answers.cdt[q.id] || answers.cdt[q.id].trim() === '') {
          complete = false;
        }
      });
      
      // Check ICD questions using the filtered array
      filteredIcdQuestions.forEach(q => {
        if (!answers.icd[q.id] || answers.icd[q.id].trim() === '') {
          complete = false;
        }
      });
      
      return complete;
    };
    
    return allQuestionsAnswered();
  };

  const switchSection = () => {
    setCurrentSection(prev => prev === 'cdt' ? 'icd' : 'cdt');
  };

  const getScenarioText = (scenarioId) => {
    const scenario = scenarios.find(s => s.questionId === scenarioId);
    return scenario ? scenario.text : "Unknown scenario";
  };

  // If not visible, don't render
  if (!isVisible) return null;

  // If there are no questions, don't render
  if (filteredCdtQuestions.length === 0 && filteredIcdQuestions.length === 0) return null;

  return (
    <div className="fixed inset-0 flex items-center justify-center z-50">
      {/* Backdrop */}
      <div 
        className="absolute inset-0 bg-black bg-opacity-50" 
        onClick={onClose}
      ></div>
      
      {/* Modal Content */}
      <div 
        className={`relative w-full max-w-2xl mx-auto p-6 rounded-lg shadow-xl ${
          isDark ? 'bg-gray-800 text-gray-100' : 'bg-white text-gray-800'
        } max-h-[90vh] overflow-y-auto`}
        onClick={e => e.stopPropagation()}
      >
        {/* Close Button */}
        <button 
          onClick={onClose}
          className={`absolute top-2 right-2 w-8 h-8 rounded-full flex items-center justify-center ${
            isDark ? 'bg-gray-700 text-gray-300 hover:bg-gray-600' : 'bg-gray-200 text-gray-600 hover:bg-gray-300'
          }`}
        >
          &times;
        </button>
        
        {/* Title */}
        <h2 className={`text-xl font-semibold mb-4 ${isDark ? 'text-blue-300' : 'text-blue-600'}`}>
          Answer All Questions
        </h2>
        
        <p className={`text-sm mb-4 ${isDark ? 'text-gray-300' : 'text-gray-600'}`}>
          Please answer all questions below for each scenario to continue processing.
        </p>
        
        {/* Tab Navigation */}
        {filteredCdtQuestions.length > 0 && filteredIcdQuestions.length > 0 && (
          <div className="flex border-b mb-4">
            <button
              onClick={() => setCurrentSection('cdt')}
              className={`px-4 py-2 mr-2 ${
                currentSection === 'cdt' 
                  ? (isDark ? 'border-blue-500 text-blue-400' : 'border-blue-500 text-blue-700') 
                  : (isDark ? 'text-gray-400' : 'text-gray-500')
              } ${currentSection === 'cdt' ? 'border-b-2' : ''}`}
            >
              CDT Questions ({filteredCdtQuestions.length})
            </button>
            <button
              onClick={() => setCurrentSection('icd')}
              className={`px-4 py-2 ${
                currentSection === 'icd' 
                  ? (isDark ? 'border-blue-500 text-blue-400' : 'border-blue-500 text-blue-700') 
                  : (isDark ? 'text-gray-400' : 'text-gray-500')
              } ${currentSection === 'icd' ? 'border-b-2' : ''}`}
            >
              ICD Questions ({filteredIcdQuestions.length})
            </button>
          </div>
        )}

        {/* Error Display */}
        {error && (
          <div className={`p-4 mb-4 rounded-lg ${isDark ? 'bg-red-900/30 text-red-200' : 'bg-red-100 text-red-700'}`}>
            {error}
          </div>
        )}
        
        {/* Form */}
        <form onSubmit={handleSubmit}>
          {/* CDT Questions */}
          {currentSection === 'cdt' && Object.keys(cdtQuestionsGrouped).length > 0 && (
            <div className="space-y-6">
              {Object.entries(cdtQuestionsGrouped).map(([scenarioId, questions]) => (
                <div key={`cdt-scenario-${scenarioId}`} className={`p-4 rounded-lg ${
                  isDark ? 'bg-gray-700/70' : 'bg-gray-100'
                } border ${isDark ? 'border-gray-600' : 'border-gray-300'}`}>
                  <div 
                    className="flex justify-between items-center cursor-pointer mb-2"
                    onClick={() => toggleScenarioExpand(scenarioId)}
                  >
                    <h3 className={`font-medium ${isDark ? 'text-yellow-300' : 'text-yellow-700'}`}>
                      Scenario #{scenarioId} ({questions.length} questions)
                    </h3>
                    <span>{expandedScenarios[scenarioId] ? '▼' : '▶'}</span>
                  </div>
                  
                  {(expandedScenarios[scenarioId] || true) && (
                    <div className={`mb-3 p-2 text-sm ${
                      isDark ? 'bg-gray-800/50 text-gray-300' : 'bg-white/80 text-gray-600'
                    } rounded`}>
                      {getScenarioText(scenarioId).substring(0, 100)}
                      {getScenarioText(scenarioId).length > 100 ? '...' : ''}
                    </div>
                  )}
                  
                  <div className="space-y-4">
                    {questions.map((question, index) => (
                      <div key={`cdt-${scenarioId}-${index}-${question.id}`} className={`p-3 rounded-lg ${
                        isDark ? 'bg-gray-800' : 'bg-white'
                      } border ${isDark ? 'border-gray-700' : 'border-gray-200'}`}>
                        <p className="mb-2 font-medium">{question.question}</p>
                        <div className="mt-2">
                          <textarea
                            name={`cdt-${question.id}`}
                            value={answers.cdt[question.id] || ''}
                            onChange={(e) => handleAnswerChange('cdt', question.id, e.target.value)}
                            placeholder="Enter your answer..."
                            className={`w-full p-2 rounded-md ${
                              isDark ? 'bg-gray-700 text-white border-gray-600' : 'bg-gray-50 text-gray-800 border-gray-300'
                            } border focus:outline-none focus:ring-2 ${
                              isDark ? 'focus:ring-blue-500' : 'focus:ring-blue-400'
                            }`}
                            rows="3"
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          )}
          
          {/* ICD Questions */}
          {currentSection === 'icd' && Object.keys(icdQuestionsGrouped).length > 0 && (
            <div className="space-y-6">
              {Object.entries(icdQuestionsGrouped).map(([scenarioId, questions]) => (
                <div key={`icd-scenario-${scenarioId}`} className={`p-4 rounded-lg ${
                  isDark ? 'bg-gray-700/70' : 'bg-gray-100'
                } border ${isDark ? 'border-gray-600' : 'border-gray-300'}`}>
                  <div 
                    className="flex justify-between items-center cursor-pointer mb-2"
                    onClick={() => toggleScenarioExpand(scenarioId)}
                  >
                    <h3 className={`font-medium ${isDark ? 'text-yellow-300' : 'text-yellow-700'}`}>
                      Scenario #{scenarioId} ({questions.length} questions)
                    </h3>
                    <span>{expandedScenarios[scenarioId] ? '▼' : '▶'}</span>
                  </div>
                  
                  {(expandedScenarios[scenarioId] || true) && (
                    <div className={`mb-3 p-2 text-sm ${
                      isDark ? 'bg-gray-800/50 text-gray-300' : 'bg-white/80 text-gray-600'
                    } rounded`}>
                      {getScenarioText(scenarioId).substring(0, 100)}
                      {getScenarioText(scenarioId).length > 100 ? '...' : ''}
                    </div>
                  )}
                  
                  <div className="space-y-4">
                    {questions.map((question, index) => (
                      <div key={`icd-${scenarioId}-${index}-${question.id}`} className={`p-3 rounded-lg ${
                        isDark ? 'bg-gray-800' : 'bg-white'
                      } border ${isDark ? 'border-gray-700' : 'border-gray-200'}`}>
                        <p className="mb-2 font-medium">{question.question}</p>
                        <div className="mt-2">
                          <textarea
                            name={`icd-${question.id}`}
                            value={answers.icd[question.id] || ''}
                            onChange={(e) => handleAnswerChange('icd', question.id, e.target.value)}
                            placeholder="Enter your answer..."
                            className={`w-full p-2 rounded-md ${
                              isDark ? 'bg-gray-700 text-white border-gray-600' : 'bg-gray-50 text-gray-800 border-gray-300'
                            } border focus:outline-none focus:ring-2 ${
                              isDark ? 'focus:ring-blue-500' : 'focus:ring-blue-400'
                            }`}
                            rows="3"
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Navigation/Submit Controls */}
          <div className="flex justify-between mt-6">
            {/* Switch Button - shows when there are both CDT and ICD questions */}
            {filteredCdtQuestions.length > 0 && filteredIcdQuestions.length > 0 && (
              <button
                type="button"
                onClick={switchSection}
                className={`px-4 py-2 rounded-lg ${
                  isDark ? 'bg-gray-700 text-gray-200 hover:bg-gray-600' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                {currentSection === 'cdt' ? 'View ICD Questions' : 'View CDT Questions'}
              </button>
            )}
            
            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading || !isFormComplete()}
              className={`px-4 py-2 rounded-lg ${
                isFormComplete() 
                  ? (isDark 
                      ? 'bg-blue-700 text-white hover:bg-blue-600' 
                      : 'bg-blue-600 text-white hover:bg-blue-700') 
                  : (isDark 
                      ? 'bg-gray-700 text-gray-400 cursor-not-allowed' 
                      : 'bg-gray-300 text-gray-500 cursor-not-allowed')
              }`}
            >
              {loading ? 'Submitting...' : 'Submit All Answers'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

Questioner.propTypes = {
  isVisible: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  questions: PropTypes.shape({
    cdt_questions: PropTypes.arrayOf(PropTypes.shape({
      id: PropTypes.string,
      question: PropTypes.string,
      scenarioId: PropTypes.string,
      recordId: PropTypes.string
    })),
    icd_questions: PropTypes.arrayOf(PropTypes.shape({
      id: PropTypes.string,
      question: PropTypes.string,
      scenarioId: PropTypes.string,
      recordId: PropTypes.string
    })),
    length: PropTypes.number,
    forEach: PropTypes.func,
    map: PropTypes.func
  }),
  onSubmitSuccess: PropTypes.func.isRequired,
  scenarios: PropTypes.array
};

export default Questioner; 