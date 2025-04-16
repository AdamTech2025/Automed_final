"""
Module for extracting minor treatment to control harmful habits codes.
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
from subtopics.prompt.prompt import PROMPT

class MinorTreatmentHarmfulHabits:
    """Class to analyze and extract minor treatment to control harmful habits codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing minor treatment to control harmful habits."""
        return PromptTemplate(
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

SCENARIO: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_minor_treatment_harmful_habits_code(self, scenario: str) -> str:
        """Extract minor treatment to control harmful habits code for a given scenario."""
        try:
            print(f"Analyzing minor treatment to control harmful habits scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Minor treatment to control harmful habits extract_minor_treatment_harmful_habits_code result: {code}")
            return code
        except Exception as e:
            print(f"Error in minor treatment to control harmful habits code extraction: {str(e)}")
            return ""
    
    def activate_minor_treatment_harmful_habits(self, scenario: str) -> str:
        """Activate the minor treatment to control harmful habits analysis process and return results."""
        try:
            result = self.extract_minor_treatment_harmful_habits_code(scenario)
            if not result:
                print("No minor treatment to control harmful habits code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating minor treatment to control harmful habits analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_minor_treatment_harmful_habits(scenario)
        print(f"\n=== MINOR TREATMENT TO CONTROL HARMFUL HABITS ANALYSIS RESULT ===")
        print(f"MINOR TREATMENT TO CONTROL HARMFUL HABITS CODE: {result if result else 'None'}")


minor_treatment_harmful_habits = MinorTreatmentHarmfulHabits()
# Example usage
if __name__ == "__main__":
    scenario = input("Enter a minor treatment to control harmful habits scenario: ")
    minor_treatment_harmful_habits.run_analysis(scenario) 