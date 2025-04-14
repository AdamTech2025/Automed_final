import os
import sys
from langchain.prompts import PromptTemplate
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(parent_dir)
from llm_services import create_chain, invoke_chain, get_llm_service, set_model_for_file
from subtopics.prompt.prompt import PROMPT



def create_pulpotomy_extractor():
    """
    Create a LangChain-based Pulpotomy code extractor.
    """
    prompt_template = f"""
You are a highly experienced dental coding expert

### Before picking a code, ask:
- What was the primary reason the patient came in?
- Is the procedure being performed on a primary or permanent tooth?
- Is this a therapeutic procedure or preparatory for root canal therapy?
- Does the patient have incomplete root development?
- Is this an emergency procedure for pain relief?

---

### Pulpotomy Codes

**Code: D3220**  
**Heading:** Therapeutic pulpotomy (excluding final restoration) — removal of pulp coronal to the dentinocemental junction and application of medicament  
**Use when:** The procedure involves the surgical removal of a portion of the pulp with the aim of maintaining the vitality of the remaining portion using an adequate dressing.  
**Check:** Ensure that the procedure is performed on either primary or permanent teeth, but NOT as the first stage of root canal therapy. Not for apexogenesis.  
**Note:** This procedure is not to be used for permanent teeth with incomplete root development; instead, use D3222.

---

**Code: D3221**  
**Heading:** Pulpal debridement, primary and permanent teeth  
**Use when:** The procedure is performed for relief of acute pain before conventional root canal therapy.  
**Check:** Confirm that endodontic treatment is not being completed on the same day. This is an interim procedure meant to manage pain.  
**Note:** Should not be used if root canal therapy is initiated or completed during the same appointment.

---

**Code: D3222**  
**Heading:** Partial pulpotomy for apexogenesis — permanent tooth with incomplete root development  
**Use when:** A portion of the pulp is removed, and medicament is applied to maintain vitality and encourage continued root formation.  
**Check:** Ensure that the procedure is performed only on permanent teeth with incomplete root development.  
**Note:** This procedure is not considered the first stage of root canal therapy.

---

### Key Takeaways:
- **Primary vs. Permanent:** Ensure that the correct code is chosen based on whether the tooth is primary or permanent.
- **Therapeutic vs. Preparatory:** Pulpotomy is a standalone therapeutic treatment, whereas pulpal debridement (D3221) is used for temporary pain relief before further endodontic treatment.
- **Apexogenesis Considerations:** If the tooth has incomplete root development, D3222 is the appropriate code, not D3220.
- **Pain Management:** Use D3221 for acute pain relief before conventional root canal therapy, but ensure treatment is not completed the same day.
- **Long-Term Planning:** Consider the patient's overall treatment plan and select the code that best matches their stage of care.



### **Scenario:**
"{{scenario}}"

{PROMPT}
"""
    
    prompt = PromptTemplate(template=prompt_template, input_variables=["scenario"])
    return create_chain(prompt)

def extract_pulpotomy_code(scenario):
    """
    Extract Pulpotomy code(s) for a given scenario.
    """
    try:
        extractor = create_pulpotomy_extractor()
        result = invoke_chain(extractor, {"scenario": scenario})
        return result.get("text", "").strip()
    except Exception as e:
        print(f"Error in pulpotomy code extraction: {str(e)}")
        return None

def activate_pulpotomy(scenario):
    """
    Activate Pulpotomy analysis and return results.
    """
    try:
        result = extract_pulpotomy_code(scenario)
        return result
    except Exception as e:
        print(f"Error activating pulpotomy analysis: {str(e)}")
        return None

# Example usage
if __name__ == "__main__":
    # Print the current Gemini model and temperature being used
    llm_service = get_llm_service()
    print(f"Using Gemini model: {llm_service.gemini_model} with temperature: {llm_service.temperature}")
    
    scenario = "A 6-year-old child comes in with a deep carious lesion on a primary molar. The dentist performs a therapeutic pulpotomy to maintain the vitality of the remaining pulp."
    result = activate_pulpotomy(scenario)
    print(result) 