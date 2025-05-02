import os
import sys
import asyncio
import re # Added for parsing
from langchain.prompts import PromptTemplate
from llm_services import LLMService, get_service, set_model, set_temperature
from database import MedicalCodingDB
from sub_topic_registry import SubtopicRegistry

# Add the root directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)


from subtopics.diagnostics.clinicaloralevaluation import clinical_oral_evaluations_service
from subtopics.diagnostics.diagnosticimaging import diagnostic_imaging_service
from subtopics.diagnostics.oralpathologylaboratory import oral_pathology_laboratory_service
from subtopics.diagnostics.prediagnosticservices import prediagnostic_service
from subtopics.diagnostics.testsandexaminations import tests_service
from database import MedicalCodingDB
# Helper function removed


class DiagnosticServices:
    """Class to analyze and activate diagnostic services based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.db = MedicalCodingDB()
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
        prompt_data = self.db.get_topic_prompt("diagnostic_prompt")
        instruction_data = self.db.get_instruction("instruction_prompt")
        if not prompt_data or not prompt_data.get("template"):
            raise ValueError("Failed to retrieve prompt 'diagnostic_services_prompt' from database")
        template = prompt_data["template"]
        
        return PromptTemplate(
            template=f"""
            {template}
            {instruction_data}
            """,
            input_variables=["scenario"]
        )
    
    def analyze_diagnostic(self, scenario: str) -> dict: # Changed return type to dict
        """Analyze the scenario and return raw LLM output and the applicable code range string."""
        result = {"raw_output": None, "code_range": None}
        try:
            print(f"Analyzing diagnostic scenario: {scenario[:100]}...")
            raw_result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            result["raw_output"] = raw_result # Store raw output
            
            # Extract Code Range directly using regex based on the expected format
            code_range_match = re.search(r"CODE RANGE:\s*(.*)", raw_result, re.IGNORECASE | re.DOTALL)
            code_range_string = None # Initialize
            
            if code_range_match:
                extracted_string = code_range_match.group(1).strip()
                # Handle potential 'none' response
                if extracted_string.lower() != 'none':
                    code_range_string = extracted_string
            else:
                # Fallback: Try to find Dxxxx-Dxxxx patterns if "CODE RANGE:" marker isn't found
                fallback_matches = re.findall(r"(D\d{4}-D\d{4})", raw_result)
                if fallback_matches:
                    code_range_string = ", ".join(fallback_matches)

            result["code_range"] = code_range_string # Store extracted range (or None)

            if code_range_string:
                 print(f"Diagnostic analyze result: Found Code Range={code_range_string}")
            else:
                 print("Diagnostic analyze result: No applicable code range found in raw output.")
                    
            return result
                    
        except Exception as e:
            print(f"Error in analyze_diagnostic: {str(e)}")
            result["error"] = str(e) # Add error to result
            return result # Return result even on error
    
    async def activate_diagnostic(self, scenario: str) -> dict: # Changed return type and logic
        """Activate relevant subtopics in parallel based on LLM-identified code ranges."""
        # Updated final result structure
        final_result = {"raw_topic_data": None, "code_range": "D0100-D0999", "activated_subtopics": [], "subtopics_data": [], "error": None}
        try:
            # Get the analysis result dictionary
            analysis_result = self.analyze_diagnostic(scenario)
            
            # Store the raw output
            final_result["raw_topic_data"] = analysis_result.get("raw_output")

            # Check for errors during analysis
            if analysis_result.get("error"):
                final_result["error"] = f"Analysis Error: {analysis_result['error']}"
                if final_result["error"] is None: del final_result["error"]
                return final_result
            
            # Get the code range string
            code_range_string = analysis_result.get("code_range")
            
            if code_range_string:
                print(f"Diagnostic activate using code ranges: {code_range_string}")
                # Activate subtopics in parallel
                # activate_all now returns a list of dictionaries directly
                subtopic_results_list = await self.registry.activate_all(scenario, code_range_string)
                
                # Aggregate results
                aggregated_subtopic_data = [] # Renamed for clarity
                activated_subtopic_names = set()

                # Directly iterate over the returned list
                for sub_result in subtopic_results_list:
                    # sub_result is a dict like: {"topic": ..., "code_range": ..., "raw_result": ..., "error": ...}
                    if isinstance(sub_result, dict):
                        topic_name = sub_result.get("topic", "Unknown Subtopic")
                        if sub_result.get("error"):
                            print(f"  Error activating subtopic '{topic_name}': {sub_result['error']}")
                            # Optionally store the error if needed
                            # aggregated_subtopic_data.append({"topic": topic_name, "error": sub_result['error']})
                        else:
                            # Add the raw result directly to the list
                            aggregated_subtopic_data.append(sub_result) # Store the whole dict including raw_result
                            activated_subtopic_names.add(topic_name) # Add name if successful
                    else:
                         print(f"  Warning: Unexpected item type in subtopic results list: {type(sub_result)}")

                final_result["activated_subtopics"] = sorted(list(activated_subtopic_names))
                final_result["subtopics_data"] = aggregated_subtopic_data # Store the list of raw results/errors
            else:
                print("No applicable code ranges identified by LLM for diagnostic analysis.")
                
            # Clear the error key if no error occurred
            if final_result.get("error") is None:
                 try: del final_result["error"]
                 except KeyError: pass

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
        # Updated printing logic
        print(f"RAW TOPIC DATA:\n---\n{result.get('raw_topic_data', 'N/A')}\n---")
        print(f"OVERALL TOPIC CODE RANGE: {result.get('code_range', 'None')}")
        print(f"ACTIVATED SUBTOPICS: {', '.join(result.get('activated_subtopics', []))}")
        print(f"SUBTOPICS DATA: {result.get('subtopics_data', [])}")
        if 'error' in result:
            print(f"ERROR: {result['error']}")

diagnostic_service = DiagnosticServices()
# Example usage
if __name__ == "__main__":
    async def main():
        scenario = input("Enter a diagnostic dental scenario: ")
        await diagnostic_service.run_analysis(scenario)
    
    asyncio.run(main())