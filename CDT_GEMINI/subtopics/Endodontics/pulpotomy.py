import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from subtopics.prompt.prompt import PROMPT


# Get model name from environment variable, default to gpt-4o if not set
MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o")

def create_pulpotomy_extractor(temperature=0.0):
    """
    Create a LangChain-based Pulpotomy code extractor.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro-exp-03-25", temperature=temperature)
    
    prompt_template = PromptTemplate(
        template=f"""
You are a highly experienced dental coding expert

### Before picking a code, ask:
- What was the primary reason the patient came in?
- Is the procedure being performed on a primary or permanent tooth?
- Is this a therapeutic procedure or preparatory for root canal therapy?
- Does the patient have incomplete root development?
- Is this an emergency procedure for pain relief?

---

### Pulpotomy Codes

**Code: D3220**  
**Heading:** Therapeutic pulpotomy (excluding final restoration) — removal of pulp coronal to the dentinocemental junction and application of medicament  
**Use when:** The procedure involves the surgical removal of a portion of the pulp with the aim of maintaining the vitality of the remaining portion using an adequate dressing.  
**Check:** Ensure that the procedure is performed on either primary or permanent teeth, but NOT as the first stage of root canal therapy. Not for apexogenesis.  
**Note:** This procedure is not to be used for permanent teeth with incomplete root development; instead, use D3222.

---

**Code: D3221**  
**Heading:** Pulpal debridement, primary and permanent teeth  
**Use when:** The procedure is performed for relief of acute pain before conventional root canal therapy.  
**Check:** Confirm that endodontic treatment is not being completed on the same day. This is an interim procedure meant to manage pain.  
**Note:** Should not be used if root canal therapy is initiated or completed during the same appointment.

---

**Code: D3222**  
**Heading:** Partial pulpotomy for apexogenesis — permanent tooth with incomplete root development  
**Use when:** A portion of the pulp is removed, and medicament is applied to maintain vitality and encourage continued root formation.  
**Check:** Ensure that the procedure is performed only on permanent teeth with incomplete root development.  
**Note:** This procedure is not considered the first stage of root canal therapy.

---

### Key Takeaways:
- **Primary vs. Permanent:** Ensure that the correct code is chosen based on whether the tooth is primary or permanent.
- **Therapeutic vs. Preparatory:** Pulpotomy is a standalone therapeutic treatment, whereas pulpal debridement (D3221) is used for temporary pain relief before further endodontic treatment.
- **Apexogenesis Considerations:** If the tooth has incomplete root development, D3222 is the appropriate code, not D3220.
- **Pain Management:** Use D3221 for acute pain relief before conventional root canal therapy, but ensure treatment is not completed the same day.
- **Long-Term Planning:** Consider the patient's overall treatment plan and select the code that best matches their stage of care.



### **Scenario:**
"{{question}}"

{PROMPT}
""",
        input_variables=["question"]
    )
    
    return LLMChain(llm=llm, prompt=prompt_template)

def extract_pulpotomy_code(scenario, temperature=0.0):
    """
    Extract Pulpotomy code(s) for a given scenario.
    """
    chain = create_pulpotomy_extractor(temperature)
    return chain.run(question=scenario).strip()

def activate_pulpotomy(scenario):
    """
    Activate Pulpotomy analysis and return results.
    """
    return extract_pulpotomy_code(scenario) 