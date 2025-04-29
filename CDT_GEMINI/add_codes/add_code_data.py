from langchain.prompts import PromptTemplate
from llm_services import generate_response, get_service, set_model, set_temperature
from database import MedicalCodingDB
from typing import Dict, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def Add_code_data(scenario: str, code_to_analyze: str, code_type: str = 'CDT') -> str:
    """
    Analyze a dental scenario and determine relevance of provided CDT codes.
    """
    # Dynamically set the code type label in the prompt
    code_type_label = "CDT CODE" if code_type.upper() == 'CDT' else "ICD CODE"

    # Prepare the prompt template
    template = f"""
You are a dental coding assistant trained in analyzing clinical scenarios and determining the relevance of {code_type.upper()} codes.

Your task is to:
1. Interpret the SCENARIO based on clinical context.
2. For the provided {code_type_label}, explain whether it is justified or not based on the scenario.
3. Be medically accurate and grounded in {code_type.upper()} definitions. Do NOT guess or fabricate explanations.

---

### SCENARIO:
{scenario}

### {code_type_label} TO ANALYZE:
{code_to_analyze}

---

### RESPONSE FORMAT:
{code_type_label}: [code]
- **Applicable?** Yes / No
- **Reason**: [Explain why it's relevant or not based on the scenario]

Do NOT suggest a specific code unless you're sure the procedure matches exactly.
Do NOT go beyond what is clinically supported.

Always stay concise, clear, and clinically grounded.
"""

    try:
        # Format the prompt with the input values
        formatted_prompt = template.format(scenario=scenario, code_to_analyze=code_to_analyze)
        
        # Generate response using the LLM service
        response_text = generate_response(formatted_prompt)
        
        # Store the analysis in the database
        db = MedicalCodingDB()
        # Conditionally pass code to the database based on type
        # Assumes db.add_code_analysis expects cdt_codes primarily
        db_cdt_code = code_to_analyze if code_type.upper() == 'CDT' else None
        record_id = db.add_code_analysis(scenario=scenario, cdt_codes=db_cdt_code, response=response_text)
        logger.info(f"✅ Analysis stored with ID: {record_id}")
        
        return response_text

    except Exception as e:
        error_msg = f"Error during analysis: {str(e)}"
        logger.error(f"❌ {error_msg}")
        return error_msg

# Test block for direct execution
if __name__ == "__main__":
    test_scenario = "Patient came in with pain in tooth #19. Clinical examination revealed deep caries reaching the pulp chamber. Decision was made to perform a root canal treatment followed by core buildup and crown placement."
    test_code = "D3330 - Endodontic therapy, molar (excluding final restoration)"
    # Test with CDT type
    result_cdt = Add_code_data(test_scenario, test_code, code_type='CDT')
    print("--- CDT Test ---")
    print(result_cdt)

    # Test with ICD type (Example)
    test_scenario_icd = "Patient presents with fever and sore throat."
    test_code_icd = "J02.9 - Acute pharyngitis, unspecified"
    result_icd = Add_code_data(test_scenario_icd, test_code_icd, code_type='ICD')
    print("\n--- ICD Test ---")
    print(result_icd)
