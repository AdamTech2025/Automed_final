from langchain.prompts import PromptTemplate
from llm_services import generate_response, get_service, set_model, set_temperature
from database import MedicalCodingDB
from typing import Dict, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def Add_code_data(scenario: str, cdt_codes: str) -> str:
    """
    Analyze a dental scenario and determine relevance of provided CDT codes.
    """
    # Prepare the prompt template
    template = """
You are a dental coding assistant trained in analyzing clinical scenarios and determining the relevance of CDT (Current Dental Terminology) codes.

Your task is to:
1. Interpret the SCENARIO based on clinical context.
2. For each provided CDT code, explain whether it is justified or not based on the scenario.
3. Be medically accurate and grounded in CDT definitions. Do NOT guess or fabricate explanations.

---

### SCENARIO:
{scenario}

### CDT CODES:
{cdt_codes}

---

### RESPONSE FORMAT:
For each CDT code, provide:
- CDT Code: [code]
  - **Applicable?** Yes / No
  - **Reason**: [Explain why it's relevant or not based on the scenario]

Do NOT suggest a specific code unless you're sure the procedure matches exactly.
Do NOT go beyond what is clinically supported.

Always stay concise, clear, and clinically grounded.
"""

    try:
        # Format the prompt with the input values
        formatted_prompt = template.format(scenario=scenario, cdt_codes=cdt_codes)
        
        # Generate response using the LLM service
        response_text = generate_response(formatted_prompt)
        
        # Store the analysis in the database
        db = MedicalCodingDB()
        record_id = db.add_code_analysis(scenario, cdt_codes, response_text)
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
    result = Add_code_data(test_scenario, test_code)
    print(result)
