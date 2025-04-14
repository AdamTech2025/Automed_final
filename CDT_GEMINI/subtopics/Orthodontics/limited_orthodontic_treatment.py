"""
Module for extracting limited orthodontic treatment codes.
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
 
def create_limited_orthodontic_treatment_extractor(temperature=0.0):
    """
    Create a LangChain-based limited orthodontic treatment code extractor.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro-exp-03-25", temperature=temperature)
    
    prompt_template = PromptTemplate(
        template=f"""
You are a highly experienced dental coding expert
Before picking a code, ask:
What stage of dentition is the patient in—primary, transitional, adolescent, or adult?
Is the orthodontic treatment focused on correcting a limited number of teeth or a localized issue?
Is this treatment intended to address minor alignment, spacing, or functional concerns rather than comprehensive orthodontics?
Does the patient require interceptive or early intervention treatment?
Are additional appliances or procedures needed beyond standard orthodontic care?

Detailed Coding Guidelines for Limited Orthodontic Treatment
Code: D8010
Use when: Providing limited orthodontic treatment for the primary dentition.
Check: Ensure that treatment is for early intervention, addressing minor misalignment or spacing issues in young children.
Note: Used primarily for preventive or minor corrective measures before permanent teeth emerge.

Code: D8020
Use when: Providing limited orthodontic treatment for the transitional dentition.
Check: Ensure that the patient has a mix of primary and permanent teeth, and treatment is focused on minor corrections.
Note: Typically used for early orthodontic guidance, such as minor tooth movement to create space for erupting teeth.

Code: D8030
Use when: Providing limited orthodontic treatment for adolescent patients with fully erupted permanent teeth.
Check: Confirm that treatment is focused on localized alignment issues rather than a full set of braces.
Note: Often used for minor corrective treatment in teens who do not require comprehensive orthodontic work.

Code: D8040
Use when: Providing limited orthodontic treatment for adult dentition.
Check: Ensure that treatment is addressing minor alignment concerns rather than full orthodontic correction.
Note: Common for adult patients seeking cosmetic or minor functional improvements without full orthodontic intervention.

Key Takeaways:
Limited orthodontic treatment is focused on minor corrections rather than comprehensive treatment.
Treatment is categorized based on the patient’s dentition stage: primary, transitional, adolescent, or adult.
Ensure documentation specifies the limited nature of the treatment and its objectives.
Use appropriate diagnostic records to justify limited treatment versus comprehensive orthodontic care.


Scenario:
"{{question}}"

{PROMPT}
""",
        input_variables=["question"]
    )
    
    return LLMChain(llm=llm, prompt=prompt_template)

def extract_limited_orthodontic_treatment_code(scenario, temperature=0.0):
    """
    Extract limited orthodontic treatment code(s) for a given scenario.
    """
    try:
        chain = create_limited_orthodontic_treatment_extractor(temperature)
        result = invoke_chain(chain, {"question": scenario})
        print(f"Limited orthodontic treatment code result: {result}")
        return result.strip()
    except Exception as e:
        print(f"Error in extract_limited_orthodontic_treatment_code: {str(e)}")
        return ""

def activate_limited_orthodontic_treatment(scenario):
    """
    Activate limited orthodontic treatment analysis and return results.
    """
    try:
        return extract_limited_orthodontic_treatment_code(scenario)
    except Exception as e:
        print(f"Error in activate_limited_orthodontic_treatment: {str(e)}")
        return "" 