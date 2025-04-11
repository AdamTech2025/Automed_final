import os
import sys
import logging
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from llm_services import create_chain, invoke_chain, set_model_for_file

# Load environment variables
load_dotenv()

# Set a specific model for this file (optional)
# set_model_for_file("gemini-2.5-pro-exp-03-25-thinking-exp-01-21")

def setup_logging():
    """Configure logging for the ICD inspector module."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]
    )
    return logging.getLogger(__name__)

logger = setup_logging()

def create_icd_inspector(temperature=0.0):
    """
    Create an ICD code inspector chain.
    """
    prompt_template = PromptTemplate(
        template="""
You are a highly experienced medical coding expert with over 15 years of expertise in ICD-10-CM codes for dental scenarios. 
Your task is to analyze the given dental scenario and provide final ICD-10-CM code recommendations.

Scenario:
{scenario}

Topic Analysis Results:
{topic_analysis}

Additional Information from Questions (if any):
{questioner_data}

Please provide a thorough analysis of this scenario by:
1. Only select the suitable ICD-10-CM code(s) from the suggested answers in the topic analysis
2. Be very specific, your answer is final so be careful, no errors can be tolerated
3. Don't assume anything that is not explicitly stated in the scenario
4. If a code has doubt or mentions information is not specifically stated, do not include that code
5. Choose the best between mutually exclusive codes, don't bill for the same condition twice
6. Consider any additional information provided through the question-answer process

IMPORTANT: You must format your response exactly as follows:

CODES: [comma-separated list of ICD-10-CM codes, with no square brackets around individual codes]

EXPLANATION: [provide a detailed explanation for why each code was selected or rejected. Include specific reasoning for each code mentioned in the topic analysis and explain the clinical significance.]

For example:
CODES: K05.1, Z91.89

