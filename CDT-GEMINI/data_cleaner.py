import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from llm_services import create_chain, invoke_chain, get_llm_service, set_model_for_file

load_dotenv()

# You can set a specific model for this file only
# Uncomment and modify the line below to use a specific model
# set_model_for_file("gemini-1.5-pro")

def create_scenario_processor(temperature=0.0):
    # Create the prompt template
    prompt_template = PromptTemplate(
        template="""
You are a specialized dental data processor designed to transform raw dental scenarios into clearly structured, comprehensive datasets for medical coding purposes. Your task is to process the provided input scenario dynamically and accurately, adhering to the following strict guidelines:

INPUT SCENARIO:
{scenario}

No Assumptions: Process only the information explicitly stated in the input.(basic assumptions are allowed)

Full Data Retention: Capture and preserve every detail from the input scenario in the output, ensuring nothing is omitted. your job is to only structre data

also mention the command line if something is there like that , example "only do this and this"
  


OUTPUT FORMAT:

command line : if presented (e.g., only code for diagnosis),

Patient Details:
(Basic demographics, ID, date, provider, etc.),

Subjectives (What the patient says):
Patient's symptoms, concerns, history, and complaints in their own words.
e.g., "Patient complains of sharp pain in the lower right molar for 2 days.",

Objective(What the clinician sees/tests):
Provider's findings – clinical exams, measurements, radiographs, intraoral images, observations.
e.g., "Tooth #31 with deep occlusal caries, no response to cold, positive to percussion, probing within normal limits.",

Assessment(What provider concluded):
Provider's clinical impression or diagnosis.
e.g., "Irreversible pulpitis on tooth #31",

Treatment Provided(What the provider did in that visit):
Procedures done during this visit (detailed with codes if available).
e.g., "Emergency pulpectomy performed. CDT Code: D3220",

Recommendations Made(What the provider only recommended):
Provider's advice for future care, behavioral modifications, or referrals.
e.g., "Recommend root canal therapy and crown. Avoid chewing on right side.",

Medications:
Prescribed drugs, dosage, and instructions.
e.g., "Amoxicillin 500mg TID × 5 days, Ibuprofen 600mg q6h PRN pain",

Next Steps:
Follow-up appointments, further diagnostics, referrals.
e.g., "Schedule for full root canal and crown in 1 week."

        """,
        input_variables=["scenario"]
    )
    
    # Create the chain using our LLM service
    return create_chain(prompt_template)

def process_scenario(scenario):
    # Create the processor chain
    processor = create_scenario_processor()
    
    # Invoke the chain through our LLM service
    result = invoke_chain(processor, {"scenario": scenario})
    
    return {
        "standardized_scenario": result["text"].strip()
    }

# For testing if run directly
if __name__ == "__main__":
    # Print the current Gemini model and temperature being used
    llm_service = get_llm_service()
    print(f"Using Gemini model: {llm_service.gemini_model} with temperature: {llm_service.temperature}")
    
    test_scenario = input("Enter a dental scenario to process: ")
    result = process_scenario(test_scenario)
    
    print("\n=== STANDARDIZED SCENARIO ===")
    print(result["standardized_scenario"])
    
