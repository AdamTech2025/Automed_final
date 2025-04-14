"""
Module for extracting tissue conditioning codes.
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
 
def create_tissue_conditioning_extractor(temperature=0.0):
    """
    Create a LangChain-based tissue conditioning code extractor.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro-exp-03-25", temperature=temperature)
    
    prompt_template = PromptTemplate(
        template=f"""
You are a highly experienced dental coding expert
Before Picking a Code, Ask:
Is the patient experiencing irritation, inflammation, or hyperplasia under an existing prosthesis?

Is this part of a preparatory phase before fabricating a new denture or reline?

Are you planning to make a final impression once the tissues are healthy?

Is this a soft liner applied chairside (not lab-processed)?

Is the tissue response being monitored over a 2–4 week period?

Code: D5850
Heading: Tissue conditioning, maxillary
When to Use:

Apply when the upper arch tissues are inflamed or distorted due to a poor-fitting prosthesis.

Used as a temporary treatment to promote tissue healing before taking a final impression for a new maxillary denture or reline.
What to Check:

Ensure it’s a therapeutic soft liner, not a reline or rebase.

Confirm treatment is followed by future prosthetic work (e.g., D5110 or D5750).

Note progress in clinical records — usually adjusted or replaced within 2–4 weeks.
Notes:

Cannot be billed as a definitive procedure; it is preparatory.

Requires chairside application and intraoral evaluation of soft tissue healing.

Code: D5851
Heading: Tissue conditioning, mandibular
When to Use:

Use for lower arch tissue that needs healing before denture procedures.

Common with inflamed, flabby, or traumatized tissue from long-term denture wear.
What to Check:

Confirm the intent is pre-impression therapy before final prosthesis.

Ensure documentation of soft tissue response and reason for conditioning.

Used in conjunction with full or partial mandibular prosthetic plans.
Notes:

Typically replaced or evaluated within weeks.

Include a narrative if billing alongside other prosthodontic codes.

Key Takeaways:
Tissue Conditioning ≠ Reline: It’s a temporary therapeutic step, not a fit adjustment.

Requires Follow-Up: Conditioning should be monitored and replaced within 2–4 weeks.

Document Clearly: Record reason for tissue conditioning, material used, and future prosthetic plan.

Chairside Procedure: Applied directly in the office — lab-processed liners are coded differently.


Scenario:
"{{question}}"

{PROMPT}
""",
        input_variables=["question"]
    )
    
    return LLMChain(llm=llm, prompt=prompt_template)

def extract_tissue_conditioning_code(scenario, temperature=0.0):
    """
    Extract tissue conditioning code(s) for a given scenario.
    """
    try:
        chain = create_tissue_conditioning_extractor(temperature)
        result = invoke_chain(chain, {"question": scenario})
        print(f"Tissue conditioning code result: {result}")
        return result.strip()
    except Exception as e:
        print(f"Error in extract_tissue_conditioning_code: {str(e)}")
        return ""

def activate_tissue_conditioning(scenario):
    """
    Activate tissue conditioning analysis and return results.
    """
    try:
        return extract_tissue_conditioning_code(scenario)
    except Exception as e:
        print(f"Error in activate_tissue_conditioning: {str(e)}")
        return ""

# Example usage
if __name__ == "__main__":
    scenario = "Patient needs tissue conditioning treatment on the upper jaw before taking impressions for a new denture."
    result = activate_tissue_conditioning(scenario)
    print(result) 