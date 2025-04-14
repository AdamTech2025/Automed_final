"""
Module for extracting single crowns, implant supported codes.
"""

import os
import sys
from langchain.prompts import PromptTemplate
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(parent_dir)
from llm_services import create_chain, invoke_chain, get_llm_service, set_model_for_file
from subtopics.prompt.prompt import PROMPT



def create_implant_crowns_extractor():
    """
    Creates a LangChain-based extractor for implant supported crown codes.
    """
    template = f"""
    You are a dental coding expert specializing in implant services.
    
  ## **Single Crowns, Implant Supported** 
 
### **Before picking a code, ask:** 
- What material is the crown made of? (porcelain/ceramic, metal, porcelain-fused-to-metal, etc.)
- If it's porcelain-fused-to-metal, what type of metal alloy is used? (high noble, predominantly base, noble, titanium)
- Is the crown being attached directly to the implant (not using an abutment)?
- Is this a single crown restoration or part of a multi-unit prosthesis?
- What is the location of the implant in the mouth?
- Are there special considerations for material selection based on esthetics or functional requirements?
 
---
 
### **Porcelain/Ceramic Option**
 
#### **Code: D6065** – *Implant supported porcelain/ceramic crown* 
**Use when:** A single all-ceramic or all-porcelain crown is being placed directly on an implant without an intermediate abutment.
**Check:** Verify the crown is fully made of porcelain/ceramic material with no metal substructure.
**Note:** Ideal for anterior teeth where esthetics are a primary concern. These restorations provide excellent translucency and natural appearance.
 
---
 
### **Porcelain Fused to Metal (PFM) Options**
 
#### **Code: D6066** – *Implant supported crown — porcelain fused to high noble alloys* 
**Use when:** Placing a porcelain-fused-to-metal crown directly on an implant with a high noble metal substructure.
**Check:** Confirm the metal used contains ≥60% noble metal, with ≥40% gold.
**Note:** High noble metals provide excellent biocompatibility and minimal corrosion, with good bond strength to porcelain.
 
#### **Code: D6082** – *Implant supported crown — porcelain fused to predominantly base alloys* 
**Use when:** Placing a porcelain-fused-to-metal crown directly on an implant with a predominantly base metal substructure.
**Check:** Ensure the metal contains <25% noble metal.
**Note:** More economical option that may be suitable for posterior restorations where esthetics are less critical.
 
#### **Code: D6083** – *Implant supported crown — porcelain fused to noble alloys* 
**Use when:** Placing a porcelain-fused-to-metal crown directly on an implant with a noble metal substructure.
**Check:** Verify the metal contains ≥25% noble metal.
**Note:** Noble metals offer a balance between cost and biocompatibility, making them a good middle option.
 
#### **Code: D6084** – *Implant supported crown — porcelain fused to titanium or titanium alloys* 
**Use when:** Placing a porcelain-fused-to-titanium crown directly on an implant.
**Check:** Confirm the substructure is specifically titanium or a titanium alloy.
**Note:** Titanium offers excellent biocompatibility, strength, and lightweight properties, making it ideal for patients with metal sensitivities.
 
---
 
### **Full Metal Options**
 
#### **Code: D6067** – *Implant supported crown — high noble alloys* 
**Use when:** Placing a full metal crown made of high noble alloys directly on an implant.
**Check:** Verify the metal contains ≥60% noble metal, with ≥40% gold.
**Note:** These crowns are excellent for posterior teeth where esthetics is less critical but strength and durability are paramount.
 
#### **Code: D6086** – *Implant supported crown — predominantly base alloys* 
**Use when:** Placing a full metal crown made of predominantly base alloys directly on an implant.
**Check:** Confirm the metal contains <25% noble metal.
**Note:** More economical option that still provides good strength for posterior restorations.
 
#### **Code: D6087** – *Implant supported crown — noble alloys* 
**Use when:** Placing a full metal crown made of noble alloys directly on an implant.
**Check:** Ensure the metal contains ≥25% noble metal.
**Note:** Provides a balance of cost, durability, and biocompatibility for posterior restorations.
 
#### **Code: D6088** – *Implant supported crown — titanium and titanium alloys* 
**Use when:** Placing a full titanium crown directly on an implant.
**Check:** Verify the crown is made entirely of titanium or titanium alloy.
**Note:** Excellent option for patients with metal allergies, offering superior strength-to-weight ratio and biocompatibility.
 
---
 
### **Key Takeaways:** 
- All of these codes are specifically for **single** crown restorations placed **directly on implants** without an intermediate abutment.
- For crowns placed on abutments, use the abutment-supported crown codes (D6058-D6064, D6094, D6097) instead.
- Material selection is the primary differentiating factor between these codes.
- The codes are categorized by both the visible material (porcelain/ceramic vs. metal) and the type of metal used.
- Documentation should specify the exact materials used to support the selected code.
- Consider both functional needs (strength, durability) and esthetic requirements when selecting materials.
- Verify that the restoration is specifically an implant-supported crown, not an abutment-supported crown.
    
    SCENARIO: {{scenario}}
    
    {PROMPT}
    """
    
    prompt = PromptTemplate(template=template, input_variables=["scenario"])
    return create_chain(prompt)

def extract_implant_crowns_code(scenario):
    """
    Extracts implant supported crown code(s) for a given scenario.
    """
    try:
        extractor = create_implant_crowns_extractor()
        result = invoke_chain(extractor, {"scenario": scenario})
        return result.get("text", "").strip()
    except Exception as e:
        print(f"Error in implant crowns code extraction: {str(e)}")
        return None

def activate_single_crowns_implant(scenario):
    """
    Analyze a dental scenario to determine single crowns, implant supported code.
    
    Args:
        scenario (str): The dental scenario to analyze.
        
    Returns:
        str: The identified single crowns, implant supported code or empty string if none found.
    """
    try:
        result = extract_implant_crowns_code(scenario)
        
        # Return empty string if no code found
        if result == "None" or not result or "not applicable" in result.lower():
            return ""
            
        return result
    except Exception as e:
        print(f"Error in activate_single_crowns_implant: {str(e)}")
        return ""

# Example usage
if __name__ == "__main__":
    # Print the current Gemini model and temperature being used
    llm_service = get_llm_service()
    print(f"Using Gemini model: {llm_service.gemini_model} with temperature: {llm_service.temperature}")
    
    scenario = "A patient with an implant at position #8 (upper right central incisor) requires a new crown. The dentist plans to place an all-ceramic crown directly onto the implant without using an abutment for optimal esthetics."
    result = activate_single_crowns_implant(scenario)
    print(result) 