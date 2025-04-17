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

##Dont ask any questions to the user unless and untill if the question can make a change in the codes. Else dont ask any questions. Just use the information provided and make the best judgement call.


IMPORTANT TASK TO FOLLOW: 
- Analyse only the cdt_analysis and ask questions only from the output you get from the file and do not look into the scenario. 
- Mostly try not to ask any questions, if basic assumptions solve the problem, do not ask questions.

Separate by Category:


CDT: If there is any missing information relevant to ADA dental procedure codes.


ICD: If there is any missing information relevant to ICD-10 diagnostic codes.


Avoid Unnecessary Questions: If the scenario contains all the critical information needed for accurate coding, do not ask any questions.



Return your response in this exact format:
CDT_QUESTIONS: [List CDT-specific questions, one per line, or "None" if no questions are needed]
CDT_EXPLANATION: [Briefly explain why these CDT questions are necessary or why no questions are needed]
ICD_QUESTIONS: [List ICD-specific questions, one per line, or "None" if no questions are needed]
ICD_EXPLANATION: [Briefly explain why these ICD questions are necessary or why no questions are needed]
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
        for line in response.strip().split('\n'):
            if line.startswith("CDT_QUESTIONS:"):
                current_section = "cdt_questions"
                continue
            elif line.startswith("CDT_EXPLANATION:"):
                current_section = "cdt_explanation"
                continue
            elif line.startswith("ICD_QUESTIONS:"):
                current_section = "icd_questions"
                continue
            elif line.startswith("ICD_EXPLANATION:"):
                current_section = "icd_explanation"
                continue
            
            if line.strip():
                if current_section == "cdt_questions" and line.strip().lower() != "none":
                    cdt_questions.append(line.strip())
                elif current_section == "cdt_explanation":
                    cdt_explanation = line.strip()
                elif current_section == "icd_questions" and line.strip().lower() != "none":
                    icd_questions.append(line.strip())
                elif current_section == "icd_explanation":
                    icd_explanation = line.strip()

        return {
            "cdt_questions": {
                "questions": cdt_questions,
                "explanation": cdt_explanation,
                "has_questions": len(cdt_questions) > 0
            },
            "icd_questions": {
                "questions": icd_questions,
                "explanation": icd_explanation,
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
