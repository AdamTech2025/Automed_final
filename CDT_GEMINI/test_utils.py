"""
Unit tests for utility functions in the dental code extraction application.
"""

import unittest
import json
from app import transform_topics_for_db

class TestTopicTransformation(unittest.TestCase):
    """Test cases for the topics data transformation function."""
    
    def test_transform_topics_for_db(self):
        """Test that the topics transformation function works correctly."""
        # Sample input data
        sample_topics = {
            "D0100-D0999": {
                "name": "Diagnostic",
                "result": {
                    "code_range": "D0120-D0180, D0190-D0191",
                    "subtopic": "Clinical Oral Evaluations (D0120-D0180)",
                    "activated_subtopics": [
                        "Clinical Oral Evaluations (D0120-D0180)",
                        "Pre-diagnostic Services (D0190-D0191)"
                    ],
                    "codes": [
                        "EXPLANATION: First exam performed.\nDOUBT: None.\nCODE: D0150",
                        "EXPLANATION: Space maintainer removal.\nDOUBT: None.\nCODE: D7300"
                    ],
                    "explanation": "The scenario describes a routine examination.",
                    "doubt": "The scenario lacks specific details."
                }
            },
            "D1000-D1999": {
                "name": "Preventive",
                "result": {
                    "code_range": "D1120, D1206, D1555",
                    "subtopic": "Dental Prophylaxis (D1110-D1120)",
                    "activated_subtopics": [],
                    "codes": [],
                    "explanation": "The patient is an 11-year-old.",
                    "doubt": "The documentation lacks specifics."
                }
            }
        }
        
        # Expected transformed data
        expected_result = {
            "D0100-D0999": {
                "name": "Diagnostic",
                "result": {
                    "EXPLANATION": "The scenario describes a routine examination.",
                    "DOUBT": "The scenario lacks specific details.",
                    "CODE": "D0120-D0180, D0190-D0191"
                },
                "activated_subtopics": [
                    "Clinical Oral Evaluations (D0120-D0180)",
                    "Pre-diagnostic Services (D0190-D0191)"
                ]
            },
            "D1000-D1999": {
                "name": "Preventive",
                "result": {
                    "EXPLANATION": "The patient is an 11-year-old.",
                    "DOUBT": "The documentation lacks specifics.",
                    "CODE": "D1120, D1206, D1555"
                },
                "activated_subtopics": []
            }
        }
        
        # Run the transformation
        result = transform_topics_for_db(sample_topics)
        
        # Compare with expected result
        self.assertEqual(result, expected_result)
        
        # Pretty print the result for debugging
        print(f"\nTransformed topics:")
        print(json.dumps(result, indent=2))
        
        # Also test with empty data
        empty_result = transform_topics_for_db({})
        self.assertEqual(empty_result, {})
        
        # Test with missing fields
        partial_data = {
            "D0100-D0999": {
                "name": "Diagnostic",
                "result": {
                    "explanation": "Only explanation provided"
                }
            }
        }
        
        partial_result = transform_topics_for_db(partial_data)
        self.assertEqual(
            partial_result["D0100-D0999"]["result"]["EXPLANATION"],
            "Only explanation provided"
        )
        self.assertEqual(partial_result["D0100-D0999"]["result"]["DOUBT"], "")
        self.assertEqual(partial_result["D0100-D0999"]["result"]["CODE"], "")
        self.assertEqual(partial_result["D0100-D0999"]["activated_subtopics"], [])

if __name__ == "__main__":
    unittest.main() 