import os
import sys
import asyncio
from langchain.prompts import PromptTemplate
from llm_services import LLMService, get_service, set_model, set_temperature

from sub_topic_registry import SubtopicRegistry

# Add the root directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)

# Import modules
from topics.prompt import PROMPT
from subtopics.diagnostics.clinicaloralevaluation import clinical_oral_evaluations_service
from subtopics.diagnostics.diagnosticimaging import diagnostic_imaging_service
from subtopics.diagnostics.oralpathologylaboratory import oral_pathology_laboratory_service
from subtopics.diagnostics.prediagnosticservices import prediagnostic_service
from subtopics.diagnostics.testsandexaminations import tests_service

class DiagnosticServices:
    """Class to analyze and activate diagnostic services based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
        self.registry = SubtopicRegistry()
        self._register_subtopics()
    
    def _register_subtopics(self):
        """Register all subtopics for parallel activation."""
        self.registry.register("D0120-D0180", clinical_oral_evaluations_service.activate_clinical_oral_evaluations, 
                            "Clinical Oral Evaluations (D0120-D0180)")
        self.registry.register("D0190-D0191", prediagnostic_service.activate_prediagnostic_services, 
                            "Pre-diagnostic Services (D0190-D0191)")
        self.registry.register("D0210-D0391", diagnostic_imaging_service.activate_diagnostic_imaging, 
                            "Diagnostic Imaging (D0210-D0391)")
        self.registry.register("D0472-D0502", oral_pathology_laboratory_service.activate_oral_pathology_laboratory, 
                            "Oral Pathology Laboratory (D0472-D0502)")
        self.registry.register("D0411-D0999", tests_service.activate_tests_and_examinations, 
                            "Tests and Laboratory Examinations (D0411-D0999)")
        self.registry.register("D4186", lambda x: "D4186" if "outcome assessment" in x.lower() else None, 
                            "Assessment of Patient Outcome Metrics (D4186)")
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing diagnostic services."""
        return PromptTemplate(
            template=f"""
You are a highly experienced dental coding expert with over 15 years of expertise in ADA dental codes. 
Your task is to analyze the given scenario and determine the most applicable diagnostic code range(s) based on the following classifications:

## **Clinical Oral Evaluations (D0120-D0180)**
**Use when:** Providing patient assessment services including routine or comprehensive evaluations.
**Check:** Documentation clearly specifies the type of evaluation performed (periodic, limited, comprehensive).
**Note:** These codes reflect different levels of examination depth and purpose.
**Activation trigger:** Scenario mentions OR implies any patient examination, assessment, evaluation, check-up, or diagnostic appointment. INCLUDE this range if there's any indication of patient evaluation or diagnostic assessment.

## **Pre-diagnostic Services (D0190-D0191)** 
**Use when:** Performing screening or limited assessment prior to comprehensive evaluation.
**Check:** Documentation shows brief assessment was performed to determine need for further care.
**Note:** These are typically preliminary evaluations, not comprehensive assessments.
**Activation trigger:** Scenario mentions OR implies any screening, triage, initial assessment, or preliminary examination. INCLUDE this range if there's any hint of preliminary evaluation before more detailed diagnosis.

## **Diagnostic Imaging (D0210-D0391)**
**Use when:** Capturing any diagnostic images to visualize oral structures.
**Check:** Documentation specifies the type of images obtained and their diagnostic purpose.
**Note:** Different codes apply based on the type, number, and complexity of images.
**Activation trigger:** Scenario mentions OR implies any radiographs, x-rays, imaging, CBCT, photographs, or visualization needs. INCLUDE this range if there's any indication that images were or should be taken for diagnostic purposes.

## **Oral Pathology Laboratory (D0472-D0502)**
**Use when:** Collecting and analyzing tissue samples for diagnostic purposes.
**Check:** Documentation includes details about sample collection and pathology reporting.
**Note:** These codes relate to laboratory examination of tissues, not clinical examination.
**Activation trigger:** Scenario mentions OR implies any biopsy, tissue sample, pathology testing, lesion analysis, or microscopic examination. INCLUDE this range if there's any suggestion of tissue sampling or pathological analysis.

## **Tests and Laboratory Examinations (D0411-D0999)**
**Use when:** Performing specialized diagnostic tests beyond clinical examination.
**Check:** Documentation details the specific test performed and clinical rationale.
**Note:** These include both chairside and laboratory-based diagnostic procedures.
**Activation trigger:** Scenario mentions OR implies any laboratory testing, diagnostic measures, microbial testing, pulp vitality assessment, or specialized diagnostic procedures. INCLUDE this range if there's any hint of diagnostic testing beyond visual examination.

## **Assessment of Patient Outcome Metrics (D4186)**
**Use when:** Evaluating treatment success or collecting quality improvement data.
**Check:** Documentation shows systematic assessment of treatment outcomes or patient satisfaction.
**Note:** This code relates to structured evaluation of care quality and results.
**Activation trigger:** Scenario mentions OR implies any outcome assessment, treatment success evaluation, patient satisfaction measurement, or quality improvement initiative. INCLUDE this range if there's any indication of measuring treatment effectiveness or outcomes.

### **Scenario:**
{{scenario}}
{PROMPT}

RESPOND WITH ALL APPLICABLE CODE RANGES from the options above, even if they are only slightly relevant.
List them in order of relevance, with the most relevant first.
""",
            input_variables=["scenario"]
        )
    
    def analyze_diagnostic(self, scenario: str) -> str:
        """Analyze the scenario to determine applicable code ranges."""
        try:
            print(f"Analyzing diagnostic scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code_range = result.strip()
            print(f"Diagnostic analyze_diagnostic result: {code_range}")
            return code_range
        except Exception as e:
            print(f"Error in analyze_diagnostic: {str(e)}")
            return ""
    
    async def activate_diagnostic(self, scenario: str) -> dict:
        """Activate relevant subtopics in parallel and return detailed results."""
        try:
            # Get the code range from the analysis
            diagnostic_result = self.analyze_diagnostic(scenario)
            if not diagnostic_result:
                print("No diagnostic result returned")
                return {}
            
            print(f"Diagnostic Result in activate_diagnostic: {diagnostic_result}")
            
            # Activate subtopics in parallel using the registry
            result = await self.registry.activate_all(scenario, diagnostic_result)
            
            # Return a dictionary with the required fields
            return {
                "code_range": diagnostic_result,
                "activated_subtopics": result["activated_subtopics"],
                "codes": result["topic_result"]
            }
        except Exception as e:
            print(f"Error in diagnostic analysis: {str(e)}")
            return {}
    
    async def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = await self.activate_diagnostic(scenario)
        print(f"\n=== DIAGNOSTIC ANALYSIS RESULT ===")
        print(f"CODE RANGE: {result.get('code_range', 'None')}")
        print(f"ACTIVATED SUBTOPICS: {', '.join(result.get('activated_subtopics', []))}")
        print(f"SPECIFIC CODES: {', '.join(result.get('codes', []))}")

diagnostic_service = DiagnosticServices()
# Example usage
if __name__ == "__main__":
    async def main():
        scenario = input("Enter a diagnostic dental scenario: ")
        await diagnostic_service.run_analysis(scenario)
    
    asyncio.run(main())