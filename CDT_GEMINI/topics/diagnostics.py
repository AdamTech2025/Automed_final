import os
import sys
from langchain.prompts import PromptTemplate
from llm_services import create_chain, invoke_chain, get_llm_service

# Add the root directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)

# Now import modules
from topics.prompt import PROMPT
from subtopics.diagnostics import (
    activate_clinical_oral_evaluations,
    activate_pre_diagnostic_services,
    activate_diagnostic_imaging,
    activate_oral_pathology_laboratory,
    activate_tests_and_laboratory_examinations,
    
)

# Load environment variables

# Get model name from environment variable, default to gpt-4o if not set

# Ensure API key is set
def analyze_diagnostic(scenario):
    """
    Analyze a diagnostic scenario and return relevant code ranges.
    
    Args:
        scenario (str): The dental scenario text to analyze
        
    Returns:
        str: The identified diagnostic code range(s)
    """
    try:
        # Create the prompt template
        prompt_template = PromptTemplate(
            template=f"""
You are a highly experienced dental coding expert with over 15 years of expertise in ADA dental codes. 
Your task is to analyze the given scenario and determine the most applicable diagnostic code range(s) based on the following classifications:


## **Clinical Oral Evaluations (D0120-D0180)**
**Use when:** Providing patient assessment services including routine or comprehensive evaluations.
**Check:** Documentation clearly specifies the type of evaluation performed (periodic, limited, comprehensive).
**Note:** These codes reflect different levels of examination depth and purpose.
**Activation trigger:** Scenario mentions OR implies any patient examination, assessment, evaluation, check-up, or diagnostic appointment. INCLUDE this range if there's any indication of patient evaluation or diagnostic assessment.

## **Pre-diagnostic Services (D0190-D0191)** 
**Use when:** Performing screening or limited assessment prior to comprehensive evaluation.
**Check:** Documentation shows brief assessment was performed to determine need for further care.
**Note:** These are typically preliminary evaluations, not comprehensive assessments.
**Activation trigger:** Scenario mentions OR implies any screening, triage, initial assessment, or preliminary examination. INCLUDE this range if there's any hint of preliminary evaluation before more detailed diagnosis.

## **Diagnostic Imaging (D0210-D0391)**
**Use when:** Capturing any diagnostic images to visualize oral structures.
**Check:** Documentation specifies the type of images obtained and their diagnostic purpose.
**Note:** Different codes apply based on the type, number, and complexity of images.
**Activation trigger:** Scenario mentions OR implies any radiographs, x-rays, imaging, CBCT, photographs, or visualization needs. INCLUDE this range if there's any indication that images were or should be taken for diagnostic purposes.

## **Oral Pathology Laboratory (D0472-D0502)**
**Use when:** Collecting and analyzing tissue samples for diagnostic purposes.
**Check:** Documentation includes details about sample collection and pathology reporting.
**Note:** These codes relate to laboratory examination of tissues, not clinical examination.
**Activation trigger:** Scenario mentions OR implies any biopsy, tissue sample, pathology testing, lesion analysis, or microscopic examination. INCLUDE this range if there's any suggestion of tissue sampling or pathological analysis.

## **Tests and Laboratory Examinations (D0411-D0999)**
**Use when:** Performing specialized diagnostic tests beyond clinical examination.
**Check:** Documentation details the specific test performed and clinical rationale.
**Note:** These include both chairside and laboratory-based diagnostic procedures.
**Activation trigger:** Scenario mentions OR implies any laboratory testing, diagnostic measures, microbial testing, pulp vitality assessment, or specialized diagnostic procedures. INCLUDE this range if there's any hint of diagnostic testing beyond visual examination.

## **Assessment of Patient Outcome Metrics (D4186)**
**Use when:** Evaluating treatment success or collecting quality improvement data.
**Check:** Documentation shows systematic assessment of treatment outcomes or patient satisfaction.
**Note:** This code relates to structured evaluation of care quality and results.
**Activation trigger:** Scenario mentions OR implies any outcome assessment, treatment success evaluation, patient satisfaction measurement, or quality improvement initiative. INCLUDE this range if there's any indication of measuring treatment effectiveness or outcomes.

### **Scenario:**
{{scenario}}
{PROMPT}

RESPOND WITH ALL APPLICABLE CODE RANGES from the options above, even if they are only slightly relevant.
List them in order of relevance, with the most relevant first.
""",
            input_variables=["scenario"]
        )
        
        # Create the chain using our LLM service
        chain = create_chain(prompt_template)
        
        # Use the provided scenario directly
        print(f"Analyzing diagnostic scenario: {scenario[:100]}...")
        
        # Use invoke through our LLM service
        result = invoke_chain(chain, {"scenario": scenario})
        
        # Extract the text from the result
        code_range = result.get("text", "").strip()
        
        print(f"Diagnostic analyze_diagnostic result: {code_range}")
        return code_range
    except Exception as e:
        print(f"Error in analyze_diagnostic: {str(e)}")
        return ""

