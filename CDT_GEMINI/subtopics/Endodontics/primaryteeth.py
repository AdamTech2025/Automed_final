import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from subtopics.prompt.prompt import PROMPT


# Get model name from environment variable, default to gpt-4o if not set
MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o")

def create_primary_teeth_therapy_extractor(temperature=0.0):
    """
    Create a LangChain-based Endodontic Therapy on Primary Teeth code extractor.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro-exp-03-25", temperature=temperature)
    
    prompt_template = PromptTemplate(
        template=f"""
You are a highly experienced dental coding expert 

### Before Picking a Code, Ask:
- What was the primary reason the patient came in? Was it a routine visit, or did the child present with pain, swelling, or trauma to a primary tooth?
- Which tooth is being treated? Is it an anterior (incisor/cuspid) or posterior (molar) primary tooth?
- Is the procedure focused on pulpal therapy with a resorbable filling, or does it involve additional restorative work?
- Has the tooth’s condition (e.g., caries, trauma, or infection) been evaluated via clinical exam or radiographs?
- Is this an emergency treatment or a planned procedure?

---

### Endodontic Therapy on Primary Teeth

#### Code: D3230
**Heading:** Pulpal therapy (resorbable filling) — anterior, primary tooth (excluding final restoration)  
**Description:** Primary incisors and cuspids.  
**When to Use:**  
- The patient is a child with a primary anterior tooth (incisor or cuspid) requiring pulpal therapy due to deep caries, trauma, or pulp exposure.  
- The procedure involves removing diseased pulp and placing a resorbable filling material to maintain tooth function until natural exfoliation.  
- Use when the focus is on pulp treatment, not the final restoration (e.g., crown or filling).  
**What to Check:**  
- Confirm the tooth is a primary anterior tooth (incisor or cuspid) via clinical exam or radiograph.  
- Assess the extent of pulp involvement (e.g., reversible/irreversible pulpitis or necrosis).  
- Check for signs of infection, abscess, or mobility that might indicate extraction instead.  
- Verify the patient’s medical history for conditions affecting treatment (e.g., allergies to materials).  
**Notes:**  
- This code excludes the final restoration—use a separate restorative code (e.g., D2940 or D2930) if a crown or filling is placed afterward.  
- Not appropriate for permanent teeth or posterior primary teeth (see D3240 for molars).  
- Narrative may be required if insurance questions the necessity (e.g., include X-ray evidence or clinical findings).  

#### Code: D3240
**Heading:** Pulpal therapy (resorbable filling) — posterior, primary tooth (excluding final restoration)  
**Description:** Primary first and second molars.  
**When to Use:**  
- The patient is a child with a primary posterior tooth (first or second molar) needing pulpal therapy due to caries, trauma, or pulp exposure.  
- The procedure involves pulp removal and placement of a resorbable filling material to preserve the tooth until exfoliation.  
- Use when the treatment targets the pulp, not the final restoration.  
**What to Check:**  
- Confirm the tooth is a primary molar (first or second) using clinical exam or radiograph.  
- Evaluate pulp vitality and the presence of infection, abscess, or excessive mobility.  
- Assess the tooth’s position and root resorption stage to ensure pulpal therapy is viable.  
- Review the child’s behavior and cooperation level, as this may affect treatment delivery.  
**Notes:**  
- Excludes final restoration—code separately for any crown (e.g., D2930) or filling placed after.  
- Not for anterior primary teeth (use D3230) or permanent teeth.  
- May require a narrative for insurance, detailing the clinical justification (e.g., caries depth, pulp status).  

---

### Key Takeaways:
- **Anterior vs. Posterior:** D3230 is for incisors/cuspids, while D3240 is for molars—tooth location drives code selection.  
- **Scope Matters:** These codes cover pulpal therapy only; additional restorative work requires separate coding.  
- **Resorbable Material:** Both procedures use resorbable fillings suited for primary teeth, not permanent solutions.  
- **Patient Age & Tooth Status:** Confirm the tooth is primary and not nearing exfoliation, as this impacts treatment decisions.  
- **Documentation:** Always document clinical findings (e.g., pulp exposure, infection) to support code use, especially for insurance claims.



### **Scenario:**
"{{question}}"

{PROMPT}
""",
        input_variables=["question"]
    )
    
    return LLMChain(llm=llm, prompt=prompt_template)

def extract_primary_teeth_therapy_code(scenario, temperature=0.0):
    """
    Extract Endodontic Therapy on Primary Teeth code(s) for a given scenario.
    """
    chain = create_primary_teeth_therapy_extractor(temperature)
    return chain.run(question=scenario).strip()

def activate_primary_teeth_therapy(scenario):
    """
    Activate Endodontic Therapy on Primary Teeth analysis and return results.
    """
    return extract_primary_teeth_therapy_code(scenario) 