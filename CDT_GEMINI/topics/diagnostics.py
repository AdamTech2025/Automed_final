import os
import sys
import asyncio
import re # Added for parsing
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

# Helper function to parse LLM activation results (same as in adjunctivegeneralservices.py)
def _parse_llm_topic_output(result_text: str) -> dict:
    parsed = {"explanation": None, "doubt": None, "code_range": None}
    if not isinstance(result_text, str):
        return parsed

    # Extract Explanation
    explanation_match = re.search(r"EXPLANATION:\s*(.*?)(?=\s*DOUBT:|\s*CODE RANGE:|$)", result_text, re.DOTALL | re.IGNORECASE)
    if explanation_match:
        parsed["explanation"] = explanation_match.group(1).strip()
        if parsed["explanation"].lower() == 'none': parsed["explanation"] = None

    # Extract Doubt
    doubt_match = re.search(r"DOUBT:\s*(.*?)(?=\s*CODE RANGE:|$)", result_text, re.DOTALL | re.IGNORECASE)
    if doubt_match:
        parsed["doubt"] = doubt_match.group(1).strip()
        if parsed["doubt"].lower() == 'none': parsed["doubt"] = None

    # Extract Code Range
    code_range_match = re.search(r"CODE RANGE:\s*(.*)", result_text, re.IGNORECASE)
    if code_range_match:
        parsed["code_range"] = code_range_match.group(1).strip()
        if parsed["code_range"].lower() == 'none': parsed["code_range"] = None
    elif not parsed["code_range"]: # Fallback: Find Dxxxx-Dxxxx patterns if CODE RANGE: not found
        matches = re.findall(r"(D\d{4}-D\d{4})", result_text)
        if matches:
            parsed["code_range"] = ", ".join(matches)

    return parsed

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
        self.registry.register("D4186", lambda x: {"codes": [{"code": "D4186"}]} if "outcome assessment" in x.lower() else None, # Simplified lambda for consistency
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
    
    def analyze_diagnostic(self, scenario: str) -> dict: # Changed return type
        """Analyze the scenario and return parsed explanation, doubt, and code range."""
        try:
            print(f"Analyzing diagnostic scenario: {scenario[:100]}...")
            raw_result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            parsed_result = _parse_llm_topic_output(raw_result) # Use helper
            print(f"Diagnostic analyze result: Exp={parsed_result['explanation']}, Doubt={parsed_result['doubt']}, Range={parsed_result['code_range']}")
            return parsed_result # Return parsed dictionary
        except Exception as e:
            print(f"Error in analyze_diagnostic: {str(e)}")
            return {"explanation": None, "doubt": None, "code_range": None, "error": str(e)}
    
    async def activate_diagnostic(self, scenario: str) -> dict: # Changed return type and logic
        """Activate relevant subtopics in parallel and return detailed results including explanation and doubt."""
        final_result = {"explanation": None, "doubt": None, "code_range": None, "activated_subtopics": [], "codes": []}
        try:
            # Get the parsed analysis (explanation, doubt, code_range)
            topic_analysis_result = self.analyze_diagnostic(scenario)
            
            # Store analysis results
            final_result["explanation"] = topic_analysis_result.get("explanation")
            final_result["doubt"] = topic_analysis_result.get("doubt")
            final_result["code_range"] = "D0100-D0999" # Hardcoded for now, might need dynamic lookup
            
            code_range_string = topic_analysis_result.get("code_range")
            
            if code_range_string:
                print(f"Diagnostic activate using code ranges: {code_range_string}")
                # Activate subtopics in parallel using the registry with the parsed code range string
                subtopic_results = await self.registry.activate_all(scenario, code_range_string)
                
                # Aggregate codes from the subtopic results
                aggregated_codes = []
                activated_subtopic_names = set() # Collect names of subtopics that returned codes

                subtopic_results_list = subtopic_results.get("topic_result", [])
                for sub_result in subtopic_results_list:
                    if isinstance(sub_result, dict) and not sub_result.get("error"):
                        codes_from_sub = sub_result.get("codes", [])
                        if codes_from_sub:
                            # Add subtopic name or keep original topic from sub-result if needed
                            # For now, just aggregate the code dicts
                            aggregated_codes.extend(codes_from_sub)
                            # Try to get a cleaner subtopic name
                            subtopic_name_match = re.match(r"^(.*?)\s*\(", sub_result.get("topic", ""))
                            if subtopic_name_match:
                                activated_subtopic_names.add(subtopic_name_match.group(1).strip())
                            else:
                                activated_subtopic_names.add(sub_result.get("topic", "Unknown Subtopic"))

                final_result["activated_subtopics"] = sorted(list(activated_subtopic_names))
                final_result["codes"] = aggregated_codes # Assign the flattened list of code dicts
            else:
                print("No applicable code ranges found in diagnostic analysis.")
                
            return final_result
            
        except Exception as e:
            print(f"Error in diagnostic activation: {str(e)}")
            final_result["error"] = str(e)
            return final_result
    
    async def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = await self.activate_diagnostic(scenario)
        print(f"\n=== DIAGNOSTIC ANALYSIS RESULT ===")
        print(f"EXPLANATION: {result.get('explanation', 'N/A')}")
        print(f"DOUBT: {result.get('doubt', 'N/A')}")
        print(f"CODE RANGE: {result.get('code_range', 'None')}")
        print(f"ACTIVATED SUBTOPICS: {', '.join(result.get('activated_subtopics', []))}")
        print(f"SPECIFIC CODES: {result.get('codes', [])}")

diagnostic_service = DiagnosticServices()
# Example usage
if __name__ == "__main__":
    async def main():
        scenario = input("Enter a diagnostic dental scenario: ")
        await diagnostic_service.run_analysis(scenario)
    
    asyncio.run(main())