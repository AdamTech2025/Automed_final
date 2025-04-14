"""
Module for extracting crown codes.
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
 
def create_crowns_extractor(temperature=0.0):
    """
    Create a LangChain-based crowns code extractor.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro-exp-03-25", temperature=temperature)
    
    prompt_template = PromptTemplate(
        template=f"""
    You are a highly experienced dental coding expert

Before picking a code, ask:**
- What was the primary reason the patient came in?
- Was it for a general check-up, or to address a specific concern?
- What type of restoration is being placed?
- Is the restoration a full crown or partial (3/4 crown)?
- What material is being used—resin, metal, porcelain, or a combination?
- Is the restoration temporary or definitive?

---

### **Crown – Single Restorations Only**

#### **D2710 – Crown, resin-based composite (indirect)**
**Use when:** A full-coverage indirect resin-based composite crown is placed.  
**Check:** Ensure proper occlusion, marginal fit, and shade match.  
**Note:** Not commonly used due to durability concerns compared to other materials.

#### **D2712 – Crown, 3/4 resin-based composite (indirect)**
**Use when:** A three-quarter indirect resin-based composite crown is needed.  
**Check:** Confirm retention and bonding strength.  
**Note:** This procedure does not include facial veneers.

#### **D2720 – Crown, resin with high noble metal**
**Use when:** A full-coverage resin crown with high noble metal support is required.  
**Check:** Ensure metal substructure provides adequate strength.  
**Note:** Offers esthetic benefits but may wear faster than porcelain alternatives.

#### **D2721 – Crown, resin with predominantly base metal**
**Use when:** A resin crown with a base metal substructure is needed.  
**Check:** Verify adequate retention and compatibility with adjacent restorations.  
**Note:** Less expensive than high noble alternatives but may have esthetic drawbacks.

#### **D2722 – Crown, resin with noble metal**
**Use when:** A resin crown with a noble metal substructure is required.  
**Check:** Ensure proper fit and margin adaptation.  
**Note:** Offers a balance between strength and esthetics.

#### **D2740 – Crown, porcelain/ceramic**
**Use when:** A full-coverage porcelain or ceramic crown is needed for esthetics.  
**Check:** Verify shade match and marginal adaptation.  
**Note:** Ideal for anterior teeth due to superior esthetics.

#### **D2750 – Crown, porcelain fused to high noble metal**
**Use when:** A strong and esthetic restoration is required.  
**Check:** Ensure porcelain bonding to metal substructure is intact.  
**Note:** Commonly used for both anterior and posterior restorations.

#### **D2751 – Crown, porcelain fused to predominantly base metal**
**Use when:** A cost-effective porcelain-fused metal crown is needed.  
**Check:** Confirm adequate porcelain coverage and metal framework adaptation.  
**Note:** Stronger than all-ceramic but may have esthetic limitations.

#### **D2752 – Crown, porcelain fused to noble metal**
**Use when:** A porcelain-fused crown with improved metal quality is required.  
**Check:** Ensure compatibility with adjacent restorations and occlusion.  
**Note:** Balances durability and esthetics.

#### **D2753 – Crown, porcelain fused to titanium and titanium alloys**
**Use when:** A titanium-based crown is needed for biocompatibility.  
**Check:** Confirm proper bonding of porcelain to titanium.  
**Note:** Suitable for patients with metal allergies.

#### **D2780 – Crown, 3/4 cast high noble metal**
**Use when:** A three-quarter crown with high noble metal is needed.  
**Check:** Verify retention and fit.  
**Note:** Provides durability while preserving tooth structure.

#### **D2781 – Crown, 3/4 cast predominantly base metal**
**Use when:** A more affordable 3/4 metal crown is required.  
**Check:** Ensure functional occlusion and marginal integrity.  
**Note:** Less esthetic due to metal visibility.

#### **D2782 – Crown, 3/4 cast noble metal**
**Use when:** A balance between strength and conservation of tooth structure is needed.  
**Check:** Ensure long-term retention and occlusion.  
**Note:** More esthetic than base metal alternatives.

#### **D2783 – Crown, 3/4 porcelain/ceramic**
**Use when:** A three-quarter porcelain or ceramic crown is required for esthetics.  
**Check:** Verify shade match and minimal preparation.  
**Note:** Does not include facial veneers.

#### **D2790 – Crown, full cast high noble metal**
**Use when:** A full-coverage high noble metal crown is needed for durability.  
**Check:** Ensure long-term occlusal stability.  
**Note:** Common for posterior teeth where esthetics is less of a concern.

#### **D2791 – Crown, full cast predominantly base metal**
**Use when:** A cost-effective full metal crown is needed.  
**Check:** Confirm adaptation and occlusal harmony.  
**Note:** Extremely durable but lacks esthetic appeal.

#### **D2792 – Crown, full cast noble metal**
**Use when:** A full metal crown with noble metal composition is required.  
**Check:** Verify retention, fit, and occlusion.  
**Note:** Provides a balance between cost and durability.

#### **D2794 – Crown, titanium and titanium alloys**
**Use when:** A metal crown with titanium for biocompatibility is needed.  
**Check:** Confirm proper occlusion and adaptability.  
**Note:** Ideal for patients with metal sensitivities.

#### **D2799 – Interim crown**
**Use when:** A temporary crown is needed due to ongoing treatment or diagnostics.  
**Check:** Ensure proper fit and function until final restoration is placed.  
**Note:** Not to be used as a routine temporary crown for prosthetic restorations.

---

### **Key Takeaways:**
- **Material Selection:** Consider strength, esthetics, and cost when choosing between resin, porcelain, or metal crowns.
- **Full vs. 3/4 Crowns:** Three-quarter crowns conserve more tooth structure but require careful preparation.
- **Temporary vs. Permanent:** Ensure interim crowns are used appropriately and not as substitutes for permanent restorations.
- **Esthetic Considerations:** Porcelain and ceramic options are preferred for anterior teeth, while metal crowns offer better longevity for posterior teeth.
- **Proper Fit & Occlusion:** Always verify marginal integrity and occlusal balance to prevent future complications.

---

This document provides a structured approach for selecting the correct restorative crown codes, ensuring accurate treatment planning and billing.





Scenario:
"{{question}}"

{PROMPT}
""",
        input_variables=["question"]
    )
    
    return LLMChain(llm=llm, prompt=prompt_template)

def extract_crowns_code(scenario, temperature=0.0):
    """
    Extract crowns code(s) for a given scenario.
    """
    try:
        chain = create_crowns_extractor(temperature)
        result = invoke_chain(chain, {"scenario": scenario})
        print(f"Crowns code result: {result}")
        return result.strip()
    except Exception as e:
        print(f"Error in extract_crowns_code: {str(e)}")
        return ""

def activate_crowns(scenario):
    """
    Activate crowns analysis and return results.
    """
    try:
        return extract_crowns_code(scenario)
    except Exception as e:
        print(f"Error in activate_crowns: {str(e)}")
        return ""

# Example usage
if __name__ == "__main__":
    scenario = "Patient needs a full porcelain crown on tooth #8 after root canal treatment."
    result = activate_crowns(scenario)
    print(result) 