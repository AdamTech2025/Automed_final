import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from subtopics.prompt.prompt import PROMPT


# Get model name from environment variable, default to gpt-4o if not set
MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o")

def create_apexification_extractor(temperature=0.0):
    """
    Create a LangChain-based Apexification/Recalcification code extractor.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-flash-8b", temperature=temperature)
    
    prompt_template = PromptTemplate(
        template=f"""
You are a highly experienced dental coding expert

Before Picking a Code, Ask:
- What was the primary reason the patient came in? Did they present with symptoms (e.g., pain, swelling) tied to a previously treated root canal, or was it discovered during a routine visit?
- Which tooth is being retreated? Is it an anterior, premolar, or molar tooth?
- Has the prior root canal failed due to issues like persistent infection, poor sealing, or new pathology?
- Are there diagnostic tools (e.g., radiographs, clinical exams) confirming the need for retreatment?
- Is the tooth still restorable, or does its condition suggest a different approach (e.g., extraction)?

---

### Apexification/Recalcification (Endodontic Retreatment with Provided Codes)
#### **Code:** D3351  
**Heading:** Apexification/Recalcification – Initial Visit  
**When to Use:**  
- The patient has an immature permanent tooth or an open apex that requires apical closure.  
- Used in cases involving root resorption, perforations, or other anomalies requiring calcific barrier formation.  
- Typically indicated when performing endodontic treatment on a non-vital tooth with an incompletely formed apex.  
- May also apply when repairing perforations or managing resorptive defects with medicament therapy.  

**What to Check:**  
- Confirm the presence of an open apex or apical pathology via radiographic evidence.  
- Assess the tooth’s vitality and pulpal status (usually necrotic pulp in young permanent teeth).  
- Evaluate whether the root is restorable and the prognosis is favorable with apexification.  
- Document clinical signs (e.g., sinus tract, swelling) and diagnostic testing (cold test, percussion).  

**Notes:**  
- Includes opening the tooth, canal debridement, placement of the first medicament (e.g., calcium hydroxide, MTA), and necessary radiographs.  
- Often represents the **first stage of root canal therapy** for immature teeth.  
- Follow-up visits for additional medicament replacement may require **D3352**, and the final visit for closure is coded with **D3353**.  
- Document material used and rationale clearly for insurance—especially in trauma or developmental cases.  


### Key Takeaways:
- **Tooth Location Drives Coding:** D3346 (anterior), D3347 (premolar), and D3348 (molar) are specific to tooth type—precision is critical.  
- **Evidence of Failure:** Retreatment codes require proof of prior root canal issues (e.g., imaging, symptoms).  
- **Non-Surgical Only:** These codes apply to non-surgical retreatments; surgical options have separate codes.  
- **Restoration Separate:** Final restorations aren’t included—code them independently.  
- **Insurance Prep:** Expect to provide narratives and X-rays to support retreatment claims.


Scenario:
"{{question}}"

{PROMPT}
""",
        input_variables=["question"]
    )
    
    return LLMChain(llm=llm, prompt=prompt_template)

def extract_apexification_code(scenario, temperature=0.0):
    """
    Extract Apexification/Recalcification code for a given scenario.
    """
    chain = create_apexification_extractor(temperature)
    return chain.run(question=scenario).strip()

def activate_apexification(scenario):
    """
    Activate Apexification/Recalcification analysis and return results.
    """
    return extract_apexification_code(scenario) 