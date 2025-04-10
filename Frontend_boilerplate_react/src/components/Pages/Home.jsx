import { FaTooth, FaCogs } from 'react-icons/fa';
import { analyzeDentalScenario } from '../../interceptors/services.js'; // Adjust path as needed
import { useState } from 'react';

const Home = () => {
  const [scenario, setScenario] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await analyzeDentalScenario({ scenario });
      setResult(response);
    } catch (err) {
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

  return (
    <div className="flex flex-col bg-gray-100">
      {/* Main content container */}
      <div className="flex-grow flex items-center justify-center p-4">
        <div className="w-full p-2 md:p-6 bg-white rounded-lg shadow-lg">
          {/* Header */}
          <div className="bg-blue-500 text-white p-4 rounded-lg mb-6">
            <h2 className="text-xl md:text-2xl font-semibold flex items-center">
              <FaTooth className="mr-2" /> Dental Scenario
            </h2>
          </div>

          {/* Form */}
          <div className="p-4">
            <form id="dental-form" className="space-y-4" onSubmit={handleSubmit}>
              <div>
                <label
                  htmlFor="scenario"
                  className="block text-gray-700 font-medium mb-2 text-sm md:text-base"
                >
                  Enter dental scenario to analyze:
                </label>
                <textarea
                  id="scenario"
                  name="scenario"
                  rows="6"
                  className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 text-sm md:text-base"
                  placeholder="Describe the dental procedure or diagnosis..."
                  value={scenario}
                  onChange={(e) => setScenario(e.target.value)}
                  onKeyDown={handleKeyDown}
                  required
                ></textarea>
              </div>
              <div className="flex justify-end">
                <button
                  type="submit"
                  className="bg-blue-600 text-white px-4 py-2 md:px-6 md:py-2 rounded-lg shadow-md hover:bg-blue-700 disabled:bg-gray-400 text-sm md:text-base"
                  disabled={loading}
                >
                  <FaCogs className="inline mr-2" />
                  {loading ? 'Analyzing...' : 'Analyze'}
                </button>
              </div>
            </form>

            {/* Result */}
            {result && (
              <div className="mt-4 p-4 bg-green-100 rounded-lg overflow-auto">
                <h3 className="font-semibold text-sm md:text-base">Analysis Result:</h3>
                <pre className="text-xs md:text-sm">{JSON.stringify(result, null, 2)}</pre>
              </div>
            )}

            {/* Error */}
            {error && (
              <div className="mt-4 p-4 bg-red-100 rounded-lg">
                <h3 className="font-semibold text-red-800 text-sm md:text-base">Error:</h3>
                <p className="text-xs md:text-sm">{error}</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;