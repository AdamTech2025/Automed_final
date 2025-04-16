import os
from dotenv import load_dotenv
from llm_services import generate_response, get_service, set_model, set_temperature
from typing import Dict, Any, Optional
from llm_services import OPENROUTER_MODEL, DEFAULT_TEMP
load_dotenv()

class DentalScenarioProcessor:
    """Class to handle dental scenario processing with configurable prompts and settings"""
    
    PROMPT_TEMPLATE = """
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
"""

    def __init__(self, model: str = OPENROUTER_MODEL, temperature: float = DEFAULT_TEMP):
        """Initialize the processor with model and temperature settings"""
        self.service = get_service()
        self.configure(model, temperature)

    def configure(self, model: Optional[str] = None, temperature: Optional[float] = None) -> None:
        """Configure model and temperature settings"""
        if model:
            set_model(model)
        if temperature is not None:
            set_temperature(temperature)

    def format_prompt(self, scenario: str) -> str:
        """Format the prompt template with the given scenario"""
        return self.PROMPT_TEMPLATE.format(scenario=scenario)

    def process(self, scenario: str) -> Dict[str, str]:
        """Process a dental scenario and return structured output"""
        formatted_prompt = self.format_prompt(scenario)
        result = generate_response(formatted_prompt)
        return {"standardized_scenario": result}

    @property
    def current_settings(self) -> Dict[str, Any]:
        """Get current model settings"""
        return {
            "model": self.service.model,
            "temperature": self.service.temperature
        }

class ScenarioProcessorCLI:
    """Command Line Interface for the DentalScenarioProcessor"""
    
    def __init__(self):
        self.processor = DentalScenarioProcessor()

    def print_settings(self):
        """Print current model settings"""
        settings = self.processor.current_settings
        print(f"Using model: {settings['model']} with temperature: {settings['temperature']}")

    def run(self):
        """Run the CLI interface"""
        self.print_settings()
        scenario = input("Enter dental scenario to process: ")
        result = self.processor.process(scenario)
        print("\n=== STANDARDIZED SCENARIO ===")
        print(result["standardized_scenario"])

def main():
    """Main entry point for the script"""
    cli = ScenarioProcessorCLI()
    cli.run()

if __name__ == "__main__":
    main()


