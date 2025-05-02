import { useState } from 'react';
import { FaUpload, FaFile, FaImage, FaFileAlt, FaSpinner, FaCopy, FaCheck } from 'react-icons/fa';
import { useTheme } from '../../context/ThemeContext';
import { uploadAndExtract } from '../../interceptors/services';

const Extractor = () => {
  const { isDark } = useTheme();
  const [file, setFile] = useState(null);
  const [fileName, setFileName] = useState('');
  const [extractedData, setExtractedData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [copiedIndex, setCopiedIndex] = useState(null);

  const getFileIcon = (type) => {
    if (type?.startsWith('image/')) return <FaImage className="w-6 h-6" />;
    if (type?.includes('pdf')) return <FaFileAlt className="w-6 h-6" />;
    return <FaFile className="w-6 h-6" />;
  };

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setFileName(selectedFile.name);
      setError(null);
    }
  };

  const handleCopyScenario = async (text, index) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopiedIndex(index);
      setTimeout(() => setCopiedIndex(null), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;

    setIsLoading(true);
    setError(null);

    try {
      const result = await uploadAndExtract(file);
      setExtractedData(result);
    } catch (err) {
      setError(err.message || 'Failed to process file');
      setExtractedData(null);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className={`max-w-4xl mx-auto`}>
        {/* Upload Section */}
        <div className={`p-6 rounded-lg shadow-lg mb-8
          ${isDark ? 'bg-[var(--color-bg-card)] border border-gray-700' : 'bg-white border border-gray-200'}`}>
          
          <h1 className={`text-2xl font-bold mb-6 text-center
            ${isDark ? 'text-gray-100' : 'text-gray-800'}`}>
            Document Extractor
          </h1>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="flex flex-col items-center justify-center w-full">
              <label 
                htmlFor="file-upload"
                className={`w-full h-40 border-2 border-dashed rounded-lg cursor-pointer
                  flex flex-col items-center justify-center
                  ${isDark ? 'border-gray-600 hover:border-blue-500' : 'border-gray-300 hover:border-blue-600'}
                  transition-colors duration-200
                  ${file ? 'bg-opacity-50 bg-blue-50 dark:bg-opacity-10 dark:bg-blue-900' : ''}`}
              >
                <div className="flex flex-col items-center justify-center py-6">
                  {file ? (
                    <div className="flex items-center space-x-3">
                      {getFileIcon(file.type)}
                      <span className={`text-sm ${isDark ? 'text-gray-300' : 'text-gray-600'}`}>
                        {fileName}
                      </span>
                    </div>
                  ) : (
                    <>
                      <FaUpload className={`w-10 h-10 mb-3 ${isDark ? 'text-gray-400' : 'text-gray-500'}`} />
                      <p className={`text-sm ${isDark ? 'text-gray-400' : 'text-gray-500'}`}>
                        Click to upload or drag and drop
                      </p>
                      <p className={`text-xs mt-2 ${isDark ? 'text-gray-500' : 'text-gray-400'}`}>
                        PDF, TXT, DOC, or Image files
                      </p>
                    </>
                  )}
                </div>
                <input
                  id="file-upload"
                  type="file"
                  className="hidden"
                  onChange={handleFileChange}
                  accept=".pdf,.txt,.doc,.docx,.png,.jpg,.jpeg"
                />
              </label>
            </div>

            {error && (
              <div className="text-red-500 text-sm text-center">
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={!file || isLoading}
              className={`w-full py-3 px-4 rounded-md font-medium flex items-center justify-center
                ${isDark 
                  ? 'bg-blue-600 hover:bg-blue-700 text-white' 
                  : 'bg-blue-500 hover:bg-blue-600 text-white'}
                disabled:opacity-50 disabled:cursor-not-allowed
                transition-colors duration-200`}
            >
              {isLoading ? (
                <>
                  <FaSpinner className="animate-spin mr-2" />
                  Processing...
                </>
              ) : (
                'Extract Content'
              )}
            </button>
          </form>
        </div>

        {/* Results Section */}
        {extractedData && (
          <div className={`space-y-6`}>
            <div className={`p-4 rounded-lg shadow-lg
              ${isDark ? 'bg-[var(--color-bg-card)] border border-gray-700' : 'bg-white border border-gray-200'}`}>
              <div className="flex items-center justify-between mb-4">
                <h2 className={`text-xl font-semibold
                  ${isDark ? 'text-gray-100' : 'text-gray-800'}`}>
                  Extracted Scenarios
                </h2>
                <span className={`text-sm ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
                  {extractedData.scenarios?.length || 0} scenarios found
                </span>
              </div>
            </div>

            {/* Scenarios Grid */}
            <div className="grid grid-cols-1 gap-6">
              {extractedData.scenarios?.map((scenario, index) => (
                <div
                  key={index}
                  className={`p-6 rounded-lg shadow-lg relative
                    ${isDark ? 'bg-[var(--color-bg-card)] border border-gray-700' : 'bg-white border border-gray-200'}`}
                >
                  <div className="flex justify-between items-start mb-4">
                    <h3 className={`text-lg font-medium
                      ${isDark ? 'text-gray-200' : 'text-gray-700'}`}>
                      Scenario {index + 1}
                    </h3>
                    <button
                      onClick={() => handleCopyScenario(scenario, index)}
                      className={`p-2 rounded-md transition-colors duration-200
                        ${isDark 
                          ? 'hover:bg-gray-700 text-gray-400 hover:text-gray-200' 
                          : 'hover:bg-gray-100 text-gray-600 hover:text-gray-800'}`}
                      title="Copy scenario"
                    >
                      {copiedIndex === index ? (
                        <FaCheck className="w-5 h-5 text-green-500" />
                      ) : (
                        <FaCopy className="w-5 h-5" />
                      )}
                    </button>
                  </div>
                  <div className={`whitespace-pre-wrap text-sm
                    ${isDark ? 'text-gray-300' : 'text-gray-600'}`}>
                    {scenario}
                  </div>
                </div>
              ))}
            </div>

            {/* Message */}
            {extractedData.message && (
              <div className={`p-4 rounded-lg text-center text-sm
                ${isDark ? 'bg-green-900 text-green-200' : 'bg-green-50 text-green-700'}`}>
                {extractedData.message}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default Extractor; 