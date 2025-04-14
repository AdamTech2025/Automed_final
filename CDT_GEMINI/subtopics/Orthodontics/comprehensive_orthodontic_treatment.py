"""
Module for extracting comprehensive orthodontic treatment codes.
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
 
def create_comprehensive_orthodontic_treatment_extractor(temperature=0.0):
    """
    Create a LangChain-based comprehensive orthodontic treatment code extractor.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro-exp-03-25", temperature=temperature)
    
    prompt_template = PromptTemplate(
            template=f"""
    You are a highly experienced dental coding expert

Before picking a code, ask:
What stage of dentition is the patient in—transitional, adolescent, or adult?
Is this a full-course orthodontic treatment rather than a limited or interceptive treatment?
Does the patient require alignment of all or most teeth, including bite correction and occlusal adjustments?
Will the treatment involve multiple phases, including appliances, brackets, or other orthodontic interventions?
Are there specific skeletal or dental malocclusions being corrected over an extended period?
Will retention and post-treatment stabilization be necessary?

Detailed Coding Guidelines for Comprehensive Orthodontic Treatment
Code: D8070
Use when: Providing comprehensive orthodontic treatment for the transitional dentition.
Check: Ensure that the patient has a mix of primary and permanent teeth and requires full orthodontic correction.
Note: Typically used when significant alignment or bite issues are addressed before full permanent dentition erupts.
Code: D8080
Use when: Providing comprehensive orthodontic treatment for adolescent patients.
Check: Confirm that the patient has fully erupted permanent teeth and requires full orthodontic treatment.
Note: This is the most commonly used comprehensive orthodontic code for teenagers undergoing complete alignment correction.
Code: D8090
Use when: Providing comprehensive orthodontic treatment for adult dentition.
Check: Ensure that the patient requires full orthodontic correction, including bite realignment, over an extended treatment period.
Note: Often used for adult patients undergoing complex orthodontic treatment, including pre-prosthetic adjustments.

Key Takeaways:
Comprehensive orthodontic treatment addresses full dental alignment, bite correction, and occlusal adjustments.
Treatment is categorized based on dentition stage: transitional, adolescent, or adult.
Ensure documentation supports the necessity of full orthodontic intervention over an extended period.
Treatment often includes multiple phases, appliances, and retention strategies.

Scenario:
"{{question}}"

{PROMPT}
""",
        input_variables=["question"]
    )
    
    return LLMChain(llm=llm, prompt=prompt_template)

def extract_comprehensive_orthodontic_treatment_code(scenario, temperature=0.0):
    """
    Extract comprehensive orthodontic treatment code(s) for a given scenario.
    """
    try:
        chain = create_comprehensive_orthodontic_treatment_extractor(temperature)
        result = invoke_chain(chain, {"question": scenario})
        print(f"Comprehensive orthodontic treatment code result: {result}")
        return result.strip()
    except Exception as e:
        print(f"Error in extract_comprehensive_orthodontic_treatment_code: {str(e)}")
        return ""

def activate_comprehensive_orthodontic_treatment(scenario):
    """
    Activate comprehensive orthodontic treatment analysis and return results.
    """
    try:
        return extract_comprehensive_orthodontic_treatment_code(scenario)
    except Exception as e:
        print(f"Error in activate_comprehensive_orthodontic_treatment: {str(e)}")
        return "" 