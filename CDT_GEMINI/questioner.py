import os
import logging
from dotenv import load_dotenv
from llm_services import generate_response, get_service, set_model, set_temperature
from llm_services import OPENROUTER_MODEL, DEFAULT_TEMP
from typing import Dict, Any, Optional


load_dotenv()

class Questioner:
    """Class to handle dental scenario questioning with configurable prompts and settings"""
    
    PROMPT_TEMPLATE = """
You are a highly experienced dental and medical coding expert with over 15 years of expertise in ADA dental procedure codes and ICD-10 diagnostic codes. Your task is to review the provided dental scenario along with the CDT and ICD analysis results to determine if any critical information is missing that is necessary for accurately assigning codes.

Scenario:
{scenario}

CDT Analysis Results:
{cdt_analysis}

ICD Analysis Results:
{icd_analysis}

Instructions:

1. Only ask questions that would directly impact the code selection. Do not ask questions that can be reasonably inferred from the scenario or that won't change the code selection.

2. For CDT codes, focus on:
   - Whether the patient is new or established (impacts evaluation codes)
   - The extent of the cavity (number of surfaces involved)
   - Whether radiographs were taken and what type
   - Only ask about treatment details if treatment was performed

IMPORTANT TASK TO FOLLOW: 
- Analyse only the cdt_analysis and icd_analysis ask questions only from the output you get from the file.
- Mostly try not to ask any questions, if basic assumptions solve the problem, do not ask questions.

4. If the scenario provides sufficient information for accurate coding, do not ask any questions.

Return your response in this exact format:
CDT_QUESTIONS: [List only the most critical CDT-specific questions that would impact code selection, one per line, or "None" if no questions are needed]
CDT_EXPLANATION: [Briefly explain why these specific CDT questions are necessary for code selection]
ICD_QUESTIONS: [List only the most critical ICD-specific questions that would impact code selection, one per line, or "None" if no questions are needed]
ICD_EXPLANATION: [Briefly explain why these specific ICD questions are necessary for code selection]

"""

    def __init__(self, model: str = OPENROUTER_MODEL, temperature: float = DEFAULT_TEMP):
        """Initialize the questioner with model and temperature settings"""
        self.service = get_service()
        self.configure(model, temperature)
        self.logger = self._setup_logging()

    def _setup_logging(self) -> logging.Logger:
        """Configure logging for the questioner module"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[logging.StreamHandler()]
        )
        return logging.getLogger(__name__)

    def configure(self, model: Optional[str] = None, temperature: Optional[float] = None) -> None:
        """Configure model and temperature settings"""
        if model:
            set_model(model)
        if temperature is not None:
            set_temperature(temperature)

    def format_prompt(self, scenario: str, cdt_analysis: Any, icd_analysis: Any) -> str:
        """Format the prompt template with the given inputs"""
        cdt_analysis_str = "\n".join([
            f"{key}: {value}" for key, value in cdt_analysis.items()
        ]) if isinstance(cdt_analysis, dict) else str(cdt_analysis)
        
        icd_analysis_str = "\n".join([
            f"{key}: {value}" for key, value in icd_analysis.items()
        ]) if isinstance(icd_analysis, dict) else str(icd_analysis)

        return self.PROMPT_TEMPLATE.format(
            scenario=scenario,
            cdt_analysis=cdt_analysis_str,
            icd_analysis=icd_analysis_str
        )

    def parse_response(self, response: str) -> Dict[str, Any]:
        """Parse the LLM response into structured format"""
        cdt_questions = []
        cdt_explanation = ""
        icd_questions = []
        icd_explanation = ""
        
        current_section = None
        current_explanation = ""
        for line in response.strip().split('\\n'):
            stripped_line = line.strip()
            if not stripped_line: 
                continue
            
            if stripped_line.startswith('"explanation":'):
                # This indicates the start of the JSON-like structure, ignore it
                continue

            upper_line = stripped_line.upper()
            if upper_line.startswith("CDT_QUESTIONS:"):
                current_section = "cdt"
                if ":" in stripped_line:
                    potential_explanation = stripped_line.split(":", 1)[1].strip()
                    if potential_explanation and not potential_explanation.lower().startswith("none"):
                        # If explanation is on the same line
                         cdt_explanation = potential_explanation
                continue # Move to the next line to read questions
            elif upper_line.startswith("ICD_QUESTIONS:"):
                current_section = "icd"
                if ":" in stripped_line:
                    potential_explanation = stripped_line.split(":", 1)[1].strip()
                    if potential_explanation and not potential_explanation.lower().startswith("none"):
                        # If explanation is on the same line
                         icd_explanation = potential_explanation
                continue # Move to the next line to read questions
            elif upper_line.startswith("EXPLANATION:"):
                 current_explanation = stripped_line[len("EXPLANATION:"):].strip()
                 # Decide where to put this explanation based on the current section context
                 if current_section == "cdt" and not cdt_explanation:
                     cdt_explanation = current_explanation
                 elif current_section == "icd" and not icd_explanation:
                     icd_explanation = current_explanation
                 # If section is None or already has explanation, this might be a general explanation (or misplaced)
                 # For now, we just store it; consider where it fits best if needed.
                 continue # Move to the next line

            # Add line to the correct list if it's not a marker or empty
            # CRITICAL FIX: Check if the line is literally "None" (case-insensitive)
            if stripped_line.lower() == '"none"' or stripped_line.lower() == 'none':
                continue # Skip adding "None" as a question

            if current_section == "cdt":
                cdt_questions.append(stripped_line.strip('"-, '))
            elif current_section == "icd":
                icd_questions.append(stripped_line.strip('"-, '))
            elif current_explanation: # If we captured an explanation before finding a section marker
                 # Assign explanation based on which question list gets populated first (heuristic)
                 if not cdt_explanation and not icd_explanation:
                      # Check if the line looks like a potential question
                     if stripped_line: # Add more checks if needed
                         # Assume it belongs to CDT if it appears first
                         cdt_explanation = current_explanation
                         cdt_questions.append(stripped_line.strip('"-, '))
                         current_section = "cdt" # Set section now

        return {
            "cdt_questions": {
                "questions": cdt_questions,
                "explanation": cdt_explanation.strip(),
                "has_questions": len(cdt_questions) > 0
            },
            "icd_questions": {
                "questions": icd_questions,
                "explanation": icd_explanation.strip(),
                "has_questions": len(icd_questions) > 0
            },
            "has_questions": len(cdt_questions) > 0 or len(icd_questions) > 0
        }

    def process(self, scenario: str, cdt_analysis: Any = None, icd_analysis: Any = None) -> Dict[str, Any]:
        """Process a scenario and generate questions"""
        try:
            formatted_prompt = self.format_prompt(scenario, cdt_analysis, icd_analysis)
            response = generate_response(formatted_prompt)
            return self.parse_response(response)
        except Exception as e:
            self.logger.error(f"Error in process: {str(e)}")
            return {
                "cdt_questions": {
                    "questions": [],
                    "explanation": f"Error occurred: {str(e)}",
                    "has_questions": False
                },
                "icd_questions": {
                    "questions": [],
                    "explanation": f"Error occurred: {str(e)}",
                    "has_questions": False
                },
                "has_questions": False
            }

    @property
    def current_settings(self) -> Dict[str, Any]:
        """Get current model settings"""
        return {
            "model": self.service.model,
            "temperature": self.service.temperature
        }

class QuestionerCLI:
    """Command Line Interface for the Questioner"""
    
    def __init__(self):
        self.questioner = Questioner()

    def print_settings(self):
        """Print current model settings"""
        settings = self.questioner.current_settings
        print(f"Using model: {settings['model']} with temperature: {settings['temperature']}")

    def print_results(self, result: Dict[str, Any]):
        """Print questioner results in a formatted way"""
        print("\n=== CDT QUESTIONS ===")
        if result["cdt_questions"]["has_questions"]:
            for q in result["cdt_questions"]["questions"]:
                print(f"- {q}")
            print(f"\nExplanation: {result['cdt_questions']['explanation']}")
        else:
            print("No CDT questions needed")

        print("\n=== ICD QUESTIONS ===")
        if result["icd_questions"]["has_questions"]:
            for q in result["icd_questions"]["questions"]:
                print(f"- {q}")
            print(f"\nExplanation: {result['icd_questions']['explanation']}")
        else:
            print("No ICD questions needed")

    def run(self):
        """Run the CLI interface"""
        self.print_settings()
        scenario = input("Enter dental scenario: ")
        cdt_analysis = input("Enter CDT analysis (or press Enter to skip): ") or None
        icd_analysis = input("Enter ICD analysis (or press Enter to skip): ") or None
        
        result = self.questioner.process(scenario, cdt_analysis, icd_analysis)
        self.print_results(result)

def main():
    """Main entry point for the script"""
    cli = QuestionerCLI()
    cli.run()

if __name__ == "__main__":
    main()
