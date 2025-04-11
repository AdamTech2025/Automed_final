import os
import logging
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from llm_services import create_chain, invoke_chain, set_model_for_file

# Load environment variables
load_dotenv()

# Set a specific model for this file (optional)
# set_model_for_file("gemini-2.5-pro-preview-03-25")

def setup_logging():
    """Configure logging for the questioner module."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]
    )
    return logging.getLogger(__name__)

logger = setup_logging()

def create_questioner(temperature=0.0):
    """
    Create a questioner chain for both CDT and ICD.
    """
    prompt_template = PromptTemplate(
        template="""
You are a highly experienced dental and medical coding expert with over 15 years of expertise in ADA dental procedure codes and ICD-10 diagnostic codes. Your task is to review the provided dental scenario along with the CDT and ICD analysis results to determine if any critical information is missing that is necessary for accurately assigning codes.

Scenario:
{scenario}

CDT Analysis Results:
{cdt_analysis}

ICD Analysis Results:
{icd_analysis}

Instructions:

1. Only ask questions that would directly impact the code selection. Do not ask questions that can be reasonably inferred from the scenario or that won't change the code selection.

2. For CDT codes, focus on:
   - Whether the patient is new or established (impacts evaluation codes)
   - The extent of the cavity (number of surfaces involved)
   - Whether radiographs were taken and what type
   - Only ask about treatment details if treatment was performed

IMPORTANT TASK TO FOLLOW: 
- Analyse only the cdt_analysis and icd_analysis ask questions only from the output you get from the file.
- Mostly try not to ask any questions, if basic assumptions solve the problem, do not ask questions.

4. If the scenario provides sufficient information for accurate coding, do not ask any questions.

Return your response in this exact format:
CDT_QUESTIONS: [List only the most critical CDT-specific questions that would impact code selection, one per line, or "None" if no questions are needed]
CDT_EXPLANATION: [Briefly explain why these specific CDT questions are necessary for code selection]
ICD_QUESTIONS: [List only the most critical ICD-specific questions that would impact code selection, one per line, or "None" if no questions are needed]
ICD_EXPLANATION: [Briefly explain why these specific ICD questions are necessary for code selection]
""",
        input_variables=["scenario", "cdt_analysis", "icd_analysis"]
    )
    
    return create_chain(prompt_template)

def process_questioner(scenario, cdt_analysis=None, icd_analysis=None):
    """
    Process the scenario and generate questions for both CDT and ICD if needed.
    """
    try:
        chain = create_questioner()
        
        # Convert analyses to string if they're dictionaries
        cdt_analysis_str = "\n".join([
            f"{key}: {value}" for key, value in cdt_analysis.items()
        ]) if isinstance(cdt_analysis, dict) else str(cdt_analysis)
        
        icd_analysis_str = "\n".join([
            f"{key}: {value}" for key, value in icd_analysis.items()
        ]) if isinstance(icd_analysis, dict) else str(icd_analysis)
        
        result = invoke_chain(chain, {
            "scenario": scenario,
            "cdt_analysis": cdt_analysis_str,
            "icd_analysis": icd_analysis_str
        })
        
        # Extract the content from the result object
        if hasattr(result, 'content'):
            result_text = result.content
        elif isinstance(result, dict) and "text" in result:
            result_text = result["text"]
        else:
            result_text = str(result)
        
        # Parse the results
        cdt_questions = []
        cdt_explanation = ""
        icd_questions = []
        icd_explanation = ""
        
        current_section = None
        for line in result_text.strip().split('\n'):
            if line.startswith("CDT_QUESTIONS:"):
                current_section = "cdt_questions"
                continue
            elif line.startswith("CDT_EXPLANATION:"):
                current_section = "cdt_explanation"
                continue
            elif line.startswith("ICD_QUESTIONS:"):
                current_section = "icd_questions"
                continue
            elif line.startswith("ICD_EXPLANATION:"):
                current_section = "icd_explanation"
                continue
            
            if current_section == "cdt_questions" and line.strip():
                if line.strip().lower() != "none":
                    cdt_questions.append(line.strip())
            elif current_section == "cdt_explanation" and line.strip():
                cdt_explanation = line.strip()
            elif current_section == "icd_questions" and line.strip():
                if line.strip().lower() != "none":
                    icd_questions.append(line.strip())
            elif current_section == "icd_explanation" and line.strip():
                icd_explanation = line.strip()
        
        return {
            "cdt_questions": {
                "questions": cdt_questions,
                "explanation": cdt_explanation,
                "has_questions": len(cdt_questions) > 0
            },
            "icd_questions": {
                "questions": icd_questions,
                "explanation": icd_explanation,
                "has_questions": len(icd_questions) > 0
            },
            "has_questions": len(cdt_questions) > 0 or len(icd_questions) > 0
        }
    
    except Exception as e:
        logger.error(f"Error in process_questioner: {str(e)}")
        return {
            "cdt_questions": {
                "questions": [],
                "explanation": f"Error occurred: {str(e)}",
                "has_questions": False
            },
            "icd_questions": {
                "questions": [],
                "explanation": f"Error occurred: {str(e)}",
                "has_questions": False
            },
            "has_questions": False
        } 