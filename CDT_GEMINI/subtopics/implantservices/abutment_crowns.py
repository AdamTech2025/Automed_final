"""
Module for extracting single crowns, abutment supported codes.
"""

import os
import sys
from langchain.prompts import PromptTemplate
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(parent_dir)
from llm_services import create_chain, invoke_chain, get_llm_service, set_model_for_file
from subtopics.prompt.prompt import PROMPT



def create_abutment_crowns_extractor():
    """
    Creates a LangChain-based extractor for abutment supported crown codes.
    """
    template = f"""
    You are a dental coding expert specializing in implant services.
    
  ## **Single Crowns, Abutment Supported** 
 
### **Before picking a code, ask:** 
- What material is the crown made of? (porcelain/ceramic, metal, porcelain-fused-to-metal, etc.)
- If it's porcelain-fused-to-metal, what type of metal is used? (high noble, predominantly base, noble metal, titanium)
- Is the crown being attached to an abutment on an implant?
- Is this a single crown restoration or part of a multi-unit structure?
- What is the location of the implant in the mouth?
- Are there any special considerations for material selection based on esthetics or functional requirements?
 
---
 
### **Porcelain/Ceramic Options**
 
#### **Code: D6058** – *Abutment supported porcelain/ceramic crown* 
**Use when:** A single all-ceramic or all-porcelain crown is being placed on an implant abutment.
**Check:** Verify the crown is fully made of porcelain/ceramic material with no metal substructure.
**Note:** Ideal for anterior teeth where esthetics are a primary concern. These restorations provide excellent translucency and natural appearance.
 
---
 
### **Porcelain Fused to Metal (PFM) Options**
 
#### **Code: D6059** – *Abutment supported porcelain fused to metal crown (high noble metal)* 
**Use when:** Placing a porcelain-fused-to-metal crown on an implant abutment with a high noble metal substructure.
**Check:** Confirm the metal used contains ≥60% noble metal, with ≥40% gold.
**Note:** High noble metals provide excellent biocompatibility, minimal corrosion, and good bond strength to porcelain.
 
#### **Code: D6060** – *Abutment supported porcelain fused to metal crown (predominantly base metal)* 
**Use when:** Placing a porcelain-fused-to-metal crown on an implant abutment with a predominantly base metal substructure.
**Check:** Ensure the metal used contains <25% noble metal.
**Note:** Base metal options are generally more affordable but may have less biocompatibility in some patients.
 
#### **Code: D6061** – *Abutment supported porcelain fused to metal crown (noble metal)* 
**Use when:** Placing a porcelain-fused-to-metal crown on an implant abutment with a noble metal substructure.
**Check:** Verify the metal used contains ≥25% noble metal.
**Note:** Noble metals provide a balance between cost and biocompatibility, making them a good middle option.
 
#### **Code: D6097** – *Abutment supported crown — porcelain fused to titanium or titanium alloys* 
**Use when:** Placing a porcelain-fused-to-titanium crown on an implant abutment.
**Check:** Confirm the substructure is specifically titanium or a titanium alloy.
**Note:** Titanium offers excellent biocompatibility, strength, and lightweight properties, making it ideal for patients with metal sensitivities.
 
---
 
### **Full Metal Options**
 
#### **Code: D6062** – *Abutment supported cast metal crown (high noble metal)* 
**Use when:** Placing a full cast metal crown made of high noble metal on an implant abutment.
**Check:** Verify the metal contains ≥60% noble metal, with ≥40% gold.
**Note:** These crowns are excellent for posterior teeth where esthetics is less critical but strength and durability are paramount.
 
#### **Code: D6063** – *Abutment supported cast metal crown (predominantly base metal)* 
**Use when:** Placing a full cast metal crown made of predominantly base metal on an implant abutment.
**Check:** Confirm the metal contains <25% noble metal.
**Note:** More economical option that still provides good strength for posterior restorations.
 
#### **Code: D6064** – *Abutment supported cast metal crown (noble metal)* 
**Use when:** Placing a full cast metal crown made of noble metal on an implant abutment.
**Check:** Ensure the metal contains ≥25% noble metal.
**Note:** Provides a balance of cost, durability, and biocompatibility for posterior restorations.
 
#### **Code: D6094** – *Abutment supported crown (titanium)* 
**Use when:** Placing a full titanium crown on an implant abutment.
**Check:** Verify the crown is made entirely of titanium or titanium alloy.
**Note:** Excellent option for patients with metal allergies, offering superior strength-to-weight ratio and biocompatibility.
 
---
 
### **Key Takeaways:** 
- All of these codes are specifically for **single** crown restorations placed on implant abutments.
- Material selection is the primary differentiating factor between these codes.
- The codes are categorized by both the visible material (porcelain/ceramic vs. metal) and the type of metal used.
- Documentation should specify the exact materials used to support the selected code.
- Consider both functional needs (strength, durability) and esthetic requirements when selecting materials.
- Verify that the restoration is specifically for an abutment-supported crown, not a cement-retained or screw-retained restoration.
    
    SCENARIO: {{scenario}}
    
    {PROMPT}
    """
    
    prompt = PromptTemplate(template=template, input_variables=["scenario"])
    return create_chain(prompt)

def extract_abutment_crowns_code(scenario):
    """
    Extracts abutment supported crown code(s) for a given scenario.
    """
    try:
        extractor = create_abutment_crowns_extractor()
        result = invoke_chain(extractor, {"scenario": scenario})
        return result.get("text", "").strip()
    except Exception as e:
        print(f"Error in abutment crowns code extraction: {str(e)}")
        return None

def activate_single_crowns_abutment(scenario):
    """
    Analyze a dental scenario to determine single crowns, abutment supported code.
    
    Args:
        scenario (str): The dental scenario to analyze.
        
    Returns:
        str: The identified single crowns, abutment supported code or empty string if none found.
    """
    try:
        result = extract_abutment_crowns_code(scenario)
        
        # Return empty string if no code found
        if result == "None" or not result or "not applicable" in result.lower():
            return ""
            
        return result
    except Exception as e:
        print(f"Error in activate_single_crowns_abutment: {str(e)}")
        return ""

# Example usage
if __name__ == "__main__":
    # Print the current Gemini model and temperature being used
    llm_service = get_llm_service()
    print(f"Using Gemini model: {llm_service.gemini_model} with temperature: {llm_service.temperature}")
    
    scenario = "A patient with an implant at position #8 (upper right central incisor) requires a crown. The dentist plans to place an all-ceramic crown on the custom abutment that was previously placed on the implant."
    result = activate_single_crowns_abutment(scenario)
    print(result) 