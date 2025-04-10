import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from subtopics.prompt.prompt import PROMPT


# Get model name from environment variable, default to gpt-4o if not set
MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o")

def create_pulpal_regeneration_extractor(temperature=0.0):
    """
    Create a LangChain-based Pulpal Regeneration code extractor.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.0-flash-thinking-exp-01-21", temperature=temperature)
    
    prompt_template = PromptTemplate(
        template=f"""
You are a highly experienced dental coding expert 


### Before Picking a Code, Ask:
- What was the primary reason the patient came in? Did they present with a specific issue (e.g., trauma, immature tooth with necrotic pulp) requiring pulpal regeneration, or was it identified during an exam?
- Is this the initial visit, an interim medication replacement, or the completion of the regeneration process?
- Does the tooth have an open apex or immature root development necessitating regenerative treatment?
- Are diagnostic tools (e.g., radiographs, pulp vitality tests) confirming the need for pulpal regeneration?
- Is the tooth a candidate for regeneration (e.g., young patient, no extensive damage), or is traditional root canal therapy more appropriate?

---

### Pulpal Regeneration

#### Code: D3355
**Heading:** Pulpal regeneration — initial visit  
**Description:** Includes opening tooth, preparation of canal spaces, placement of medication.  
**When to Use:**  
- The patient has a permanent tooth with an immature apex and necrotic pulp (often due to trauma or caries), requiring the start of regenerative endodontic treatment.  
- The procedure involves accessing the tooth, cleaning canal spaces, and placing medication (e.g., antibiotic paste) to stimulate regeneration.  
- Use for the first visit of a multi-step pulpal regeneration process.  
**What to Check:**  
- Confirm the tooth is permanent with an open apex via radiograph (e.g., wide canal, thin walls).  
- Assess pulp status (e.g., necrotic but not fully infected beyond regeneration potential).  
- Check patient age (typically younger patients, e.g., 6-18) and tooth condition for regeneration viability.  
- Verify no contraindications (e.g., severe root damage, patient allergies to medications).  
**Notes:**  
- This is the initial step only—subsequent visits use D3356 or D3357 as needed.  
- Requires detailed documentation (e.g., X-rays, clinical findings) for insurance due to specialized nature.  
- Not for mature teeth or standard root canal therapy (see D3310-D3330).  

#### Code: D3356
**Heading:** Pulpal regeneration — interim medication replacement  
**When to Use:**  
- The patient returns for a follow-up visit after the initial pulpal regeneration (D3355) to replace or adjust intracanal medication.  
- Involves removing old medication, irrigating the canal, and placing new medication to promote continued regeneration.  
- Use for interim visits between the initial and final stages of treatment.  
**What to Check:**  
- Confirm prior D3355 was performed and the tooth remains a candidate for regeneration.  
- Assess canal condition (e.g., signs of healing, no persistent infection) via exam or radiograph.  
- Check patient symptoms (e.g., reduced pain, no swelling) and response to initial treatment.  
- Verify the need for additional medication rather than completion (D3357).  
**Notes:**  
- May be used multiple times if several interim visits are required—document each instance.  
- Not a standalone code—must follow D3355 and precede D3357 in the regeneration sequence.  
- Narrative may be needed to explain the number of interim visits for insurance approval.  

#### Code: D3357
**Heading:** Pulpal regeneration — completion of treatment  
**Description:** Does not include final restoration.  
**When to Use:**  
- The patient has completed the regenerative process, and the final visit seals the canal with a biocompatible material (e.g., MTA) to encourage root development.  
- Use when the pulpal regeneration treatment concludes, confirming apex closure or dentin thickening.  
- Applied after initial (D3355) and any interim (D3356) visits.  
**What to Check:**  
- Confirm prior D3355 and D3356 (if applicable) were performed and regeneration goals are met.  
- Assess radiographic evidence of root maturation (e.g., apex closure, wall thickening).  
- Check for resolution of symptoms and absence of infection or inflammation.  
- Verify the tooth’s stability and readiness for final restoration (coded separately).  
**Notes:**  
- Excludes final restoration—use separate codes (e.g., D2950, D2750) for core buildup or crown.  
- Requires pre- and post-treatment X-rays and a narrative for insurance to document success.  
- Not for incomplete treatments or cases requiring extraction.  

---

### Key Takeaways:
- **Multi-Step Process:** D3355 (initial), D3356 (interim), and D3357 (completion) reflect distinct stages—use them sequentially.  
- **Immature Teeth Only:** Pulpal regeneration targets permanent teeth with open apices, not mature roots.  
- **Regeneration vs. Therapy:** These codes differ from standard root canal codes (D3310-D3330) by aiming to regenerate tissue.  
- **Restoration Separate:** Final restorations are not included—code them independently.  
- **Documentation Critical:** Insurance often requires detailed records (e.g., X-rays, medication used) due to the procedure’s complexity.



### **Scenario:**
"{{question}}"

{PROMPT}
""",
        input_variables=["question"]
    )
    
    return LLMChain(llm=llm, prompt=prompt_template)

def extract_pulpal_regeneration_code(scenario, temperature=0.0):
    """
    Extract Pulpal Regeneration code(s) for a given scenario.
    """
    chain = create_pulpal_regeneration_extractor(temperature)
    return chain.run(question=scenario).strip()

def activate_pulpal_regeneration(scenario):
    """
    Activate Pulpal Regeneration analysis and return results.
    """
    return extract_pulpal_regeneration_code(scenario) 