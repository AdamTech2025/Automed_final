import os
import sys
from langchain.prompts import PromptTemplate
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(parent_dir)
from llm_services import create_chain, invoke_chain, get_llm_service, set_model_for_file
from subtopics.prompt.prompt import PROMPT



def create_pulp_capping_extractor():
    """
    Create a LangChain-based Pulp Capping code extractor.
    """
    prompt_template = f"""
You are a highly experienced dental coding expert 

 Before picking a code, ask:
- What was the primary reason the patient came in?
- Was it for a general check-up, or to address a specific concern?
- Is the treatment intended to preserve the pulp or remove infected tissue?
- Is the pulp exposed, nearly exposed, or has deep decay?
- Is the procedure direct or indirect?

---

### **Endodontic Procedure Codes**

#### **D3110 - Pulp Cap — Direct (excluding final restoration)**
**Use when:** The pulp is exposed, and a protective dressing is applied directly over it to promote healing.  
**Check:** Ensure the material used is biocompatible and supports dentin bridge formation.  
**Note:** This is NOT a final restoration; a separate restorative procedure will be required.

#### **D3120 - Pulp Cap — Indirect (excluding final restoration)**
**Use when:** The pulp is nearly exposed, and a protective dressing is applied to protect it from further injury.  
**Check:** Confirm that all caries have been removed before placing the protective material.  
**Note:** This code is NOT to be used for bases and liners when all decay has been removed.

---

### **Key Takeaways:**
- **Direct vs. Indirect:** Direct pulp caps are used when the pulp is actually exposed; indirect pulp caps are used when the pulp is nearly exposed but still covered by dentin.
- **Final Restoration:** These procedures do not include final restorative work; a separate code should be used for the restoration.
- **Caries Removal:** Ensure all decay has been properly removed before applying an indirect pulp cap.
- **Documentation:** Clearly document pulp exposure status and materials used to support appropriate billing and case tracking.

### **Scenario:**
"{{scenario}}"

{PROMPT}
"""
    
    prompt = PromptTemplate(template=prompt_template, input_variables=["scenario"])
    return create_chain(prompt)

def extract_pulp_capping_code(scenario):
    """
    Extract Pulp Capping code(s) for a given scenario.
    """
    try:
        extractor = create_pulp_capping_extractor()
        result = invoke_chain(extractor, {"scenario": scenario})
        return result.get("text", "").strip()
    except Exception as e:
        print(f"Error in pulp capping code extraction: {str(e)}")
        return None

def activate_pulp_capping(scenario):
    """
    Activate Pulp Capping analysis and return results.
    """
    try:
        result = extract_pulp_capping_code(scenario)
        return result
    except Exception as e:
        print(f"Error activating pulp capping analysis: {str(e)}")
        return None

# Example usage
if __name__ == "__main__":
    # Print the current Gemini model and temperature being used
    llm_service = get_llm_service()
    print(f"Using Gemini model: {llm_service.gemini_model} with temperature: {llm_service.temperature}")
    
    scenario = "During a restoration of a deep cavity on tooth #30, the dentist accidentally exposes the pulp. The dentist immediately applies calcium hydroxide directly to the exposed pulp to promote healing before placing the final restoration."
    result = activate_pulp_capping(scenario)
    print(result) 