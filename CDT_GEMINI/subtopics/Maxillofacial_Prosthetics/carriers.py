"""
Module for extracting maxillofacial prosthetics carriers codes.
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from subtopics.prompt.prompt import PROMPT


# Load environment variables
load_dotenv()

# Get model name from environment variable, default to gpt-4o if not set
MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o")

def activate_carriers(scenario):
    """
    Analyze a dental scenario to determine maxillofacial prosthetics carriers code.
    
    Args:
        scenario (str): The dental scenario to analyze.
        
    Returns:
        str: The identified maxillofacial prosthetics carriers code or empty string if none found.
    """
    try:
        llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro-exp-03-25", temperature=0.0)        
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
        chain = LLMChain(llm=llm, prompt=prompt)
        
        result = chain.run(scenario=scenario).strip()
        
        # Return empty string if no code found
        if result == "None" or not result or "not applicable" in result.lower():
            return ""
            
        return result
    except Exception as e:
        print(f"Error in activate_carriers: {str(e)}")
        return "" 