def activate_diagnostic(scenario):
    """
    Activate diagnostic analysis and return the results with specific subtopic activations.
    
    Args:
        scenario (str): The dental scenario text to analyze
        
    Returns:
        dict: A dictionary containing the code range, subtopic and specific codes
    """
    try:
        # Get the code range from the analysis
        diagnostic_result = analyze_diagnostic(scenario)
        if not diagnostic_result:
            print("No diagnostic result returned")
            return {}
        
        print(f"Diagnostic Result in activate_diagnostic: {diagnostic_result}")
        
        # Process specific diagnostic subtopics based on the result
        specific_codes = []
        activated_subtopics = []
        
        # Check for each subtopic and activate if applicable
        if "D0120-D0180" in diagnostic_result:
            print("Activating subtopic: Clinical Oral Evaluations (D0120-D0180)")
            evaluation_code = activate_clinical_oral_evaluations(scenario)
            if evaluation_code:
                specific_codes.append(evaluation_code)
                activated_subtopics.append("Clinical Oral Evaluations (D0120-D0180)")
                
        if "D0190-D0191" in diagnostic_result:
            print("Activating subtopic: Pre-diagnostic Services (D0190-D0191)")
            pre_diagnostic_code = activate_pre_diagnostic_services(scenario)
            if pre_diagnostic_code:
                specific_codes.append(pre_diagnostic_code)
                activated_subtopics.append("Pre-diagnostic Services (D0190-D0191)")
                
        if "D0210-D0391" in diagnostic_result:
            print("Activating subtopic: Diagnostic Imaging (D0210-D0391)")
            imaging_code = activate_diagnostic_imaging(scenario)
            if imaging_code:
                specific_codes.append(imaging_code)
                activated_subtopics.append("Diagnostic Imaging (D0210-D0391)")
                
        if "D0472-D0502" in diagnostic_result:
            print("Activating subtopic: Oral Pathology Laboratory (D0472-D0502)")
            pathology_code = activate_oral_pathology_laboratory(scenario)
            if pathology_code:
                specific_codes.append(pathology_code)
                activated_subtopics.append("Oral Pathology Laboratory (D0472-D0502)")
                
        if "D0411-D0999" in diagnostic_result:
            print("Activating subtopic: Tests and Laboratory Examinations (D0411-D0999)")
            tests_code = activate_tests_and_laboratory_examinations(scenario)
            if tests_code:
                specific_codes.append(tests_code)
                activated_subtopics.append("Tests and Laboratory Examinations (D0411-D0999)")
                
        
        
        # Choose the primary subtopic (either the first activated or a default)
        primary_subtopic = activated_subtopics[0] if activated_subtopics else "Clinical Oral Evaluations (D0120-D0180)"
        
        # Format detailed results if specific codes were found
        if specific_codes:
            # Return a dictionary with the required fields
            return {
                "code_range": diagnostic_result,
                "subtopic": primary_subtopic,
                "activated_subtopics": activated_subtopics,  # Add this for clarity about which subtopics were activated
                "codes": specific_codes
            }
            
        # Return a dictionary even if no specific codes were found
        return {
            "code_range": diagnostic_result,
            "subtopic": primary_subtopic,
            "activated_subtopics": activated_subtopics,
            "codes": []
        }
    except Exception as e:
        print(f"Error in diagnostic analysis: {str(e)}")
        return {}

# Example usage
if __name__ == "__main__":
    # Print the current Gemini model and temperature being used
    llm_service = get_llm_service()
    print(f"Using Gemini model: {llm_service.gemini_model} with temperature: {llm_service.temperature}")
    
    scenario = input("Enter a diagnostic dental scenario: ")
    result = activate_diagnostic(scenario)
    print(f"\n=== DIAGNOSTIC ANALYSIS RESULT ===")
    print(f"CODE RANGE: {result.get('code_range', 'None')}")
    print(f"PRIMARY SUBTOPIC: {result.get('subtopic', 'None')}")
    print(f"ACTIVATED SUBTOPICS: {', '.join(result.get('activated_subtopics', []))}")
    print(f"SPECIFIC CODES: {', '.join(result.get('codes', []))}")

