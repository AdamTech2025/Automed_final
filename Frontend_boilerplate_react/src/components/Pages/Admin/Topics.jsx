import { useState, useEffect, useCallback } from 'react';
import { getTopicsPrompts, updateTopicPrompt } from '../../../interceptors/services';
import { FaSpinner, FaChevronDown, FaChevronUp, FaSave } from 'react-icons/fa';
import { message } from 'antd';

const Topics = () => {
  const [topics, setTopics] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [editingTopicId, setEditingTopicId] = useState(null); // Track which topic is being edited locally
  const [editedTemplates, setEditedTemplates] = useState({}); // Store local edits { topicId: template }
  const [savingTopicId, setSavingTopicId] = useState(null); // Track which topic is currently saving
  const [expandedTopicId, setExpandedTopicId] = useState(null); // Track which topic accordion is open

  const fetchTopics = useCallback(async (signal) => {
    setLoading(true);
    setError(null);
    try {
      const response = await getTopicsPrompts(signal);
      setTopics(response?.topics || []);
      // Initialize editedTemplates with fetched data
      const initialTemplates = (response?.topics || []).reduce((acc, topic) => {
        acc[topic.id] = topic.template;
        return acc;
      }, {});
      setEditedTemplates(initialTemplates);
    } catch (err) {
      if (err.name !== 'AbortError') {
        console.error("Failed to fetch topics:", err);
        setError(err.message || 'Failed to load topics.');
        message.error(err.message || 'Failed to load topics.');
      }
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    const controller = new AbortController();
    fetchTopics(controller.signal);
    return () => controller.abort(); // Cleanup on unmount
  }, [fetchTopics]);

  const handleTemplateChange = (topicId, value) => {
    setEditedTemplates(prev => ({ ...prev, [topicId]: value }));
    setEditingTopicId(topicId); // Mark this topic as having local edits
  };

  const handleSaveChanges = async (topicId) => {
    const templateToSave = editedTemplates[topicId];
    if (!templateToSave) return;

    setSavingTopicId(topicId);
    setError(null);
    const controller = new AbortController();

    try {
      await updateTopicPrompt(topicId, templateToSave, controller.signal);
      message.success(`Prompt for topic ${topics.find(t => t.id === topicId)?.name || topicId} updated successfully!`);
      setEditingTopicId(null); // Clear editing state after successful save
      // Optionally re-fetch to confirm or update local state directly if API returns updated data
      // To keep it simple, we assume the local state is now the source of truth until next fetch
      setTopics(prevTopics => 
        prevTopics.map(t => t.id === topicId ? { ...t, template: templateToSave } : t)
      );

    } catch (err) {
      if (err.name !== 'AbortError') {
        console.error(`Failed to update topic ${topicId}:`, err);
        setError(err.message || `Failed to update topic ${topicId}.`);
        message.error(err.message || `Failed to update topic ${topicId}.`);
      }
    } finally {
      setSavingTopicId(null);
    }
  };

  const toggleExpand = (topicId) => {
    setExpandedTopicId(prev => (prev === topicId ? null : topicId));
  };

  if (loading && topics.length === 0) { // Show loader only on initial load
    return (
      <div className="flex justify-center items-center h-64">
        <FaSpinner className="animate-spin text-4xl text-[var(--color-primary)]" />
        <span className="ml-4 text-lg text-[var(--color-text-secondary)]">Loading Topics...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-8 text-center">
        <p className="text-red-500 dark:text-red-400">{error}</p>
        <button
          onClick={() => fetchTopics(new AbortController().signal)}
          className="mt-4 px-4 py-2 bg-[var(--color-primary)] text-white rounded hover:bg-[var(--color-primary-hover)]"
          disabled={loading}
        >
          {loading ? <FaSpinner className="animate-spin inline mr-2" /> : null}
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="p-4 md:p-8 bg-[var(--color-bg-primary)] text-[var(--color-text-primary)]">
      <h1 className="text-2xl font-bold mb-6 text-[var(--color-text-primary)] border-b border-[var(--color-border)] pb-2">Manage Topic Prompts</h1>

      <div className="space-y-4">
        {topics.map((topic) => {
          const isExpanded = expandedTopicId === topic.id;
          const isEditing = editingTopicId === topic.id;
          const isSaving = savingTopicId === topic.id;
          const hasUnsavedChanges = isEditing && topic.template !== editedTemplates[topic.id];

          return (
            <div key={topic.id} className="border border-[var(--color-border)] rounded-lg overflow-hidden shadow-sm bg-[var(--color-bg-secondary)]">
              {/* Accordion Header */}
              <button
                onClick={() => toggleExpand(topic.id)}
                className="flex justify-between items-center w-full p-4 text-left hover:bg-[var(--color-bg-primary)] transition-colors duration-150 focus:outline-none"
              >
                <span className="font-semibold text-lg text-[var(--color-text-primary)]">{topic.name}</span>
                <div className="flex items-center">
                   {hasUnsavedChanges && !isSaving && (
                     <span className="text-xs text-yellow-500 dark:text-yellow-400 mr-2 italic">(Unsaved changes)</span>
                   )}
                   {isSaving && <FaSpinner className="animate-spin text-[var(--color-primary)] mr-3" />}
                   {isExpanded ? <FaChevronUp className="text-[var(--color-text-secondary)]"/> : <FaChevronDown className="text-[var(--color-text-secondary)]"/>}
                </div>
              </button>

              {/* Accordion Content */}
              {isExpanded && (
                <div className="p-4 border-t border-[var(--color-border)] bg-[var(--color-input-bg)]">
                  <label htmlFor={`template-${topic.id}`} className="block text-sm font-medium text-[var(--color-text-secondary)] mb-2">
                    Prompt Template:
                  </label>
                  <textarea
                    id={`template-${topic.id}`}
                    value={editedTemplates[topic.id] || ''}
                    onChange={(e) => handleTemplateChange(topic.id, e.target.value)}
                    className="w-full border rounded-lg p-3 bg-[var(--color-input-bg)] text-[var(--color-text-primary)] border-[var(--color-border)] focus:ring-2 focus:ring-[var(--color-primary)] text-sm font-mono leading-relaxed min-h-[200px] h-auto resize-y"
                    placeholder="Enter the prompt template..."
                    rows={15} // Suggest a default number of rows
                    disabled={isSaving}
                  />
                  <div className="mt-4 flex justify-end">
                    <button
                      onClick={() => handleSaveChanges(topic.id)}
                      disabled={isSaving || !hasUnsavedChanges}
                      className="flex items-center px-4 py-2 bg-green-600 hover:bg-green-700 text-white text-sm rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-1 focus:ring-green-500"
                    >
                      {isSaving ? (
                        <>
                          <FaSpinner className="animate-spin inline mr-2" /> Saving...
                        </>
                      ) : (
                        <>
                           <FaSave className="inline mr-2" /> Save Changes
                        </>
                      )}
                    </button>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default Topics; 