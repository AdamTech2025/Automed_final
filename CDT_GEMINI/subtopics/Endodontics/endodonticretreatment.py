import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from subtopics.prompt.prompt import PROMPT


# Get model name from environment variable, default to gpt-4o if not set
MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o")

def create_endodontic_retreatment_extractor(temperature=0.0):
    """
    Create a LangChain-based Endodontic Retreatment code extractor.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-flash-8b", temperature=temperature)
    
    prompt_template = PromptTemplate(
        template=f"""
You are a highly experienced dental coding expert

### Before Picking a Code, Ask:
- What was the primary reason the patient came in? Did they present with symptoms (e.g., pain, swelling) related to a previously treated root canal, or was it identified during a routine exam?
- Which tooth is being retreated? Is it an anterior, premolar, or molar tooth?
- Has the previous root canal failed due to persistent infection, inadequate seal, or new decay/trauma?
- Are there diagnostic findings (e.g., radiographs, clinical exam) confirming the need for retreatment?
- Is the retreatment feasible, or does the tooth’s condition suggest extraction or surgical intervention instead?

---

### Endodontic Retreatment

#### Code: D3346
**Heading:** Retreatment of previous root canal therapy — anterior  
**When to Use:**  
- The patient has a permanent anterior tooth (incisor or canine) with a prior root canal that has failed (e.g., persistent infection, pain, or radiolucency).  
- The procedure involves removing old root canal filling material, re-cleaning, shaping, and re-obturating the canal.  
- Use when the focus is on non-surgical retreatment of the anterior tooth.  
**What to Check:**  
- Confirm the tooth is an anterior permanent tooth via radiograph or clinical exam.  
- Assess the reason for failure (e.g., missed canal, coronal leakage, or periapical pathology).  
- Check the tooth’s restorability and prognosis post-retreatment.  
- Verify patient symptoms (e.g., sensitivity, swelling) and history of the initial treatment.  
**Notes:**  
- Excludes final restoration—use a separate code (e.g., D2950 or D2750) for core buildup or crown.  
- Not for premolars or molars (see D3347 or D3348).  
- Narrative and pre/post-treatment X-rays may be required for insurance to justify retreatment.  

#### Code: D3347
**Heading:** Retreatment of previous root canal therapy — premolar  
**When to Use:**  
- The patient has a permanent premolar with a previously treated root canal showing signs of failure (e.g., abscess, discomfort).  
- Involves removing existing filling material, re-treating the canal(s), and sealing them again.  
- Use when the procedure is a non-surgical retreatment of a premolar.  
**What to Check:**  
- Confirm the tooth is a premolar using clinical exam or radiograph.  
- Evaluate the number of canals (typically 1-2) and the cause of failure (e.g., inadequate obturation).  
- Check for fractures, resorption, or periapical lesions affecting treatment success.  
- Review patient history for prior endodontic details or recent symptoms.  
**Notes:**  
- Excludes final restoration—code separately for restorative work.  
- Not for anterior teeth or molars (see D3346 or D3348).  
- Documentation of failure (e.g., X-ray evidence) is critical for insurance approval.  

#### Code: D3348
**Heading:** Retreatment of previous root canal therapy — molar  
**When to Use:**  
- The patient has a permanent molar with a failed prior root canal (e.g., persistent infection, new decay).  
- Involves removing old canal filling, re-cleaning, shaping, and re-filling multiple canals (typically 3-4).  
- Use when the focus is on non-surgical retreatment of a molar.  
**What to Check:**  
- Confirm the tooth is a molar via radiograph or clinical exam.  
- Assess the number and condition of canals (e.g., missed canals, calcification) and failure cause.  
- Check the tooth’s structural integrity and restorability after retreatment.  
- Verify patient symptoms and diagnostic findings (e.g., periapical radiolucency).  
**Notes:**  
- Excludes final restoration—use separate codes for crowns or fillings.  
- Not for anterior or premolar teeth (see D3346 or D3347).  
- Higher complexity (e.g., extra canals) may require a detailed narrative for insurance.  

---

### Key Takeaways:
- **Tooth-Specific Coding:** D3346 (anterior), D3347 (premolar), and D3348 (molar) are tied to tooth type—location accuracy is essential.  
- **Failure Confirmation:** Retreatment codes require evidence of prior root canal failure (e.g., X-rays, symptoms).  
- **Non-Surgical Focus:** These codes apply to non-surgical retreatments; surgical options (e.g., apicoectomy) use different codes.  
- **Restoration Exclusion:** Final restorations are coded separately—don’t bundle them into retreatment codes.  
- **Documentation Matters:** Insurance often demands narratives and imaging to support retreatment necessity.



### **Scenario:**
"{{question}}"

{PROMPT}
""",
        input_variables=["question"]
    )
    
    return LLMChain(llm=llm, prompt=prompt_template)

def extract_endodontic_retreatment_code(scenario, temperature=0.0):
    """
    Extract Endodontic Retreatment code(s) for a given scenario.
    """
    chain = create_endodontic_retreatment_extractor(temperature)
    return chain.run(question=scenario).strip()

def activate_endodontic_retreatment(scenario):
    """
    Activate Endodontic Retreatment analysis and return results.
    """
    return extract_endodontic_retreatment_code(scenario) 