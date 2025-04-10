from langchain.prompts import PromptTemplate
from llm_services import create_chain, invoke_chain, get_llm_service
from database import MedicalCodingDB

def Add_code_data(scenario: str, cdt_codes: str) -> str:
    """
    Analyze a dental scenario and determine relevance of provided CDT codes.
    """
    prompt_template = PromptTemplate(
        input_variables=["scenario", "cdt_codes"],
        template="""
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
    )

    try:
        llm = get_llm_service()
        chain = create_chain(llm, prompt_template)
        response = invoke_chain(chain, {"scenario": scenario, "cdt_codes": cdt_codes})
        
        # Store the analysis in the database
        db = MedicalCodingDB()
        record_id = db.add_code_analysis(scenario, cdt_codes, response)
        print(f"✅ Analysis stored with ID: {record_id}")
        
        return response

    except Exception as e:
        error_msg = f"Error during analysis: {str(e)}"
        print(f"❌ {error_msg}")
        return error_msg

# Test block
