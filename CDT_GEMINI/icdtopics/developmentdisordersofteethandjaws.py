"""
Module for extracting development disorders of teeth and jaws ICD-10 codes.
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

class DevelopmentDisordersServices:
    """Class to analyze and extract development disorders of teeth and jaws ICD-10 codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing development disorders of teeth and jaws."""
        return PromptTemplate(
            template=f"""
You are a highly experienced medical coding expert specializing in development disorders of teeth and jaws. 
Analyze the given scenario and determine the most applicable ICD-10 code(s).

3.1 Disorders of Tooth Development:
- K00.0: Anodontia
- K00.1: Supernumerary teeth
- K00.2: Abnormalities of size and form of teeth
- K00.3: Mottled teeth
- K00.4: Disturbances in tooth formation
- K00.5: Hereditary disturbances in tooth structure, not elsewhere classified
- K00.6: Disturbances in tooth eruption
- K00.7: Teething syndrome
- K00.8: Other disorders of tooth development
- K00.9: Disorder of tooth development, unspecified

3.2 Embedded and Impacted Teeth:
- K01.0: Embedded teeth
- K01.1: Impacted teeth

8.4 Malocclusion
- M26.211: Malocclusion, Angle's Class I
- M26.212: Malocclusion, Angle's Class II
- M26.213: Malocclusion, Angle's Class III
- M26.220: Open anterior occlusal relationship
- M26.221: Open posterior occlusal relationship
- M26.23: Excessive horizontal overlap
- M26.24: Reverse articulation
- M26.25: Anomalies of interarch distance
- M26.29: Other anomalies of dental arch relationship
- M26.30: Unspecified anomaly of tooth position of fully erupted tooth or teeth
- M26.31: Crowding of fully erupted teeth
- M26.32: Excessive spacing of fully erupted teeth
- M26.33: Horizontal displacement of fully erupted tooth or teeth
- M26.34: Vertical displacement of fully erupted tooth or teeth
- M26.35: Rotation of fully erupted tooth or teeth
- M26.36: Insufficient interocclusal distance of fully erupted teeth (ridge)
- M26.37: Excessive interocclusal distance of fully erupted teeth
- M26.39: Other anomalies of tooth position of fully erupted tooth or teeth
- M26.51: Abnormal jaw closure
- M26.52: Limited mandibular range of motion
- M26.53: Deviation in opening and closing of the mandible
- M26.54: Insufficient anterior guidance
- M26.55: Centric occlusion maximum intercuspation discrepancy
- M26.56: Non-working side interference
- M26.57: Lack of posterior occlusal support
- M26.59: Other dentofacial functional abnormalities

8.5 Jaw Anomalies
- M26.01: Maxillary hyperplasia
- M26.02: Maxillary hypoplasia
- M26.03: Mandibular hyperplasia
- M26.04: Mandibular hypoplasia
- M26.05: Macrogenia
- M26.06: Microgenia
- M26.07: Excessive tuberosity of jaw
- M26.10: Unspecified anomaly of jaw-cranial base relationship
- M26.11: Maxillary asymmetry
- M26.12: Other jaw asymmetry
- M26.19: Other specified anomalies of jaw-cranial base relationship
- M26.20: Unspecified anomaly of dental arch relationship

8.7 Cleft Lip and Palate
- Q35.1: Cleft hard palate
- Q35.3: Cleft soft palate
- Q35.5: Cleft hard palate with cleft soft palate
- Q35.7: Cleft uvula
- Q36.0: Cleft lip, bilateral
- Q36.1: Cleft lip, median
- Q36.9: Cleft lip, unilateral
- Q37.0: Cleft hard palate with bilateral cleft lip
- Q37.1: Cleft hard palate with unilateral cleft lip
- Q37.2: Cleft soft palate with bilateral cleft lip
- Q37.3: Cleft soft palate with unilateral cleft lip
- Q37.4: Cleft hard and soft palate with bilateral cleft lip
- Q37.5: Cleft hard and soft palate with unilateral cleft lip

8.8 Congenital Malformations of Mouth, Tongue, and Pharynx
- Q38.0: Congenital malformations of lips, not elsewhere classified
- Q38.1: Macroglossia
- Q38.2: Other congenital malformations of tongue
- Q38.3: Congenital malformations of salivary glands and ducts
- Q38.4: Congenital malformations of palate, not elsewhere classified
- Q38.5: Other congenital malformations of mouth
- Q38.6: Ankyloglossia

SCENARIO: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_development_disorders_code(self, scenario: str) -> str:
        """Extract development disorders of teeth and jaws code(s) for a given scenario."""
        try:
            print(f"Analyzing development disorders scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Development disorders extract_development_disorders_code result: {code}")
            return code
        except Exception as e:
            print(f"Error in development disorders code extraction: {str(e)}")
            return ""
    
    def activate_development_disorders(self, scenario: str) -> str:
        """Activate the development disorders analysis process and return results."""
        try:
            result = self.extract_development_disorders_code(scenario)
            if not result:
                print("No development disorders code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating development disorders analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_development_disorders(scenario)
        print(f"\n=== DEVELOPMENT DISORDERS ANALYSIS RESULT ===")
        print(f"DEVELOPMENT DISORDERS CODE: {result if result else 'None'}")


development_disorders_service = DevelopmentDisordersServices()
# Example usage
if __name__ == "__main__":
    scenario = input("Enter a development disorders of teeth and jaws scenario: ")
    development_disorders_service.run_analysis(scenario)