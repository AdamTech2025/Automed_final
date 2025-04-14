"""
Module for extracting minor treatment to control harmful habits codes.
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
 
def create_minor_treatment_harmful_habits_extractor(temperature=0.0):
    """
    Create a LangChain-based minor treatment to control harmful habits code extractor.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro-exp-03-25", temperature=temperature)
    
    prompt_template = PromptTemplate(
        template=f"""
Before picking a code, ask:
Is the treatment aimed at preventing or correcting a harmful oral habit such as thumb sucking or tongue thrusting?
Does the patient require a fixed or removable appliance for habit control?
Is the appliance intended for long-term or short-term use?
Has the patient demonstrated compliance with previous habit control interventions?
Will additional orthodontic intervention be needed in the future?

Detailed Coding Guidelines for Minor Treatment to Control Harmful Habits
Code: D8210
Use when: Providing a removable appliance for habit control therapy.
Check: Ensure that the appliance is designed to address oral habits such as thumb sucking or tongue thrusting and can be removed by the patient.
Note: Commonly used for younger patients requiring temporary habit correction without fixed orthodontic intervention.
Code: D8220
Use when: Providing a fixed appliance for habit control therapy.
Check: Confirm that the appliance is cemented or bonded in place to prevent patient removal and is specifically used to address habits like thumb sucking or tongue thrusting.
Note: Typically used when compliance with a removable appliance is a concern or when long-term control is necessary.

Key Takeaways:
Habit control appliances are used to prevent or correct harmful oral habits that can affect dental development.
The choice between removable (D8210) and fixed (D8220) appliances depends on patient compliance and the severity of the habit.
Documentation should specify the habit being addressed, appliance type, and expected treatment duration.
Habit correction may be a standalone treatment or part of a broader orthodontic plan.


Scenario:
"{{question}}"

{PROMPT}
""",
        input_variables=["question"]
    )
    
    return LLMChain(llm=llm, prompt=prompt_template)

def extract_minor_treatment_harmful_habits_code(scenario, temperature=0.0):
    """
    Extract minor treatment to control harmful habits code(s) for a given scenario.
    """
    try:
        chain = create_minor_treatment_harmful_habits_extractor(temperature)
        result = invoke_chain(chain, {"question": scenario})
        print(f"Minor treatment to control harmful habits code result: {result}")
        return result.strip()
    except Exception as e:
        print(f"Error in extract_minor_treatment_harmful_habits_code: {str(e)}")
        return ""

def activate_minor_treatment_harmful_habits(scenario):
    """
    Activate minor treatment to control harmful habits analysis and return results.
    """
    try:
        return extract_minor_treatment_harmful_habits_code(scenario)
    except Exception as e:
        print(f"Error in activate_minor_treatment_harmful_habits: {str(e)}")
        return "" 