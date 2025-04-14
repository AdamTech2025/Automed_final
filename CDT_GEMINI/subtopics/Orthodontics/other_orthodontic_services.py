"""
Module for extracting other orthodontic services codes.
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
 
def create_other_orthodontic_services_extractor(temperature=0.0):
    """
    Create a LangChain-based other orthodontic services code extractor.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro-exp-03-25", temperature=temperature)
    
    prompt_template = PromptTemplate(
        template=f"""
You are a highly experienced dental coding expert

Other Orthodontic Services – Detailed Coding Guidelines

Before picking a code, ask:
Is this a pre-treatment evaluation or a periodic visit during treatment?
Is the service related to monitoring, retention, appliance repair, or re-bonding?
Does the patient require adjustments, repairs, or removal of orthodontic devices?
Is this a case where a standard code does not apply, requiring a report-based procedure?



Code: D8660
Use when: Monitoring a patient’s growth and dental development before starting orthodontic treatment.
 Check: Ensure periodic evaluations are documented separately from diagnostic procedures.
 Note: This code applies to observation appointments to determine the right time for treatment.
Code: D8670
Use when: Conducting a periodic orthodontic treatment visit, typically for adjustments.
 Check: Confirm that the visit is part of an ongoing orthodontic treatment plan.
 Note: This is used for routine checkups and appliance adjustments during treatment.
Code: D8680
Use when: Completing orthodontic treatment and transitioning to retention.
 Check: Ensure documentation includes removal of appliances and placement of retainers.
 Note: This is a post-treatment phase to maintain alignment after braces are removed.
Code: D8681
Use when: Adjusting a removable orthodontic retainer after initial placement.
 Check: Verify that this is an adjustment visit, not a retainer replacement.
 Note: Routine minor modifications to retainers fall under this code.
Code: D8695
Use when: Removing fixed orthodontic appliances before treatment completion.
 Check: Ensure removal is due to reasons other than successful treatment completion.
 Note: Typically used for early removal due to patient preference or medical necessity.
Code: D8696
Use when: Repairing a maxillary orthodontic appliance, excluding brackets and standard braces.
 Check: Ensure the repair involves functional appliances, expanders, or specialized devices.
 Note: Standard bracket repairs are not included under this code.
Code: D8697
Use when: Repairing a mandibular orthodontic appliance, excluding standard braces.
 Check: Confirm the repair is necessary for non-standard orthodontic appliances.
 Note: Functional appliances and expanders fall under this category.
Code: D8698
Use when: Re-cementing or re-bonding a fixed maxillary retainer.
 Check: Ensure it is a reattachment, not a new retainer placement.
 Note: This applies to retainers that become loose but are still intact.
Code: D8699
Use when: Re-cementing or re-bonding a fixed mandibular retainer.
 Check: Confirm the original retainer is being reattached, not replaced.
 Note: This helps maintain retention without creating a new appliance.
Code: D8701
Use when: Repairing and reattaching a fixed retainer in the maxillary arch.
 Check: Ensure documentation includes the cause of damage and the method of repair.
 Note: Covers repairs beyond simple re-bonding, such as fractured retainers.
Code: D8702
Use when: Repairing and reattaching a fixed retainer in the mandibular arch.
 Check: Confirm the retainer is intact and requires only repair, not replacement.
 Note: Similar to D8701 but for the lower arch.
Code: D8703
Use when: Replacing a lost or broken maxillary retainer.
 Check: Ensure that the retainer is no longer usable and requires full replacement.
 Note: This code is for completely new retainers, not simple repairs.
Code: D8704
Use when: Replacing a lost or broken mandibular retainer.
 Check: Verify the need for a new retainer due to loss or irreparable damage.
 Note: Used similarly to D8703 but for the lower arch.
Code: D8999
Use when: A procedure is not adequately described by any existing orthodontic code.
 Check: Ensure proper documentation of the procedure details in a report.
 Note: This is a catch-all code for unlisted orthodontic services, requiring justification.

Key Takeaways:
Differentiate between pre-treatment evaluations, periodic visits, retention, and repairs.


Ensure documentation clearly supports the need for the service provided.


Use D8999 for unique orthodontic procedures that don’t fit standard codes.


Be specific about whether the service is for maxillary or mandibular appliances.



Scenario:
"{{question}}"

{PROMPT}
""",
        input_variables=["question"]
    )
    
    return LLMChain(llm=llm, prompt=prompt_template)

def extract_other_orthodontic_services_code(scenario, temperature=0.0):
    """
    Extract other orthodontic services code(s) for a given scenario.
    """
    try:
        chain = create_other_orthodontic_services_extractor(temperature)
        result = invoke_chain(chain, {"question": scenario})
        print(f"Other orthodontic services code result: {result}")
        return result.strip()
    except Exception as e:
        print(f"Error in extract_other_orthodontic_services_code: {str(e)}")
        return ""

def activate_other_orthodontic_services(scenario):
    """
    Activate other orthodontic services analysis and return results.
    """
    try:
        return extract_other_orthodontic_services_code(scenario)
    except Exception as e:
        print(f"Error in activate_other_orthodontic_services: {str(e)}")
        return "" 