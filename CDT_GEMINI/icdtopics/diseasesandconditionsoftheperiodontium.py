"""
Module for extracting diseases and conditions of the periodontium ICD-10 codes.
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

class PeriodontiumDiseasesServices:
    """Class to analyze and extract diseases and conditions of the periodontium ICD-10 codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing diseases and conditions of the periodontium."""
        return PromptTemplate(
            template=f"""
You are a highly experienced medical coding expert specializing in diseases and conditions of the periodontium. 
Analyze the given scenario and determine the most applicable ICD-10 code(s).

Diseases and Conditions of the Periodontium ICD-10 codes include:
5.1 Gingivitis
- K05.00: Acute gingivitis, plaque induced
- K05.01: Acute gingivitis, non-plaque induced
- K05.10: Chronic gingivitis, plaque induced
- K05.11: Chronic gingivitis, non-plaque induced

5.2 Gingival Recession
- K06.011: Localized gingival recession, minimal
- K06.012: Localized gingival recession, moderate
- K06.013: Localized gingival recession, severe
- K06.021: Generalized gingival recession, minimal
- K06.022: Generalized gingival recession, moderate
- K06.023: Generalized gingival recession, severe

5.3 Other Gingival Conditions
- K06.1: Gingival enlargement
- K06.2: Gingival and edentulous alveolar ridge lesions associated with trauma
- K06.3: Horizontal alveolar bone loss
- K06.8: Other specified disorders of gingiva and edentulous alveolar ridge

5.4 Periodontitis
- K05.211: Aggressive periodontitis, localized, slight
- K05.212: Aggressive periodontitis, localized, moderate
- K05.213: Aggressive periodontitis, localized, severe
- K05.219: Aggressive periodontitis, localized, unspecified severity
- K05.221: Aggressive periodontitis, generalized, slight
- K05.222: Aggressive periodontitis, generalized, moderate
- K05.223: Aggressive periodontitis, generalized, severe
- K05.311: Chronic periodontitis, localized, slight
- K05.312: Chronic periodontitis, localized, moderate
- K05.313: Chronic periodontitis, localized, severe
- K05.321: Chronic periodontitis, generalized, slight
- K05.322: Chronic periodontitis, generalized, moderate
- K05.323: Chronic periodontitis, generalized, severe
- K05.4: Periodontosis
- K05.5: Other periodontal disease

SCENARIO: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_periodontium_diseases_code(self, scenario: str) -> str:
        """Extract diseases and conditions of the periodontium code(s) for a given scenario."""
        try:
            print(f"Analyzing periodontium diseases scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Periodontium diseases extract_periodontium_diseases_code result: {code}")
            return code
        except Exception as e:
            print(f"Error in periodontium diseases code extraction: {str(e)}")
            return ""
    
    def activate_periodontium_disorders(self, scenario: str) -> str:
        """Activate the periodontium diseases analysis process and return results."""
        try:
            result = self.extract_periodontium_diseases_code(scenario)
            if not result:
                print("No periodontium diseases code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating periodontium diseases analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_periodontium_disorders(scenario)
        print(f"\n=== PERIODONTIUM DISEASES ANALYSIS RESULT ===")
        print(f"PERIODONTIUM DISEASES CODE: {result if result else 'None'}")


periodontium_diseases_service = PeriodontiumDiseasesServices()
# Example usage
if __name__ == "__main__":
    scenario = input("Enter a periodontium diseases dental scenario: ")
    periodontium_diseases_service.run_analysis(scenario)
