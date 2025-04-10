import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from subtopics.prompt.prompt import PROMPT


# Get model name from environment variable, default to gpt-4o if not set
MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o")

def create_pulp_capping_extractor(temperature=0.0):
    """
    Create a LangChain-based Pulp Capping code extractor.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.0-flash-thinking-exp-01-21", temperature=temperature)
    
    prompt_template = PromptTemplate(
        template=f"""
You are a highly experienced dental coding expert 

 Before picking a code, ask:
- What was the primary reason the patient came in?
- Was it for a general check-up, or to address a specific concern?
- Is the treatment intended to preserve the pulp or remove infected tissue?
- Is the pulp exposed, nearly exposed, or has deep decay?
- Is the procedure direct or indirect?

---

### **Endodontic Procedure Codes**

#### **D3110 - Pulp Cap — Direct (excluding final restoration)**
**Use when:** The pulp is exposed, and a protective dressing is applied directly over it to promote healing.  
**Check:** Ensure the material used is biocompatible and supports dentin bridge formation.  
**Note:** This is NOT a final restoration; a separate restorative procedure will be required.

#### **D3120 - Pulp Cap — Indirect (excluding final restoration)**
**Use when:** The pulp is nearly exposed, and a protective dressing is applied to protect it from further injury.  
**Check:** Confirm that all caries have been removed before placing the protective material.  
**Note:** This code is NOT to be used for bases and liners when all decay has been removed.

---

### **Key Takeaways:**
- **Direct vs. Indirect:** Direct pulp caps are used when the pulp is actually exposed; indirect pulp caps are used when the pulp is nearly exposed but still covered by dentin.
- **Final Restoration:** These procedures do not include final restorative work; a separate code should be used for the restoration.
- **Caries Removal:** Ensure all decay has been properly removed before applying an indirect pulp cap.
- **Documentation:** Clearly document pulp exposure status and materials used to support appropriate billing and case tracking.

### **Scenario:**
"{{question}}"

{PROMPT}
""",
        input_variables=["question"]
    )
    
    return LLMChain(llm=llm, prompt=prompt_template)

def extract_pulp_capping_code(scenario, temperature=0.0):
    """
    Extract Pulp Capping code(s) for a given scenario.
    """
    chain = create_pulp_capping_extractor(temperature)
    return chain.run(question=scenario).strip()

def activate_pulp_capping(scenario):
    """
    Activate Pulp Capping analysis and return results.
    """
    return extract_pulp_capping_code(scenario) 