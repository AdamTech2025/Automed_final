"""
Module for extracting pre-surgical implant services codes.
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from subtopics.prompt.prompt import PROMPT


# Load environment variables
try:
    load_dotenv()
except:
    pass

# Get model name from environment variable, default to gpt-4o if not set
MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o")

def create_pre_surgical_extractor():
    """
    Creates a LangChain-based extractor for pre-surgical implant services codes.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-flash-8b", temperature=0.0)    
    template = f"""
    You are a dental coding expert specializing in implant services.
    
  ## **Pre-Surgical Implant Services** 
 
### **Before picking a code, ask:** 
- Is a radiographic/surgical implant index being created for treatment planning or implant placement?
- What is the purpose of the index in the overall treatment plan?
- Will the index be used during radiographic exposure, treatment planning, or during the surgical procedure?
- Does the index relate osteotomy or fixture position to existing anatomic structures?
- Is this creating a guide for a single implant or multiple implants?
- Will this index be used for both diagnosis and surgical guidance?
 
---
 
### **Pre-Surgical Planning**
 
#### **Code: D6190** – *Radiographic/surgical implant index, by report* 
**Use when:** Creating a specialized appliance designed to relate osteotomy or fixture position to existing anatomic structures during pre-surgical planning and implant placement.
**Check:** Verify that documentation includes details about how the index was created and will be used during the surgical procedure or radiographic assessment.
**Note:** This specialized appliance serves as a precise guide for implant placement, ensuring optimal positioning relative to critical anatomical structures such as the inferior alveolar nerve, maxillary sinus, and adjacent teeth, while also accounting for prosthetic considerations by incorporating information about the final prosthesis design to achieve ideal functional and esthetic outcomes.
**Documentation Requirements:** A detailed narrative report must accompany this code, specifying the type of index created (radiographic, surgical, or dual-purpose), materials used, method of fabrication, anatomic structures referenced, number of implants planned, and how the index will be utilized during treatment planning and/or surgical phases.
**Clinical Indications:** This procedure is particularly valuable for complex cases involving multiple implants, compromised bone volume, proximity to vital anatomical structures, or when precise angulation is critical for prosthetic success, as it significantly reduces risks of surgical complications while enhancing treatment predictability.
 
---
 
### **Key Takeaways:** 
- The radiographic/surgical implant index (D6190) is a critical tool for enhancing precision and reducing risk during implant placement.
- This code requires a detailed narrative report explaining the purpose and creation of the index.
- The index serves both diagnostic and surgical guidance functions, relating implant positions to critical anatomical structures.
- This procedure is distinct from standard treatment planning or radiographic assessment, as it involves the fabrication of a specialized appliance.
- Modern digital planning with CBCT integration and 3D-printed surgical guides would typically fall under this code category.
- The index may be used during multiple phases of treatment, from initial planning through final implant placement.
- The complexity of the case and anatomical considerations should be well-documented to support the necessity of this procedure.
    
    SCENARIO: {{scenario}}
    
    {PROMPT}
    """
    
    prompt = PromptTemplate(template=template, input_variables=["scenario"])
    return LLMChain(llm=llm, prompt=prompt)

def extract_pre_surgical_code(scenario):
    """
    Extracts pre-surgical implant services code(s) for a given scenario.
    """
    try:
        extractor = create_pre_surgical_extractor()
        result = extractor.invoke({"scenario": scenario}).get("text", "").strip()
        return result
    except Exception as e:
        print(f"Error in pre-surgical code extraction: {str(e)}")
        return None

def activate_pre_surgical(scenario):
    """
    Analyze a dental scenario to determine pre-surgical implant services code.
    
    Args:
        scenario (str): The dental scenario to analyze.
        
    Returns:
        str: The identified pre-surgical code or empty string if none found.
    """
    try:
        result = extract_pre_surgical_code(scenario)
        
        # Return empty string if no code found
        if result == "None" or not result or "not applicable" in result.lower():
            return ""
            
        return result
    except Exception as e:
        print(f"Error in activate_pre_surgical: {str(e)}")
        return "" 