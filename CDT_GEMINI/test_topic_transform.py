"""
Stand-alone test for the topic transformation function.
"""
import json
import re

def transform_topics_for_db(topics_data):
    """
    Transform the complex topics structure into a simplified format for database storage.
    
    Args:
        topics_data (dict): Original topics data structure
        
    Returns:
        dict: Simplified topics structure with clean format
    """
    transformed_topics = {}
    
    for range_code, topic_data in topics_data.items():
        topic_name = topic_data.get("name", "Unknown")
        activation_result = topic_data.get("result", {})
        
        # Extract key information from the activation result
        explanation = activation_result.get("explanation", "")
        doubt = activation_result.get("doubt", "")
        activated_subtopics = activation_result.get("activated_subtopics", [])
        
        # Extract code range - handle case where it contains explanation text
        code_range = activation_result.get("code_range", "")
        if "\nCODE RANGE:" in code_range:
            # It's a complex block, extract just the code range part
            code_match = re.search(r'\nCODE RANGE:\s*(.*?)(?:\n|$)', code_range)
            if code_match:
                code_range = code_match.group(1).strip()
            else:
                # Fallback to the full text if no match
                code_range = code_range
        
        # Create a simplified structure for the topic
        transformed_topics[range_code] = {
            "name": topic_name,
            "result": {
                "EXPLANATION": explanation,
                "DOUBT": doubt,
                "CODE": code_range
            },
            "activated_subtopics": activated_subtopics
        }
    
    return transformed_topics

def test_transform_topics_for_db():
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
    
    # Run the transformation
    result = transform_topics_for_db(sample_topics)
    
    # Pretty print the result for debugging
    print(f"\nOriginal topics:")
    print(json.dumps(sample_topics, indent=2))
    
    print(f"\nTransformed topics:")
    print(json.dumps(result, indent=2))
    
    # Test with complex real-world data
    print("\nTesting with real-world data:")
    real_topics = {
        "D0100-D0999": {
            "name": "Diagnostic",
            "result": {
                "code_range": "EXPLANATION:The scenario describes a routine examination (first exam), a cleaning, fluoride application, and the identification of a space maintainer needing removal.  This necessitates a clinical evaluation (D0120-D0180) to assess the patient's oral condition and identify the space maintainer issue.  The removal of the space maintainer is a treatment procedure, but the specific CDT codes for that procedure are missing, so we cannot determine the exact code.  However, the evaluation and treatment are related, and the evaluation is the primary focus of the visit.\n\nDOUBT: The scenario lacks specific details about the complexity of the evaluation (e.g., comprehensive vs. limited).  Without the CDT codes for the space maintainer removal, the exact billing for that procedure is unknown.  Also, the absence of patient statements and specific details about the examination (e.g., specific findings) limits the precision of the coding.\n\nCODE RANGE: D0120-D0180, D0190-D0191",
                "subtopic": "Clinical Oral Evaluations (D0120-D0180)",
                "activated_subtopics": [
                    "Clinical Oral Evaluations (D0120-D0180)",
                    "Pre-diagnostic Services (D0190-D0191)"
                ],
                "codes": [
                    "EXPLANATION: The scenario states \"First exam performed.\" This indicates a comprehensive evaluation, typically performed for new patients or established patients requiring a thorough assessment after a significant time lapse or change in health status, aligning with the description for D0150. While a specific problem (space maintainer) was identified and addressed, the note explicitly mentions it was the \"First exam,\" suggesting a scope beyond a limited, problem-focused evaluation (D0140). D0150 encompasses the necessary components like history, screenings, and charting expected in an initial comprehensive assessment.\nDOUBT: Was this the patient's first visit to this specific practice, confirming \"new patient\" status for D0150? Or was the patient established but hadn't had a comprehensive evaluation in over 3 years? Does \"First exam performed\" definitively mean all components required for D0150 (e.g., full perio charting, occlusion/TMJ review) were completed and documented?\nCODE: D0150",
                    "EXPLANATION: The patient presented with a space maintainer that needed removal.  The provider performed the removal.  This is a procedure, not a screening or assessment.\nDOUBT:  While the initial exam and cleaning are part of the visit, the primary reason for the visit and the billable service is the space maintainer removal.  The provided scenario lacks sufficient detail to determine if the cleaning and exam were separately billable.\nCODE: D4340\n\nEXPLANATION: Removal of fixed space maintainer.\nDOUBT:  The scenario lacks specific CDT codes for the procedures.  Additional information is needed to determine if other codes are applicable.\nCODE: D7300"
                ],
                "explanation": "The scenario describes a routine examination (first exam), a cleaning, fluoride application, and the identification of a space maintainer needing removal.  This necessitates a clinical evaluation (D0120-D0180) to assess the patient's oral condition and identify the space maintainer issue.  The removal of the space maintainer is a treatment procedure, but the specific CDT codes for that procedure are missing, so we cannot determine the exact code.  However, the evaluation and treatment are related, and the evaluation is the primary focus of the visit.",
                "doubt": "The scenario lacks specific details about the complexity of the evaluation (e.g., comprehensive vs. limited).  Without the CDT codes for the space maintainer removal, the exact billing for that procedure is unknown.  Also, the absence of patient statements and specific details about the examination (e.g., specific findings) limits the precision of the coding."
            }
        }
    }
    
    transformed_real = transform_topics_for_db(real_topics)
    print(json.dumps(transformed_real, indent=2))

if __name__ == "__main__":
    test_transform_topics_for_db() 