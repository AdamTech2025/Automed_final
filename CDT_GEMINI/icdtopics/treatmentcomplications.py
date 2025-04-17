"""
Module for extracting treatment complications ICD-10 codes.
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

class TreatmentComplicationsServices:
    """Class to analyze and extract treatment complications ICD-10 codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing treatment complications."""
        return PromptTemplate(
            template=f"""
You are a highly experienced medical coding expert specializing in treatment complications. 
Analyze the given scenario and determine the most applicable ICD-10 code(s).

12.1 Complications Related to Dental Implants:
- T85.81XA: Embolism due to internal orthopedic prosthetic devices, implants and grafts, initial encounter
- T85.82XA: Fibrosis due to internal orthopedic prosthetic devices, implants and grafts, initial encounter
- T85.83XA: Hemorrhage due to internal orthopedic prosthetic devices, implants and grafts, initial encounter
- T85.84XA: Pain due to internal orthopedic prosthetic devices, implants and grafts, initial encounter
- T85.85XA: Stenosis due to internal orthopedic prosthetic devices, implants and grafts, initial encounter
- T85.86XA: Thrombosis due to internal orthopedic prosthetic devices, implants and grafts, initial encounter
- T85.89XA: Other specified complication of internal orthopedic prosthetic devices, implants and grafts, initial encounter

12.2 Complications of Surgical and Medical Care:
- M96.0: Pseudarthrosis after fusion or arthrodesis
- M96.1: Postlaminectomy syndrome, not elsewhere classified
- M96.6: Fracture of bone following insertion of orthopedic implant, joint prosthesis, or bone plate

12.3 Postprocedural Complications:
- K91.840: Postprocedural hemorrhage of a digestive system organ or structure following a dental procedure
- K91.841: Postprocedural hemorrhage of a digestive system organ or structure following other procedure
- K91.870: Postprocedural hematoma of a digestive system organ or structure following a dental procedure
- K91.871: Postprocedural hematoma of a digestive system organ or structure following other procedure
- K91.872: Postprocedural seroma of a digestive system organ or structure following a dental procedure
- K91.873: Postprocedural seroma of a digestive system organ or structure following other procedure

12.4 Medication-Related Complications:
- K12.31: Oral mucositis (ulcerative) due to antineoplastic therapy
- K12.32: Oral mucositis (ulcerative) due to other drugs
- K12.33: Oral mucositis (ulcerative) due to radiation
- K12.39: Other oral mucositis (ulcerative)
- T88.6XXA: Anaphylactic reaction due to adverse effect of correct drug or medicament properly administered, initial encounter
- T88.7XXA: Unspecified adverse effect of drug or medicament, initial encounter

12.5 Device-Related Complications:
- K08.52: Decreased vertical dimension of bite due to attrition of teeth
- K08.53: Decreased vertical dimension of bite due to trauma
- K08.54: Decreased vertical dimension of bite due to dietary habit (abrasion)
- K08.0: Exfoliation of teeth due to systemic causes

12.6 Failed Dental Restorative Materials:
- K08.51: Open restoration margins of tooth
- K08.530: Fractured dental restorative material with loss of material
- K08.531: Fractured dental restorative material without loss of material
- K08.539: Fractured dental restorative material, unspecified

SCENARIO: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_treatment_complications_code(self, scenario: str) -> str:
        """Extract treatment complications code(s) for a given scenario."""
        try:
            print(f"Analyzing treatment complications scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Treatment complications extract_treatment_complications_code result: {code}")
            return code
        except Exception as e:
            print(f"Error in treatment complications code extraction: {str(e)}")
            return ""
    
    def activate_treatment_complications(self, scenario: str) -> str:
        """Activate the treatment complications analysis process and return results."""
        try:
            result = self.extract_treatment_complications_code(scenario)
            if not result:
                print("No treatment complications code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating treatment complications analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_treatment_complications(scenario)
        print(f"\n=== TREATMENT COMPLICATIONS ANALYSIS RESULT ===")
        print(f"TREATMENT COMPLICATIONS CODE: {result if result else 'None'}")


treatment_complications_service = TreatmentComplicationsServices()
# Example usage
if __name__ == "__main__":
    scenario = input("Enter a treatment complications dental scenario: ")
    treatment_complications_service.run_analysis(scenario) 