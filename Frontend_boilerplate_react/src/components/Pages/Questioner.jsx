import { useState, useEffect } from 'react';
import { Modal, Form, Input, Button, Typography, Space, Spin, message } from 'antd';
import { QuestionCircleOutlined, SendOutlined } from '@ant-design/icons';
import { submitQuestionAnswers } from '../../interceptors/services';
import PropTypes from 'prop-types';

const { Title, Text } = Typography;

const Questioner = ({ 
  isVisible, 
  onClose, 
  questions, 
  recordId, 
  onSubmitSuccess 
}) => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [cdtQuestions, setCdtQuestions] = useState([]);
  const [icdQuestions, setIcdQuestions] = useState([]);

  useEffect(() => {
    // Process questions when they change
    if (questions) {
      setCdtQuestions(questions.cdt_questions || []);
      setIcdQuestions(questions.icd_questions || []);
    }
  }, [questions]);

  useEffect(() => {
    console.log('Questioner rendered with props:', { 
      isVisible, 
      recordId,
      questionCount: {
        cdt: questions?.cdt_questions?.length || 0,
        icd: questions?.icd_questions?.length || 0
      }
    });
  }, [isVisible, recordId, questions]);

  const handleSubmit = async () => {
    try {
      setLoading(true);
      const values = await form.validateFields();
      
      console.log('Submitting answers for record ID:', recordId);
      console.log('Form values:', values);
      
      if (!recordId) {
        throw new Error('Record ID is missing');
      }
      
      // Submit answers to the backend
      const response = await submitQuestionAnswers(values, recordId);
      
      if (response.status === 'error') {
        // If there's an error message in the response, display it
        message.error(response.message || 'Server returned an error');
        console.error('Server error:', response.message);
        return; // Don't close modal or reset form on error
      }
      
      message.success('Answers submitted successfully');
      
      // Reset form
      form.resetFields();
      
      // Close modal and trigger success callback with the response data
      if (onSubmitSuccess) {
        onSubmitSuccess(response);
      }
      
      onClose();
    } catch (error) {
      console.error('Error submitting answers:', error);
      message.error(error.message || 'Failed to submit answers');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal
      title={
        <Space>
          <QuestionCircleOutlined style={{ color: '#faad14' }} />
          <span>Additional Information Needed</span>
        </Space>
      }
      open={isVisible}
      onCancel={onClose}
      width={700}
      footer={[
        <Button key="cancel" onClick={onClose} disabled={loading}>
          Cancel
        </Button>,
        <Button 
          key="submit" 
          type="primary" 
          onClick={handleSubmit} 
          loading={loading}
          icon={<SendOutlined />}
        >
          Submit Answers
        </Button>
      ]}
    >
      {loading ? (
        <div style={{ textAlign: 'center', padding: '20px' }}>
          <Spin size="large" />
          <div style={{ marginTop: '10px' }}>Processing your answers...</div>
        </div>
      ) : (
        <Form form={form} layout="vertical">
          {cdtQuestions.length > 0 && (
            <>
              <Title level={4} style={{ color: '#2c3e50', marginBottom: '16px' }}>
                CDT Questions
              </Title>
              {cdtQuestions.map((question, index) => (
                <Form.Item 
                  key={`cdt-${index}`} 
                  name={question}
                  label={<Text style={{ fontSize: '14px' }}>{question}</Text>}
                  rules={[{ required: true, message: 'Please provide an answer' }]}
                >
                  <Input placeholder="Your answer" />
                </Form.Item>
              ))}
            </>
          )}

          {icdQuestions.length > 0 && (
            <>
              <Title level={4} style={{ color: '#2c3e50', marginBottom: '16px', marginTop: '24px' }}>
                ICD Questions
              </Title>
              {icdQuestions.map((question, index) => (
                <Form.Item 
                  key={`icd-${index}`} 
                  name={question}
                  label={<Text style={{ fontSize: '14px' }}>{question}</Text>}
                  rules={[{ required: true, message: 'Please provide an answer' }]}
                >
                  <Input placeholder="Your answer" />
                </Form.Item>
              ))}
            </>
          )}
        </Form>
      )}
    </Modal>
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