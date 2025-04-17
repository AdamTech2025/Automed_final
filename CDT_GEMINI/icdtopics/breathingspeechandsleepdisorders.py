"""
Module for extracting breathing, speech, and sleep disorders ICD-10 codes.
"""

import os
import sys
from langchain.prompts import PromptTemplate
from llm_services import LLMService, get_service, set_model, set_temperature

# Add the parent directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(parent_dir)

# Import modules
from icdtopics.prompt import PROMPT

class BreathingSleepDisordersServices:
    """Class to analyze and extract breathing, speech, and sleep disorders ICD-10 codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing breathing, speech, and sleep disorders."""
        return PromptTemplate(
            template=f"""
You are a highly experienced medical coding expert specializing in breathing, speech, and sleep disorders. 
Analyze the given scenario and determine the most applicable ICD-10 code(s).

Breathing, Speech, and Sleep Disorders ICD-10 codes include:
12.1 Mouthbreathing
- R06.5: Mouth breathing
- R06.83: Snoring
- R06.89: Other abnormalities of breathing

12.2 Speech Disorders
- R47.9: Unspecified speech disturbances
- F80.89: Other developmental disorders of speech and language
- F80.9: Developmental disorder of speech and language, unspecified

12.3 Sleep-Related Breathing Disorders
- G47.30: Sleep apnea, unspecified
- G47.31: Primary central sleep apnea
- G47.32: High altitude periodic breathing
- G47.33: Obstructive sleep apnea (adult) (pediatric)
- G47.34: Idiopathic sleep-related nonobstructive alveolar hypoventilation
- G47.35: Congenital central alveolar hypoventilation syndrome
- G47.36: Sleep-related hypoventilation in conditions classified elsewhere
- G47.37: Central sleep apnea in conditions classified elsewhere
- G47.39: Other sleep apnea
- G47.63: Sleep-related bruxism
- G47.8: Other sleep disorders
- G47.9: Sleep disorder, unspecified

SCENARIO: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_breathing_sleep_disorders_code(self, scenario: str) -> str:
        """Extract breathing, speech, and sleep disorders code(s) for a given scenario."""
        try:
            print(f"Analyzing breathing and sleep disorders scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Breathing and sleep disorders extract_breathing_sleep_disorders_code result: {code}")
            return code
        except Exception as e:
            print(f"Error in breathing and sleep disorders code extraction: {str(e)}")
            return ""
    
    def activate_breathing_sleep_disorders(self, scenario: str) -> str:
        """Activate the breathing and sleep disorders analysis process and return results."""
        try:
            result = self.extract_breathing_sleep_disorders_code(scenario)
            if not result:
                print("No breathing and sleep disorders code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating breathing and sleep disorders analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_breathing_sleep_disorders(scenario)
        print(f"\n=== BREATHING AND SLEEP DISORDERS ANALYSIS RESULT ===")
        print(f"BREATHING AND SLEEP DISORDERS CODE: {result if result else 'None'}")


breathing_sleep_disorders_service = BreathingSleepDisordersServices()
# Example usage
if __name__ == "__main__":
    scenario = input("Enter a breathing, speech, or sleep disorders dental scenario: ")
    breathing_sleep_disorders_service.run_analysis(scenario)
