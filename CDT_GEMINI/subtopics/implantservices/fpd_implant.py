"""
Module for extracting fixed partial denture retainer, implant supported codes.
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

def create_fpd_implant_extractor():
    """
    Creates a LangChain-based extractor for fixed partial denture retainer, implant supported codes.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro-exp-03-25", temperature=0.0)    
    template = f"""
    You are a dental coding expert specializing in implant services.
    
  ## **Fixed Partial Denture (FPD) Retainer, Implant Supported** 
 
### **Before picking a code, ask:** 
- What material is the FPD retainer made of? (porcelain/ceramic, metal, porcelain-fused-to-metal, etc.)
- If it's porcelain-fused-to-metal, what type of metal is used? (high noble, predominantly base, noble, titanium)
- Is the retainer being attached directly to the implant without an abutment?
- Is this retainer part of a fixed partial denture spanning multiple teeth?
- What is the location of the implant in the mouth?
- Are there special considerations for material selection based on esthetics or functional requirements?
 
---
 
### **Porcelain/Ceramic Option**
 
#### **Code: D6075** – *Implant supported retainer for ceramic FPD* 
**Use when:** A ceramic retainer for a fixed partial denture is being placed directly on an implant without an intermediate abutment.
**Check:** Verify the retainer is fully made of porcelain/ceramic material with no metal substructure.
**Note:** Offers excellent esthetics for anterior regions. May be less durable than metal or PFM options for high-stress areas.
 
---
 
### **Porcelain Fused to Metal (PFM) Options**
 
#### **Code: D6076** – *Implant supported retainer for FPD — porcelain fused to high noble alloys* 
**Use when:** Placing a porcelain-fused-to-metal retainer directly on an implant with a high noble metal substructure.
**Check:** Confirm the metal used contains ≥60% noble metal, with ≥40% gold.
**Note:** High noble metals provide excellent biocompatibility and durability with good bond strength to porcelain.
 
#### **Code: D6098** – *Implant supported retainer — porcelain fused to predominantly base alloys* 
**Use when:** Placing a porcelain-fused-to-metal retainer directly on an implant with a predominantly base metal substructure.
**Check:** Ensure the metal contains <25% noble metal.
**Note:** More economical option that may be suitable where cost is a primary concern.
 
#### **Code: D6099** – *Implant supported retainer for FPD — porcelain fused to noble alloys* 
**Use when:** Placing a porcelain-fused-to-metal retainer directly on an implant with a noble metal substructure.
**Check:** Verify the metal contains ≥25% noble metal.
**Note:** Provides a balance between cost and biocompatibility for a FPD retainer.
 
#### **Code: D6120** – *Implant supported retainer — porcelain fused to titanium and titanium alloys* 
**Use when:** Placing a porcelain-fused-to-titanium retainer directly on an implant.
**Check:** Confirm the substructure is specifically titanium or a titanium alloy.
**Note:** Titanium offers excellent biocompatibility and strength, making it ideal for patients with metal sensitivities.
 
---
 
### **Full Metal Options**
 
#### **Code: D6077** – *Implant supported retainer for metal FPD — high noble alloys* 
**Use when:** Placing a full metal retainer made of high noble alloys directly on an implant.
**Check:** Verify the metal contains ≥60% noble metal, with ≥40% gold.
**Note:** These retainers are excellent for posterior regions where strength and durability are paramount.
 
#### **Code: D6121** – *Implant supported retainer for metal FPD — predominantly base alloys* 
**Use when:** Placing a full metal retainer made of predominantly base alloys directly on an implant.
**Check:** Confirm the metal contains <25% noble metal.
**Note:** More economical option that still provides good strength for posterior FPD retainers.
 
#### **Code: D6122** – *Implant supported retainer for metal FPD — noble alloys* 
**Use when:** Placing a full metal retainer made of noble alloys directly on an implant.
**Check:** Ensure the metal contains ≥25% noble metal.
**Note:** Provides a balance of cost, durability, and biocompatibility.
 
#### **Code: D6123** – *Implant supported retainer for metal FPD — titanium and titanium alloys* 
**Use when:** Placing a full titanium retainer directly on an implant.
**Check:** Verify the retainer is made entirely of titanium or titanium alloy.
**Note:** Excellent option for patients with metal allergies or where maximum biocompatibility is required.
 
---
 
### **Key Takeaways:** 
- These codes are specifically for **retainers** that are part of a fixed partial denture (bridge) attached **directly to implants** without intermediate abutments.
- For retainers attached to abutments on implants, use the abutment-supported retainer codes (D6068-D6074, D6194, D6195) instead.
- The retainer is the component that attaches to the implant and provides support for the pontic(s).
- Material selection is the primary differentiating factor between these codes.
- The codes are categorized by both the visible material (porcelain/ceramic vs. metal) and the type of metal used.
- Documentation should specify the exact materials used and clarify that this is part of a fixed partial denture.
- Confirm that the restoration is specifically an implant-supported retainer, not an abutment-supported retainer.
    
    SCENARIO: {{scenario}}
    
    {PROMPT}
    """
    
    prompt = PromptTemplate(template=template, input_variables=["scenario"])
    return LLMChain(llm=llm, prompt=prompt)

def extract_fpd_implant_code(scenario):
    """
    Extracts fixed partial denture retainer, implant supported code(s) for a given scenario.
    """
    try:
        extractor = create_fpd_implant_extractor()
        result = extractor.invoke({"scenario": scenario}).get("text", "").strip()
        return result
    except Exception as e:
        print(f"Error in FPD implant code extraction: {str(e)}")
        return None

def activate_fpd_implant(scenario):
    """
    Analyze a dental scenario to determine fixed partial denture retainer, implant supported code.
    
    Args:
        scenario (str): The dental scenario to analyze.
        
    Returns:
        str: The identified fixed partial denture retainer, implant supported code or empty string if none found.
    """
    try:
        result = extract_fpd_implant_code(scenario)
        
        # Return empty string if no code found
        if result == "None" or not result or "not applicable" in result.lower():
            return ""
            
        return result
    except Exception as e:
        print(f"Error in activate_fpd_implant: {str(e)}")
        return "" 