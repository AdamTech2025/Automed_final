import { useState } from "react";
import { submitQuestionAnswers } from "../../interceptors/services";
import { useTheme } from '../../context/ThemeContext';
import PropTypes from 'prop-types';

const Questioner = ({ isVisible, onClose, questions, recordId, onSubmitSuccess }) => {
  const { isDark } = useTheme();
  const [answers, setAnswers] = useState({
    cdt: {},
    icd: {}
  });
  const [loading, setLoading] = useState(false);
  const [currentSection, setCurrentSection] = useState('cdt');
  const [error, setError] = useState(null);

  // Filter out questions with "none" as the id
  const filteredCdtQuestions = questions.cdt_questions.filter(q => q.id !== "none" && q.id.toLowerCase() !== "none");
  const filteredIcdQuestions = questions.icd_questions.filter(q => q.id !== "none" && q.id.toLowerCase() !== "none");

  const handleAnswerChange = (section, questionId, value) => {
    setAnswers(prev => ({
      ...prev,
      [section]: {
        ...prev[section],
        [questionId]: value
      }
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const payload = {
      cdt_answers: Object.entries(answers.cdt).map(([id, value]) => ({
        id,
        answer: value
      })),
      icd_answers: Object.entries(answers.icd).map(([id, value]) => ({
        id,
        answer: value
      }))
    };

    try {
      const response = await submitQuestionAnswers(payload, recordId);
      onSubmitSuccess(response);
      // If successful, close the modal
      if (response && response.status === 'success') {
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
    // Check if all questions in the current section have been answered
    const currentQuestions = currentSection === 'cdt' ? filteredCdtQuestions : filteredIcdQuestions;
    return currentQuestions.every(q => answers[currentSection][q.id] !== undefined);
  };

  const switchSection = () => {
    setCurrentSection(prev => prev === 'cdt' ? 'icd' : 'cdt');
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
        className={`relative w-full max-w-lg mx-auto p-6 rounded-lg shadow-xl ${
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
          {currentSection === 'cdt' ? 'CDT Code Questions' : 'ICD Code Questions'}
        </h2>
        
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
              CDT Questions
            </button>
            <button
              onClick={() => setCurrentSection('icd')}
              className={`px-4 py-2 ${
                currentSection === 'icd' 
                  ? (isDark ? 'border-blue-500 text-blue-400' : 'border-blue-500 text-blue-700') 
                  : (isDark ? 'text-gray-400' : 'text-gray-500')
              } ${currentSection === 'icd' ? 'border-b-2' : ''}`}
            >
              ICD Questions
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
          {currentSection === 'cdt' && filteredCdtQuestions.length > 0 && (
            <div className="space-y-4">
              {filteredCdtQuestions.map((question, index) => (
                <div key={`cdt-${index}-${question.id}`} className={`p-4 rounded-lg ${
                  isDark ? 'bg-gray-700' : 'bg-gray-50'
                }`}>
                  <p className="mb-2 font-medium">{question.question}</p>
                  <div className="space-y-2">
                    <label className="block">
                      <input
                        type="radio"
                        name={`cdt-${question.id}`}
                        value="yes"
                        onChange={() => handleAnswerChange('cdt', question.id, 'yes')}
                        checked={answers.cdt[question.id] === 'yes'}
                        className="mr-2"
                      />
                      Yes
                    </label>
                    <label className="block">
                      <input
                        type="radio"
                        name={`cdt-${question.id}`}
                        value="no"
                        onChange={() => handleAnswerChange('cdt', question.id, 'no')}
                        checked={answers.cdt[question.id] === 'no'}
                        className="mr-2"
                      />
                      No
                    </label>
                  </div>
                </div>
              ))}
            </div>
          )}
          
          {/* ICD Questions */}
          {currentSection === 'icd' && filteredIcdQuestions.length > 0 && (
            <div className="space-y-4">
              {filteredIcdQuestions.map((question, index) => (
                <div key={`icd-${index}-${question.id}`} className={`p-4 rounded-lg ${
                  isDark ? 'bg-gray-700' : 'bg-gray-50'
                }`}>
                  <p className="mb-2 font-medium">{question.question}</p>
                  <div className="space-y-2">
                    <label className="block">
                      <input
                        type="radio"
                        name={`icd-${question.id}`}
                        value="yes"
                        onChange={() => handleAnswerChange('icd', question.id, 'yes')}
                        checked={answers.icd[question.id] === 'yes'}
                        className="mr-2"
                      />
                      Yes
                    </label>
                    <label className="block">
                      <input
                        type="radio"
                        name={`icd-${question.id}`}
                        value="no"
                        onChange={() => handleAnswerChange('icd', question.id, 'no')}
                        checked={answers.icd[question.id] === 'no'}
                        className="mr-2"
                      />
                      No
                    </label>
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
                {currentSection === 'cdt' ? 'Next: ICD Questions' : 'Back to CDT Questions'}
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
              {loading ? 'Submitting...' : 'Submit Answers'}
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
    cdt_questions: PropTypes.array,
    icd_questions: PropTypes.array
  }).isRequired,
  recordId: PropTypes.string.isRequired,
  onSubmitSuccess: PropTypes.func
};

export default Questioner; 