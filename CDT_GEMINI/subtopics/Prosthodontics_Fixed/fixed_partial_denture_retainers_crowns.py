"""
Module for extracting fixed partial denture retainers - crowns codes.
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
 
def create_fixed_partial_denture_retainers_crowns_extractor(temperature=0.0):
    """
    Create a LangChain-based fixed partial denture retainers - crowns code extractor.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro-exp-03-25", temperature=temperature)
    
    prompt_template = PromptTemplate(
        template=f"""
You are a highly experienced dental coding expert
### Before picking a code, ask:
- What was the primary reason the patient came in? Was it to replace a missing tooth with a fixed partial denture or to address a specific issue with an existing retainer crown?
- What material is being used for the retainer crown (e.g., resin, porcelain, metal, or a combination)?
- Is the procedure for a permanent restoration, or is it an interim solution requiring further treatment?
- What type of metal (if any) is involved—high noble, noble, predominantly base, titanium, or none?
- Does the patient have any allergies, aesthetic preferences, or functional concerns that influence material choice?

#### Code: D6710  
**Heading:** Retainer crown – indirect resin-based composite  
**When to Use:**  
- Used for fixed prosthodontic retainers made from indirect resin composite materials.  
- Selected when esthetics and cost are prioritized over longevity and durability.  
**What to Check:**  
- Ensure the restoration is **not** being used as a provisional or temporary prosthesis.  
- Confirm the patient has no contraindications to resin-based materials (e.g., bruxism).  
**Notes:**  
- Not intended as a temporary restoration.  
- Longevity may be less than metal or porcelain-based options.

---

#### Code: D6720  
**Heading:** Retainer crown – resin with high noble metal  
**When to Use:**  
- Use when the prosthodontic retainer is constructed with resin over a **high noble metal** substructure.  
- Common in cases where esthetics are secondary to strength and biocompatibility.  
**What to Check:**  
- Ensure documentation includes alloy content (must meet ADA definition of “high noble metal”).  
- Confirm retention needs and substructure support.  
**Notes:**  
- Offers high strength and excellent fit due to high noble content.  

---

#### Code: D6721  
**Heading:** Retainer crown – resin with predominantly base metal  
**When to Use:**  
- For crowns using resin veneering over a **predominantly base metal** core.  
- Economical alternative with reasonable strength.  
**What to Check:**  
- Identify the alloy type used; verify it meets base metal standards.  
- Evaluate esthetic zones where metal discoloration could be a concern.  
**Notes:**  
- May be less biocompatible or prone to corrosion over time than noble metals.

---

#### Code: D6722  
**Heading:** Retainer crown – resin with noble metal  
**When to Use:**  
- Applied when using a resin veneer over a **noble metal** alloy base.  
- Mid-range option offering a balance of strength, esthetics, and cost.  
**What to Check:**  
- Document noble metal content and any resin material types used.  
- Review margin integrity and occlusal stress.  
**Notes:**  
- Not as durable as full metal or porcelain fused restorations.

---

#### Code: D6740  
**Heading:** Retainer crown – porcelain/ceramic  
**When to Use:**  
- For retainers where esthetics are the **primary** concern (e.g., anterior FPD).  
- Suitable when metal-free restorations are requested or needed.  
**What to Check:**  
- Assess occlusion—ceramic crowns can be brittle under high force.  
- Check esthetic needs and alignment.  
**Notes:**  
- Offers superior esthetics; may be contraindicated in heavy occlusion areas.

---

#### Code: D6750  
**Heading:** Retainer crown – porcelain fused to high noble metal  
**When to Use:**  
- Best for fixed bridges requiring esthetics and strength.  
- The gold alloy base provides excellent fit and longevity.  
**What to Check:**  
- Verify high noble metal content (e.g., gold >60%).  
- Ensure the patient doesn't require a full-metal or all-ceramic alternative.  
**Notes:**  
- Gold alloy base minimizes corrosion and improves tissue response.

---

#### Code: D6751  
**Heading:** Retainer crown – porcelain fused to predominantly base metal  
**When to Use:**  
- For retainers in less visible areas where cost is a concern.  
- Combines strength of base metal with porcelain esthetics.  
**What to Check:**  
- Ensure base metal usage is documented (nickel-chromium, cobalt-chromium, etc.).  
**Notes:**  
- May show more wear on opposing dentition compared to ceramic.

---

#### Code: D6752  
**Heading:** Retainer crown – porcelain fused to noble metal  
**When to Use:**  
- Middle-ground option for esthetics and durability.  
- Less expensive than high noble, better longevity than base metal.  
**What to Check:**  
- Confirm noble metal content (~25%–60%).  
- Evaluate tissue biocompatibility and restoration site.  
**Notes:**  
- Good esthetic and functional compromise.

---

#### Code: D6753  
**Heading:** Retainer crown – porcelain fused to titanium and titanium alloys  
**When to Use:**  
- Often used in patients with metal allergies or implant-related prosthetics.  
**What to Check:**  
- Confirm titanium compatibility with adjacent materials and soft tissue.  
**Notes:**  
- Excellent biocompatibility; slightly lower esthetic translucency.

---

#### Code: D6780  
**Heading:** Retainer crown – ¾ cast high noble metal  
**When to Use:**  
- Chosen when full coverage is not needed; ideal for preserving tooth structure.  
**What to Check:**  
- Evaluate remaining tooth structure and ability to bond partial coverage crown.  
**Notes:**  
- Requires precise prep; not recommended for high caries risk.

---

#### Code: D6781  
**Heading:** Retainer crown – ¾ cast predominantly base metal  
**When to Use:**  
- For cost-sensitive cases where full crown isn't needed.  
**What to Check:**  
- Ensure adequate prep and that patient understands limitations in longevity and esthetics.  
**Notes:**  
- Strength is acceptable but esthetics and long-term performance may vary.

---

#### Code: D6782  
**Heading:** Retainer crown – ¾ cast noble metal  
**When to Use:**  
- Moderate-cost option between high noble and base metal.  
**What to Check:**  
- Confirm metal composition and margin fit.  
**Notes:**  
- Less esthetic due to visible metal.

---

#### Code: D6783  
**Heading:** Retainer crown – ¾ porcelain/ceramic  
**When to Use:**  
- For patients needing partial esthetic coverage in anterior or premolar areas.  
**What to Check:**  
- Ensure prep design and occlusal forces are compatible with ceramic.  
**Notes:**  
- Preserves more tooth structure but fragile under bruxing forces.

---

#### Code: D6784  
**Heading:** Retainer crown – ¾ titanium and titanium alloys  
**When to Use:**  
- Typically used in implant-retained restorations or patients with sensitivities.  
**What to Check:**  
- Titanium selection must align with the clinical setting (e.g., implant platforms).  
**Notes:**  
- Highly biocompatible; esthetic limitations exist.

---

#### Code: D6790  
**Heading:** Retainer crown – full cast high noble metal  
**When to Use:**  
- Ideal for posterior fixed bridges needing maximum durability.  
**What to Check:**  
- Ensure patient is okay with lack of esthetics (visible gold).  
**Notes:**  
- Gold standard for strength and marginal seal.

---

#### Code: D6791  
**Heading:** Retainer crown – full cast predominantly base metal  
**When to Use:**  
- Used when strength is needed and esthetics are not a concern.  
**What to Check:**  
- Base metal type and allergy considerations.  
**Notes:**  
- Cost-effective but may lead to tissue sensitivity over time.

---

#### Code: D6792  
**Heading:** Retainer crown – full cast noble metal  
**When to Use:**  
- Solid crown for functional areas with moderate cost sensitivity.  
**What to Check:**  
- Document noble metal percentage.  
**Notes:**  
- Compromise between full cast gold and cheaper base metal crowns.

---

#### Code: D6793  
**Heading:** Provisional retainer crown – further treatment or diagnosis pending  
**When to Use:**  
- Temporarily placed when more diagnostics or treatment planning is needed.  
**What to Check:**  
- Ensure this is not confused with a routine temporary crown.  
**Notes:**  
- Not to be used as a temporary restoration for final prosthesis waiting period.

---

#### Code: D6794  
**Heading:** Retainer crown – titanium and titanium alloys  
**When to Use:**  
- Used especially in patients with metal sensitivities or implant scenarios.  
**What to Check:**  
- Verify compatibility with implant components if relevant.  
**Notes:**  
- Superior tissue response; not esthetically ideal in visible zones.

### Key Takeaways:
- **Material Matters:** Match the crown material to patient needs—durability (metals), aesthetics (porcelain), or biocompatibility (titanium).
- **Full vs. Partial Coverage:** Use 3/4 crowns to preserve tooth structure when possible; full crowns for maximum strength.
- **Permanent vs. Interim:** Reserve D6793 for temporary solutions; all others are permanent restorations.
- **Patient Preferences:** Discuss aesthetics, cost, and longevity to align code choice with patient expectations.
- **Post-Placement Checks:** Always verify occlusion, fit, and patient comfort after seating any retainer crown.

Scenario:
"{{question}}"

{PROMPT}
""",
        input_variables=["question"]
    )
    
    return LLMChain(llm=llm, prompt=prompt_template)

def extract_fixed_partial_denture_retainers_crowns_code(scenario, temperature=0.0):
    """
    Extract fixed partial denture retainers - crowns code(s) for a given scenario.
    """
    try:
        chain = create_fixed_partial_denture_retainers_crowns_extractor(temperature)
        result = invoke_chain(chain, {"question": scenario})
        print(f"Fixed partial denture retainers - crowns code result: {result}")
        return result.strip()
    except Exception as e:
        print(f"Error in extract_fixed_partial_denture_retainers_crowns_code: {str(e)}")
        return ""

def activate_fixed_partial_denture_retainers_crowns(scenario):
    """
    Activate fixed partial denture retainers - crowns analysis and return results.
    """
    try:
        return extract_fixed_partial_denture_retainers_crowns_code(scenario)
    except Exception as e:
        print(f"Error in activate_fixed_partial_denture_retainers_crowns: {str(e)}")
        return ""

# Example usage
if __name__ == "__main__":
    scenario = "Patient needs a three-unit bridge to replace a missing molar. The abutment teeth will need full cast crown retainers made from high noble metal."
    result = activate_fixed_partial_denture_retainers_crowns(scenario)
    print(result) 