EXPLANATION: K05.1 (Chronic gingivitis) is appropriate as the scenario describes inflammation of the gums that has persisted for several months. Z91.89 (Other specified personal risk factors) is included to document the patient's tobacco use which is significant for their periodontal condition. K05.2 was rejected because while there is gum disease, there is no evidence of destruction of the supporting structures required for periodontitis diagnosis.
""",
        input_variables=["scenario", "topic_analysis", "questioner_data"]
    )
    
    return create_chain(prompt_template)

def analyze_icd_scenario(scenario, topic_analysis, questioner_data=None):
    try:
        chain = create_icd_inspector(temperature=0.0)
        
        # Use scenario directly - it's already the cleaned data
        processed_scenario = scenario
        
        # Convert topic_analysis to string if it's a dictionary
        if topic_analysis is None:
            topic_analysis_str = "No ICD data analysis data available in DB"
        elif isinstance(topic_analysis, dict):
            # If the data is coming from the database dental_report table
            formatted_topics = []
            for category_num, topic_data in topic_analysis.items():
                # Format each topic's data in a readable way
                topic_name = topic_data.get("name", "Unknown")
                topic_result = topic_data.get("result", "No result")
                parsed_result = topic_data.get("parsed_result", {})
                
                # Format the parsed result if available
                parsed_lines = []
                if parsed_result:
                    if "code" in parsed_result and parsed_result["code"]:
                        parsed_lines.append(f"CODE: {parsed_result['code']}")
                    if "explanation" in parsed_result and parsed_result["explanation"]:
                        parsed_lines.append(f"EXPLANATION: {parsed_result['explanation']}")
                    if "doubt" in parsed_result and parsed_result["doubt"]:
                        parsed_lines.append(f"DOUBT: {parsed_result['doubt']}")
                
                # Combine all information
                topic_info = f"Category {category_num}: {topic_name}\n"
                
                if parsed_lines:
                    topic_info += "PARSED RESULT:\n" + "\n".join(parsed_lines) + "\n"
                
                topic_info += f"RAW RESULT:\n{topic_result}"
                formatted_topics.append(topic_info)
            
            topic_analysis_str = "\n\n".join(formatted_topics)
        else:
            topic_analysis_str = str(topic_analysis)
        
        # Format questioner_data if provided
        if questioner_data is None:
            questioner_data_str = "No additional information provided."
        elif isinstance(questioner_data, dict):
            if questioner_data.get("has_questions", False) and questioner_data.get("has_answers", False):
                # Format as question-answer pairs
                qa_pairs = []
                answers = questioner_data.get("answers", {})
                
                # Handle CDT questions
                cdt_questions = questioner_data.get("cdt_questions", {}).get("questions", [])
                for question in cdt_questions:
                    answer = answers.get(question, "No answer provided")
                    qa_pairs.append(f"CDT Q: {question}\nA: {answer}")
                
                # Handle ICD questions
                icd_questions = questioner_data.get("icd_questions", {}).get("questions", [])
                for question in icd_questions:
                    answer = answers.get(question, "No answer provided")
                    qa_pairs.append(f"ICD Q: {question}\nA: {answer}")
                
                questioner_data_str = "\n".join(qa_pairs) if qa_pairs else "Questions were asked but no answers were provided."
            elif questioner_data.get("has_questions", False):
                # Questions exist but no answers yet
                questioner_data_str = "Questions were identified but not yet answered."
            else:
                questioner_data_str = "No additional questions were needed."
        else:
            questioner_data_str = str(questioner_data)
        
        result = invoke_chain(chain, {
            "scenario": processed_scenario, 
            "topic_analysis": topic_analysis_str,
            "questioner_data": questioner_data_str
        })
        
        # Extract the content from the result object
        if hasattr(result, 'content'):
            result_text = result.content
        elif isinstance(result, dict) and "text" in result:
            result_text = result["text"]
        else:
            result_text = str(result)
        
        logger.info(f"ICD analysis completed for scenario")
        logger.info(f"Raw response: {result_text}")
        
        # Parse the result to extract codes and explanation
        codes_line = ""
        explanation_line = ""
        
        # More robust parsing of the response - looking for the updated format
        lines = result_text.strip().split('\n')
        in_explanation = False
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            # Check for code line with our new format (uppercase without dashes)
            if line.upper().startswith("CODES:"):
                codes_line = line.split(":", 1)[1].strip()
            
            # Check for explanation line (now uppercase without dash)
            elif line.upper().startswith("EXPLANATION:"):
                in_explanation = True
                explanation_line = line.split(":", 1)[1].strip()
            # Continue collecting explanation text if we're in the explanation section
            elif in_explanation:
                # Skip empty lines
                if line:
                    explanation_line += " " + line
        
        # Clean up the codes
        cleaned_codes = []
        if codes_line:
            # Remove any enclosing brackets from the entire string
            codes_line = codes_line.strip('[]')
            
            # Split by comma
            for code in codes_line.split(','):
                # Clean each code and remove any square brackets around individual codes
                clean_code = code.strip().strip('[]')
                if clean_code and clean_code.lower() != 'none':
                    cleaned_codes.append(clean_code)
        
        # If explanation is still empty, try to extract it using other patterns
        if not explanation_line:
            # First look for any explicit explanation section
            started = False
            collected = []
            
            for line in lines:
                if line.upper().startswith("EXPLANATION:") or line.upper().startswith("REASONING:") or line.upper().startswith("RATIONALE:"):
                    started = True
                    collected.append(line.split(":", 1)[1].strip())
                elif started and line.strip():
                    collected.append(line.strip())
                elif started and not line.strip() and len(collected) > 0:
                    # Empty line after we've started collecting - end of section
                    break
            
            if collected:
                explanation_line = " ".join(collected)
            
            # If still empty, use everything after the codes as explanation
            if not explanation_line and codes_line:
                codes_index = result_text.find("CODES:")
                if codes_index > -1:
                    remainder = result_text[codes_index:].split('\n', 1)
                    if len(remainder) > 1:
                        rest = remainder[1].strip()
                        # Check for explanation header in the rest
                        if "EXPLANATION:" in rest.upper():
                            explanation_line = rest.split("EXPLANATION:", 1)[1].strip()
                        else:
                            explanation_line = rest
        
        # Log the extracted components
        logger.info(f"Extracted ICD codes: {cleaned_codes}")
        logger.info(f"Extracted explanation: {explanation_line}")
        
        return {
            "codes": cleaned_codes,
            "explanation": explanation_line
        }
    except Exception as e:
        logger.error(f"Error in analyze_icd_scenario: {str(e)}")
        return {
            "error": str(e),
            "output": f"CODES: none\nEXPLANATION: Error occurred: {str(e)}",
            "codes": [],
            "explanation": f"Error occurred: {str(e)}",
            "type": "error",
            "data_source": "error"
        } 