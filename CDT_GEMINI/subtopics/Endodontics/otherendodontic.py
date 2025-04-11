import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from subtopics.prompt.prompt import PROMPT


# Get model name from environment variable, default to gpt-4o if not set
MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o")

def create_other_endodontic_extractor(temperature=0.0):
    """
    Create a LangChain-based Other Endodontic Procedures code extractor.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro-exp-03-25", temperature=temperature)
    
    prompt_template = PromptTemplate(
        template=f"""
You are a highly experienced dental coding expert

 Before Picking a Code, Ask:
- What was the primary reason the patient came in? Was it for a specific endodontic issue requiring a unique procedure, or was it identified during another treatment?
- Is the procedure surgical, restorative, or preparatory, and does it involve isolation, root modification, or an unspecified service?
- Does the procedure align with a specific code, or is it too unique to fit standard descriptions?
- Are diagnostic tools (e.g., radiographs, clinical exams) supporting the need for the procedure?
- Is the procedure standalone or part of a broader treatment plan (e.g., root canal, restoration)?

---

### Other Endodontic Procedures

#### Code: D3910
**Heading:** Surgical procedure for isolation of tooth with rubber dam  
**When to Use:**  
- The patient requires a surgical procedure to isolate a tooth using a rubber dam, typically to facilitate endodontic treatment in a challenging case (e.g., subgingival access).  
- Use when isolation is surgically achieved beyond standard dam placement.  
**What to Check:**  
- Confirm the tooth requires surgical isolation (e.g., deep caries, fractured below gumline) via exam or radiograph.  
- Assess the complexity of achieving a dry field surgically.  
- Check if part of another endodontic procedure (e.g., root canal) or standalone.  
- Verify patient’s periodontal status and surgical feasibility.  
**Notes:**  
- Not for routine rubber dam use—specific to surgical isolation.  
- Narrative may be required to justify surgical need for insurance.  
- Often paired with other endodontic codes (e.g., D3310).  

#### Code: D3911
**Heading:** Intraorifice barrier  
**Description:** Not to be used as a final restoration.  
**When to Use:**  
- The patient has a tooth undergoing endodontic treatment where an intraorifice barrier (e.g., MTA, glass ionomer) is placed over the canal orifices to prevent coronal leakage.  
- Use after root canal obturation but before final restoration.  
**What to Check:**  
- Confirm root canal therapy (e.g., D3310-D3330) is completed prior to barrier placement.  
- Assess the need for coronal sealing (e.g., risk of microleakage).  
- Check if a final restoration follows (code separately, e.g., D2950).  
- Verify material used and placement depth.  
**Notes:**  
- Not a final restoration—code restorative work separately.  
- Enhances prognosis—document purpose for insurance.  
- Typically used in multi-visit endodontic cases.  

#### Code: D3920
**Heading:** Hemisection (including any root removal), not including root canal therapy  
**Description:** Includes separation of a multi-rooted tooth into separate sections containing the root and the overlying portion of the crown. It may also include the removal of one or more of those sections.  
**When to Use:**  
- The patient has a multi-rooted tooth (e.g., molar) where one section (root and crown) is separated or removed due to pathology (e.g., furcation defect), preserving the rest.  
- Use when root canal therapy is not part of this procedure.  
**What to Check:**  
- Confirm the tooth is multi-rooted and sectionable via radiograph.  
- Assess which root/crown section is affected (e.g., caries, fracture).  
- Check if root canal therapy precedes or follows (code separately, e.g., D3330).  
- Verify restorability of remaining section(s).  
**Notes:**  
- Excludes root canal therapy—use separate codes if performed.  
- Specify section removed in documentation.  
- Often followed by restorative or prosthetic coding.  

#### Code: D3921
**Heading:** Decoronation or submergence of an erupted tooth  
**Description:** Intentional removal of coronal tooth structure for preservation of root and surrounding bone.  
**When to Use:**  
- The patient has an erupted tooth (often due to trauma or ankylosis) where the crown is removed to preserve the root and bone for future prosthetics or growth (e.g., in young patients).  
- Use for intentional coronal reduction and root submergence.  
**What to Check:**  
- Confirm the tooth is erupted and suitable for decoronation via radiograph.  
- Assess the root’s condition and bone preservation goals (e.g., ridge maintenance).  
- Check patient age and treatment plan (e.g., future implant).  
- Verify no infection contraindicates submergence.  
**Notes:**  
- Common in pediatric or orthodontic cases—document intent.  
- Narrative and X-rays required for insurance justification.  
- Not for extraction (use D7140 if tooth is fully removed).  

#### Code: D3950
**Heading:** Canal preparation and fitting of preformed dowel or post  
**Description:** Should not be reported in conjunction with D2952, D2953, D2954, or D2957 by the same practitioner.  
**When to Use:**  
- The patient has a tooth post-endodontic treatment requiring canal preparation and fitting of a preformed dowel/post for core retention.  
- Use when preparing the canal and fitting the post in one visit.  
**What to Check:**  
- Confirm prior root canal therapy and canal suitability for a post via radiograph.  
- Assess the preformed post type and fit (not custom fabricated).  
- Check if same practitioner avoids D2952-D2957 overlap.  
- Verify tooth restorability and core buildup plan.  
**Notes:**  
- Excludes custom posts (e.g., D2952)—use only for preformed.  
- Not billable with D2952, D2953, D2954, D2957 by same provider.  
- Often followed by core buildup code (e.g., D2950).  

#### Code: D3999
**Heading:** Unspecified endodontic procedure, by report  
**Description:** Used for a procedure that is not adequately described by a code. Describe the procedure.  
**When to Use:**  
- The patient undergoes an endodontic procedure that doesn’t fit standard codes (e.g., experimental technique, unique complication).  
- Use as a catch-all with a detailed report.  
**What to Check:**  
- Confirm no specific code applies (e.g., D3410, D3331) via procedure review.  
- Assess the procedure’s purpose, complexity, and outcome.  
- Check if diagnostic evidence (e.g., X-rays) supports the need.  
- Verify patient consent for non-standard treatment.  
**Notes:**  
- Requires a detailed narrative describing the procedure, time, and materials.  
- Insurance may delay payment pending review—submit X-rays if applicable.  
- Use sparingly—specific codes are preferred when available.  

---

### Key Takeaways:
- **Procedure Specificity:** Codes range from surgical isolation to unspecified services—match the intent precisely.  
- **Scope Limits:** Codes reflect focused actions (e.g., hemisection excludes root canal)—don’t overcode volume.  
- **Restoration Exclusion:** Many procedures (e.g., D3911, D3950) don’t include final restorations—code separately.  
- **Documentation Heavy:** Unique procedures (e.g., D3999, D3921) need narratives and evidence for insurance.  
- **Combination Rules:** Check restrictions (e.g., D3950 with D2952) to avoid billing conflicts.



### **Scenario:**
"{{question}}"

{PROMPT}
""",
        input_variables=["question"]
    )
    
    return LLMChain(llm=llm, prompt=prompt_template)

def extract_other_endodontic_code(scenario, temperature=0.0):
    """
    Extract Other Endodontic Procedures code(s) for a given scenario.
    """
    chain = create_other_endodontic_extractor(temperature)
    return chain.run(question=scenario).strip()

def activate_other_endodontic(scenario):
    """
    Activate Other Endodontic Procedures analysis and return results.
    """
    return extract_other_endodontic_code(scenario) 