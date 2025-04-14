import os
import sys
from langchain.prompts import PromptTemplate
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(parent_dir)
from llm_services import create_chain, invoke_chain, get_llm_service, set_model_for_file    
from subtopics.prompt.prompt import PROMPT



def create_professional_visits_extractor():
    """
    Creates a LangChain-based extractor for professional visits codes.
    """
    template = f"""
    You are a dental coding expert
    ### **Before picking a code, ask:**  
- Is the visit occurring outside of the dentist's office, such as in a hospital, nursing home, or extended care facility?  
- Is the visit for consultation, observation, or active treatment?  
- Did the visit occur during or outside of regular office hours?  
- Was the visit part of a scheduled case presentation for extensive treatment planning?  
- Are there additional services provided during the visit that need separate coding?  

---

### **Detailed Coding Guidelines for Professional Visits**  

#### **Code: D9410** – *House/Extended Care Facility Call*  
**Use when:** A dentist provides care at a non-office location, such as a nursing home, long-term care facility, hospice, or institution.  
**Check:** Ensure that the visit is necessary due to patient limitations preventing travel to a dental office.  
**Note:** This code is reported in addition to specific procedures performed during the visit.  

#### **Code: D9420** – *Hospital or Ambulatory Surgical Center Call*  
**Use when:** A dentist treats a patient in a hospital or surgical center rather than the dental office.  
**Check:** Confirm that the patient is admitted or receiving care in a hospital or ambulatory setting.  
**Note:** Any services provided during the visit should be coded separately in addition to this call code.  

#### **Code: D9430** – *Office Visit for Observation (During Regularly Scheduled Hours) - No Other Services Performed*  
**Use when:** A patient visits the office for observation, but no active treatment or procedures are performed.  
**Check:** Ensure that the visit is strictly for monitoring or follow-up without any additional dental procedures.  
**Note:** If treatment is rendered, use the appropriate procedural code instead.  

#### **Code: D9440** – *Office Visit - After Regularly Scheduled Hours*  
**Use when:** A dentist sees a patient outside of normal business hours.  
**Check:** Confirm that the visit is necessary and conducted outside of standard office hours, such as evenings, weekends, or emergencies.  
**Note:** This code is used in addition to any treatment provided during the after-hours visit.  

#### **Code: D9450** – *Case Presentation, Subsequent to Detailed and Extensive Treatment Planning*  
**Use when:** A dentist presents a detailed treatment plan to the patient, involving complex or multiple procedures.  
**Check:** Ensure that the treatment plan is comprehensive, requiring an in-depth consultation beyond routine discussions.  
**Note:** Typically applies to extensive restorative, prosthodontic, or surgical treatment plans.  

---

### **Key Takeaways:**  
- **D9410 & D9420** cover professional visits outside of the dental office and must be used in addition to any services provided.  
- **D9430 & D9440** are for office visits without treatment, differentiating between regular and after-hours visits.  
- **D9450** is specifically for case presentations related to detailed and extensive treatment plans.  
- **Ensure proper documentation** of the visit's necessity, setting, and whether additional procedures were performed.  


    SCENARIO: {{scenario}}
    
    {PROMPT}
    """
    
    prompt = PromptTemplate(template=template, input_variables=["scenario"])
    return create_chain(prompt)

def extract_professional_visits_code(scenario):
    """
    Extracts professional visits code(s) for a given scenario.
    """
    try:
        extractor = create_professional_visits_extractor()
        result = invoke_chain(extractor, {"scenario": scenario})
        return result.get("text", "").strip()
    except Exception as e:
        print(f"Error in professional visits code extraction: {str(e)}")
        return None

def activate_professional_visits(scenario):
    """
    Activates the professional visits analysis process and returns results.
    """
    try:
        result = extract_professional_visits_code(scenario)
        return result
    except Exception as e:
        print(f"Error activating professional visits analysis: {str(e)}")
        return None

# Example usage
if __name__ == "__main__":
    # Print the current Gemini model and temperature being used
    llm_service = get_llm_service()
    print(f"Using Gemini model: {llm_service.gemini_model} with temperature: {llm_service.temperature}")
    
    scenario = "Dentist visits nursing home resident to provide dental examination. No treatment was performed during this visit."
    result = activate_professional_visits(scenario)
    print(result) 