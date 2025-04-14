"""
Module for extracting dental prophylaxis codes.
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from subtopics.prompt.prompt import PROMPT
from llm_services import create_chain, invoke_chain, get_llm_service, set_model_for_file

# Load environment variables
load_dotenv()

# Get model name from environment variable, default to gpt-4o if not set
 
def create_dental_prophylaxis_extractor(temperature=0.0):
    """
    Create a LangChain-based dental prophylaxis code extractor.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro-exp-03-25", temperature=temperature)
    
    prompt_template = PromptTemplate(
        template=f"""
You are a highly experienced dental coding expert

Before picking a code, ask:
- What was the primary reason the patient came in? Was it for a routine cleaning, or to address a specific issue like pain or sensitivity?
- What is the patient’s age and dentition status? Are they in permanent/transitional dentition (adult) or primary/transitional dentition (child)?
- Are there any additional factors like heavy calculus buildup, staining, or medical conditions that might affect the procedure?
- Is this a standalone prophylaxis, or is it paired with other diagnostic/treatment codes?
- Does the patient have implants or other restorations that need consideration during the cleaning?

---

### Preventive Dental Codes: Dental Prophylaxis

#### Code: D1110 - Prophylaxis — Adult
- **When to use:**
  - For patients with permanent or transitional dentition (typically 13 years and older).
  - Routine cleaning to remove plaque, calculus, and stains as part of preventive care.
  - Patient presents for a scheduled maintenance visit without specific complaints.
- **What to check:**
  - Confirm the patient’s age and dentition status (permanent/transitional, not primary).
  - Assess the presence of plaque, calculus, and extrinsic stains on teeth and implants.
  - Evaluate oral health history for conditions like gingivitis or periodontal disease that might require a different code (e.g., D4346 or D4910).
  - Perform a basic oral exam to ensure no acute issues are present.
- **Notes:**
  - This code is for routine maintenance, not therapeutic treatment. If the patient has active periodontal disease, consider other codes.
  - Includes polishing and removal of local irritants; does not cover extensive scaling (use D4341/D4342 if applicable).
  - Can be used even if minor issues are found, as long as the primary intent was preventive cleaning.
  - Documentation should include the condition of the teeth/implants and the tools used (e.g., ultrasonic scaler, hand instruments).

#### Code: D1120 - Prophylaxis — Child
- **When to use:**
  - For patients with primary or transitional dentition (typically under 13 years old).
  - Routine cleaning to remove plaque, calculus, and stains as part of preventive care.
  - Patient presents for a scheduled pediatric maintenance visit without specific complaints.
- **What to check:**
  - Verify the patient’s age and dentition status (primary/transitional, not fully permanent).
  - Inspect for plaque, calculus, and stains on primary teeth, transitional teeth, or implants (if present).
  - Review the child’s dental and medical history for factors like caries risk or developmental issues.
  - Ensure the procedure aligns with pediatric preventive goals (e.g., fluoride application may follow but is coded separately).
- **Notes:**
  - This code is specific to younger patients with developing dentition; switch to D1110 once permanent dentition dominates.
  - Focus is on controlling local irritants; extensive treatment (e.g., for caries or gingivitis) requires different codes.
  - Parental education on oral hygiene may be part of the visit but isn’t billable under this code.
  - Documentation should note the dentition stage and any findings like early staining or minimal calculus.

---

### Key Takeaways:
- *Age and Dentition Matter:* D1110 is for adults with permanent/transitional teeth, while D1120 is for kids with primary/transitional teeth.
- *Routine vs. Therapeutic:* Prophylaxis codes are for preventive cleanings, not treatment of active disease—choose wisely based on intent.
- *Scope Over Volume:* Even if the cleaning takes extra time due to staining or calculus, stick to the prophylaxis code unless scaling/root planing is performed.
- *Patient History:* Review medical/dental history to avoid miscoding if underlying conditions (e.g., diabetes, periodontal issues) complicate the visit.
- *Documentation is Key:* Clearly note the patient’s dentition, findings, and procedure details to justify the code if audited.




Scenario:
"{{question}}"

{PROMPT}
""",
        input_variables=["question"]
    )
    
    return LLMChain(llm=llm, prompt=prompt_template)

def extract_dental_prophylaxis_code(scenario, temperature=0.0):
    """
    Extract dental prophylaxis code(s) for a given scenario.
    """
    try:
        chain = create_dental_prophylaxis_extractor(temperature)
        result = invoke_chain(chain, {"question": scenario})
        print(f"Dental prophylaxis code result: {result}")
        return result.strip()
    except Exception as e:
        print(f"Error in extract_dental_prophylaxis_code: {str(e)}")
        return ""

def activate_dental_prophylaxis(scenario):
    """
    Activate dental prophylaxis analysis and return results.
    """
    try:
        return extract_dental_prophylaxis_code(scenario)
    except Exception as e:
        print(f"Error in activate_dental_prophylaxis: {str(e)}")
        return "" 