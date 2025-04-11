import os
import sys
import logging
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from llm_services import create_chain, invoke_chain, set_model_for_file

# Load environment variables
load_dotenv()

# Set a specific model for this file (optional)
set_model_for_file("gemini-2.5-pro-preview-03-25")

def setup_logging():
    """Configure logging for the inspector module."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]
    )
    return logging.getLogger(__name__)

logger = setup_logging()

def create_dental_inspector(temperature=0.0):
    """
    Create a dental code inspector chain.
    """
    prompt_template = PromptTemplate(
        template="""
You are the final code selector ("Inspector") with extensive expertise in dental coding. Your task is to perform a thorough analysis of the provided scenario along with the candidate CDT code outputs—including all explanations and doubts—from previous subtopics. Your final output must include only the CDT code(s) that are justified by the scenario, with minimal assumptions.

Scenario:
{scenario}

Topic Analysis Results:
{topic_analysis}

Additional Information from Questions (if any):
{questioner_data}

Instructions:

1) Carefully read the complete clinical scenario provided.

2) Review all candidate CDT codes suggested by previous subtopics along with their explanations and any doubts raised.

3) Use Provided Codes: Only consider and select from the candidate CDT codes that were actually analyzed in the topic analysis results. Do not reject codes that weren't part of the original analysis.

4) Reasonable Assumptions: You may make basic clinical assumptions that are standard in dental practice, but avoid making significant assumptions about unstated procedures.

5) Justification: Select codes that are reasonably supported by the scenario. If a code has minor doubts but is likely correct based on the context, include it.

6) Mutually Exclusive Codes: When presented with mutually exclusive codes, choose the one that is best justified for the specific visit. Do not bill for the same procedure twice.

7) Revenue & Defensibility: Your selection should maximize revenue while ensuring billing is defensible, but don't reject codes unnecessarily.

8) Consider Additional QA: Incorporate any additional information or clarifications provided through the question-answer process.

9) Output the same code multiple times if it is applicable (e.g., 8 scans would include the code 8 times).

10) Coding Rules:
    - Consider standard bundling rules but don't be overly strict
    - Assume medical necessity for standard procedures
    - Consider emergency/post-op status if implied by context
    - Only reject codes that were explicitly analyzed in the topic analysis

IMPORTANT: You must format your response exactly as follows:

EXPLANATION: [provide a detailed explanation for why each code was selected or rejected. Include specific reasoning for each code mentioned in the topic analysis.]

CODES: [comma-separated list of CDT codes that are accepted, with no square brackets around individual codes]

REJECTED CODES: [comma-separated list of CDT codes that were considered but rejected, with no square brackets around individual codes. Only list codes that were actually analyzed in the topic analysis and are explicitly contradicted by the scenario.]

For example:

EXPLANATION: D0120 (periodic oral evaluation) is appropriate as this was a regular dental visit. D0274 (bitewings-four radiographs) is included because the scenario mentions taking four bitewing x-rays. D1110 (prophylaxis-adult) is included as the scenario describes cleaning of teeth for an adult patient. D0140 was rejected because this was not an emergency visit.
CODES: D0120, D0274, D1110
REJECTED CODES: D0140,D0220,D0230
""",
        input_variables=["scenario", "topic_analysis", "questioner_data"]
    )
    
    return create_chain(prompt_template)

def analyze_dental_scenario(scenario, topic_analysis, questioner_data=None):
    try:
        chain = create_dental_inspector(temperature=0.0)
        
        # Use scenario directly - it's already the cleaned data
        processed_scenario = scenario
        
        # Convert topic_analysis to string if it's a dictionary
        if topic_analysis is None:
            topic_analysis_str = "No CDT data analysis data available in DB"
        elif isinstance(topic_analysis, dict):
            # If the data is coming from the database dental_report table
            formatted_topics = []
            for code_range, topic_data in topic_analysis.items():
                # Format each topic's data in a readable way
                topic_name = topic_data.get("name", "Unknown")
                topic_result = topic_data.get("result", "No result")
                formatted_topics.append(f"{topic_name} ({code_range}): {topic_result}")
            
            topic_analysis_str = "\n".join(formatted_topics)
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
        
        logger.info(f"Dental analysis completed for scenario")
        logger.info(f"Raw response: {result_text}")
        
        # Parse the result to extract codes and explanation
        codes_line = ""
        explanation_line = ""
        rejected_codes_line = ""
        
        # More robust parsing of the response - looking for the updated format
        lines = result_text.strip().split('\n')
        in_explanation = False
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            # Check for code line with our new format (uppercase without dashes)
            if line.upper().startswith("CODES:"):
                codes_line = line.split(":", 1)[1].strip()
            
            # Check for rejected codes line
            elif line.upper().startswith("REJECTED CODES:"):
                rejected_codes_line = line.split(":", 1)[1].strip()
            
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
        
        # Clean up the rejected codes
        rejected_codes = []
        if rejected_codes_line:
            # Remove any enclosing brackets from the entire string
            rejected_codes_line = rejected_codes_line.strip('[]')
            
            # Split by comma
            for code in rejected_codes_line.split(','):
                # Clean each code and remove any square brackets around individual codes
                clean_code = code.strip().strip('[]')
                # Don't include wildcards or "none" in rejected codes
                if clean_code and clean_code.lower() != 'none' and '*' not in clean_code:
                    rejected_codes.append(clean_code)
        
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
        logger.info(f"Extracted codes: {cleaned_codes}")
        logger.info(f"Extracted rejected codes: {rejected_codes}")
        logger.info(f"Extracted explanation: {explanation_line}")
        
        return {
            "codes": cleaned_codes,
            "rejected_codes": rejected_codes,
            "explanation": explanation_line
        }
    except Exception as e:
        logger.error(f"Error in analyze_dental_scenario: {str(e)}")
        return {
            "error": str(e),
            "output": f"- CODES: none\n- EXPLAINATION: Error occurred: {str(e)}",
            "codes": [],
            "rejected_codes": [],
            "explanation": f"Error occurred: {str(e)}",
            "type": "error",
            "data_source": "error"
        }


# def inspect(target, topic_analysis=None):

#     logger.info(f"Inspecting: {target}")
    
#     results = {
#         "type": type(target).__name__,
#         "size": sys.getsizeof(target),
#     }
    
#     # If target is a string, attempt to analyze it as a dental scenario
#     if isinstance(target, str) and len(target) > 10:
#         dental_analysis = analyze_dental_scenario(target, topic_analysis)
#         results.update({"dental_analysis": dental_analysis})
    
#     return results





