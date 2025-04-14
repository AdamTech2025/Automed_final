"""
Module for extracting maxillofacial prosthetics carriers codes.
"""

import os
import sys
from langchain.prompts import PromptTemplate
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(parent_dir)
from llm_services import create_chain, invoke_chain, get_llm_service, set_model_for_file
from subtopics.prompt.prompt import PROMPT



def create_carriers_extractor():
    """
    Creates a LangChain-based extractor for maxillofacial prosthetics carriers codes.
    """
    template = f"""
You are a dental coding expert 
### **Before picking a code, ask:**
- What was the primary reason the patient came in?
- Is the prosthesis designed for fluoride application, medicament delivery, or radiation therapy?
- Is the device custom-fabricated and laboratory-processed?
- What is the specific function and duration of the prosthesis?
- Does the patient have a condition that requires sustained medicament contact or radiation therapy?

## **Maxillofacial Prosthetics Codes**

### **Code: D5986**  
**Heading:** Fluoride Gel Carrier  
**Use when:** The patient requires a prosthesis to apply fluoride for caries prevention or treatment.  
**Check:** Ensure proper fit and coverage of the dental arch for effective fluoride application.  
**Note:** This device helps in the daily administration of fluoride and is typically recommended for high-risk caries patients.

---

### **Code: D5995**  
**Heading:** Periodontal Medicament Carrier with Peripheral Seal – Maxillary  
**Use when:** The patient requires a custom-fabricated carrier for delivering prescribed periodontal medication to the maxillary arch.  
**Check:** Ensure peripheral seal integrity and proper adaptation for sustained contact with gingiva and periodontal pockets.  
**Note:** This carrier aids in the prolonged application of medicaments to enhance periodontal therapy outcomes.

---

### **Code: D5996**  
**Heading:** Periodontal Medicament Carrier with Peripheral Seal – Mandibular  
**Use when:** The patient requires a mandibular prosthesis for the controlled delivery of periodontal medication.  
**Check:** Confirm coverage of teeth and alveolar mucosa, and verify retention.  
**Note:** Used in cases where sustained medicament exposure is essential for treating periodontal conditions.

---

### **Code: D5983**  
**Heading:** Radiation Carrier  
**Use when:** The patient is undergoing localized radiation therapy requiring a secure prosthesis for radiation source placement.  
**Check:** Ensure the prosthesis holds radiation-emitting materials (e.g., radium, cesium) in a stable position.  
**Note:** Commonly used in coordination with oncologists for precise radiation application.

---

### **Code: D5991**  
**Heading:** Vesiculobullous Disease Medicament Carrier  
**Use when:** The patient requires a prosthesis for applying prescription medications to manage vesiculobullous diseases.  
**Check:** Ensure proper adaptation to the oral mucosa for effective medicament delivery.  
**Note:** Typically used for conditions such as pemphigus or mucous membrane pemphigoid.

---

### **Code: D5999**  
**Heading:** Unspecified Maxillofacial Prosthesis, By Report  
**Use when:** The procedure does not fit within an existing maxillofacial prosthetic code.  
**Check:** Provide a detailed report on the prosthesis type, function, and medical necessity.  
**Note:** This code requires documentation to justify the unique procedure performed.

---

### **Key Takeaways:**
- **Custom Fabrication:** Many of these prostheses require laboratory processing for precise adaptation.  
- **Targeted Application:** Each prosthesis serves a specific therapeutic purpose, such as fluoride application, periodontal treatment, or radiation therapy.  
- **Patient-Specific Design:** Ensure the device fits well and meets the treatment goals.  
- **Documentation is Critical:** Certain codes require detailed reports for proper reimbursement and justification.  
- **Collaboration:** Work closely with periodontists, oncologists, and prosthodontists to ensure optimal treatment outcomes.



Scenario:
"{{scenario}}"

{PROMPT}
"""
    
    prompt = PromptTemplate(template=template, input_variables=["scenario"])
    return create_chain(prompt)

def extract_carriers_code(scenario):
    """
    Extracts maxillofacial prosthetics carriers code(s) for a given scenario.
    """
    try:
        extractor = create_carriers_extractor()
        result = invoke_chain(extractor, {"scenario": scenario})
        return result.get("text", "").strip()
    except Exception as e:
        print(f"Error in carriers code extraction: {str(e)}")
        return None

def activate_carriers(scenario):
    """
    Analyze a dental scenario to determine maxillofacial prosthetics carriers code.
    
    Args:
        scenario (str): The dental scenario to analyze.
        
    Returns:
        str: The identified maxillofacial prosthetics carriers code or empty string if none found.
    """
    try:
        result = extract_carriers_code(scenario)
        
        # Return empty string if no code found
        if result == "None" or not result or "not applicable" in result.lower():
            return ""
            
        return result
    except Exception as e:
        print(f"Error in activate_carriers: {str(e)}")
        return ""

# Example usage
if __name__ == "__main__":
    # Print the current Gemini model and temperature being used
    llm_service = get_llm_service()
    print(f"Using Gemini model: {llm_service.gemini_model} with temperature: {llm_service.temperature}")
    
    scenario = "A 45-year-old patient with advanced periodontal disease requires a custom-fabricated device to deliver prescribed antibiotics to the periodontal pockets in the lower jaw. The dentist plans to create a mandibular carrier with peripheral seal to ensure medication stays in place and effectively treats the condition."
    result = activate_carriers(scenario)
    print(result) 