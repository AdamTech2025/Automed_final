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


from subtopics.Prosthodontics_Removable.complete_dentures import CompleteDenturesServices
from subtopics.Prosthodontics_Removable.adjustments_to_dentures import AdjustmentsToDenturesServices
from subtopics.Prosthodontics_Removable.denture_rebase_procedures import DentureRebaseProceduresServices
from subtopics.Prosthodontics_Removable.interim_prosthesis import InterimProsthesisServices
from subtopics.Prosthodontics_Removable.other_removable_prosthetic_services import OtherRemovableProstheticServices
from subtopics.Prosthodontics_Removable.partial_denture import PartialDentureServices
from subtopics.Prosthodontics_Removable.repairs_to_complete_dentures import RepairsToCompleteDenturesServices
from subtopics.Prosthodontics_Removable.repairs_to_partial_dentures import RepairsToPartialDenturesServices
from subtopics.Prosthodontics_Removable.tissue_conditioning import TissueConditioningServices
from subtopics.Prosthodontics_Removable.unspecified_removable_prosthodontic_procedure import UnspecifiedRemovableProsthodonticProcedureServices
from subtopics.Prosthodontics_Removable.denture_reline_procedures import DentureRelineProceduresServices

# Helper function removed


class RemovableProsthodonticsServices:
    """Class to analyze and activate removable prosthodontics services based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.db = MedicalCodingDB()
        self.prompt_template = self._create_prompt_template()
        
        # Removed initialization of subtopic services here, they are called statically/via class methods now
        
        self.registry = SubtopicRegistry()
        self._register_subtopics()
    
    def _register_subtopics(self):
        """Register all subtopics for parallel activation."""
        # Assuming subtopic services are designed to be called statically or via instances if needed
        # Correcting calls to point to the activation methods if they exist
        # If they are instance methods, need to instantiate the classes first.
        # Let's assume they are structured like `subtopic_service.activate_subtopic` for now.
        
        # Example assuming static/class methods or module-level functions:
        # Note: The actual function names might differ (e.g., activate_... vs. process_...)
        # Need to verify the actual structure of the subtopic modules.
        
        # Using placeholder names - these need verification against actual subtopic code.
        self.registry.register("D5110-D5140", CompleteDenturesServices().activate_complete_dentures, # Assumes instance method
                            "Complete Dentures (D5110-D5140)")
        self.registry.register("D5211-D5286", PartialDentureServices().activate_partial_denture, 
                            "Partial Denture (D5211-D5286)")
        self.registry.register("D5410-D5422", AdjustmentsToDenturesServices().activate_adjustments_to_dentures, 
                            "Adjustments to Dentures (D5410-D5422)")
        self.registry.register("D5511-D5520", RepairsToCompleteDenturesServices().activate_repairs_to_complete_dentures, 
                            "Repairs to Complete Dentures (D5511-D5520)")
        self.registry.register("D5611-D5671", RepairsToPartialDenturesServices().activate_repairs_to_partial_dentures, 
                            "Repairs to Partial Dentures (D5611-D5671)")
        self.registry.register("D5710-D5725", DentureRebaseProceduresServices().activate_denture_rebase_procedures, 
                            "Denture Rebase Procedures (D5710-D5725)")
        self.registry.register("D5730-D5761", DentureRelineProceduresServices().activate_denture_reline_procedures, 
                            "Denture Reline Procedures (D5730-D5761)")
        self.registry.register("D5810-D5821", InterimProsthesisServices().activate_interim_prosthesis, 
                            "Interim Prosthesis (D5810-D5821)")
        # Grouping Other Removable Prosthetic Services under D5863-D5899 (typical range)
        self.registry.register("D5863-D5876", OtherRemovableProstheticServices().activate_other_removable_prosthetic_services, 
                            "Other Removable Prosthetic Services (D5863-D5876)") 
        self.registry.register("D5850-D5851", TissueConditioningServices().activate_tissue_conditioning, # D5850-D5851 is specific to tissue conditioning
                            "Tissue Conditioning (D5850-D5851)")
        # D5899 is often unspecified
        self.registry.register("D5899", UnspecifiedRemovableProsthodonticProcedureServices().activate_unspecified_removable_prosthodontic_procedure, 
                            "Unspecified Removable Prosthodontic Procedure (D5899)")
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing removable prosthodontics services."""
        prompt_data = self.db.get_topic_prompt("prosthodontics_removable_prompt")
        instruction_data = self.db.get_instruction("instruction_prompt")
        print("###***Prompt Data Successfully Retrived from Database***###, ", "prosthodontics_removable_prompt")
        if not prompt_data or not prompt_data.get("template"):
            raise ValueError("Failed to retrieve prompt 'prosthodontics_removable_prompt' from database")
        template = prompt_data["template"]
        print(f"Template: {template}")
        return PromptTemplate(
            template=f"""
            {template}
            {instruction_data}
            """,
            input_variables=["scenario"]
        )
    
    def analyze_prosthodontics_removable(self, scenario: str) -> dict: # Changed return type to dict
        """Analyze the scenario and return raw LLM output and the applicable code range string."""
        result = {"raw_output": None, "code_range": None}
        try:
            print(f"Analyzing removable prosthodontics scenario: {scenario[:100]}...")
            raw_result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            result["raw_output"] = raw_result # Store raw output
            
            # Extract Code Range directly using regex
            code_range_match = re.search(r"CODE RANGE:\s*(.*)", raw_result, re.IGNORECASE | re.DOTALL)
            code_range_string = None
            
            if code_range_match:
                extracted_string = code_range_match.group(1).strip()
                if extracted_string.lower() != 'none':
                    code_range_string = extracted_string
            else:
                fallback_matches = re.findall(r"(D\d{4}-D\d{4})", raw_result)
                if fallback_matches:
                    code_range_string = ", ".join(fallback_matches)

            result["code_range"] = code_range_string

            if code_range_string:
                 print(f"Prosthodontics Removable analyze result: Found Code Range={code_range_string}")
            else:
                 print("Prosthodontics Removable analyze result: No applicable code range found in raw output.")
                    
            return result
                    
        except Exception as e:
            print(f"Error in analyze_prosthodontics_removable: {str(e)}")
            result["error"] = str(e)
            return result
    
    async def activate_prosthodontics_removable(self, scenario: str) -> dict: # Changed return type and logic
        """Activate relevant subtopics in parallel based on LLM-identified code ranges."""
        # Consistent final result structure
        final_result = {"raw_topic_data": None, "code_range": "D5000-D5899", "activated_subtopics": [], "subtopics_data": [], "error": None}
        try:
            # Get the analysis result dictionary
            analysis_result = self.analyze_prosthodontics_removable(scenario)
            
            # Store raw output
            final_result["raw_topic_data"] = analysis_result.get("raw_output")

            # Check for analysis errors
            if analysis_result.get("error"):
                final_result["error"] = f"Analysis Error: {analysis_result['error']}"
                return final_result
            
            # Get code range string
            code_range_string = analysis_result.get("code_range")
            
            if code_range_string:
                print(f"Prosthodontics Removable activate using code ranges: {code_range_string}")
                # Activate subtopics
                # activate_all returns a list of dictionaries directly
                subtopic_results_list = await self.registry.activate_all(scenario, code_range_string)
                
                # Aggregate results
                aggregated_subtopic_data = [] # Stores the raw results/errors from subtopics
                activated_subtopic_names = set()

                # Directly iterate over the returned list
                for sub_result in subtopic_results_list:
                    if isinstance(sub_result, dict):
                        topic_name = sub_result.get("topic", "Unknown Subtopic")
                        if sub_result.get("error"):
                            print(f"  Error activating subtopic '{topic_name}': {sub_result['error']}")
                            aggregated_subtopic_data.append(sub_result) # Store error entry
                        else:
                            aggregated_subtopic_data.append(sub_result) # Store successful raw result
                            activated_subtopic_names.add(topic_name)
                    else:
                        print(f"  Warning: Unexpected item type in subtopic results list: {type(sub_result)}")

                final_result["activated_subtopics"] = sorted(list(activated_subtopic_names))
                final_result["subtopics_data"] = aggregated_subtopic_data # Store the list of raw results/errors
            else:
                print("No applicable code ranges identified by LLM for removable prosthodontics analysis.")
                
            # Clear error key if no error occurred
            if final_result.get("error") is None:
                 try: del final_result["error"]
                 except KeyError: pass

            return final_result
            
        except Exception as e:
            print(f"Error in removable prosthodontics activation: {str(e)}")
            final_result["error"] = str(e)
            return final_result
    
    async def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = await self.activate_prosthodontics_removable(scenario)
        print(f"\n=== REMOVABLE PROSTHODONTICS ANALYSIS RESULT ===")
        # Updated printing logic
        print(f"RAW TOPIC DATA:\n---\n{result.get('raw_topic_data', 'N/A')}\n---")
        print(f"OVERALL TOPIC CODE RANGE: {result.get('code_range', 'None')}")
        print(f"ACTIVATED SUBTOPICS: {', '.join(result.get('activated_subtopics', []))}")
        print(f"SUBTOPICS DATA: {result.get('subtopics_data', [])}")
        if 'error' in result:
            print(f"ERROR: {result['error']}")

prosthodontics_service = RemovableProsthodonticsServices()
# Example usage
if __name__ == "__main__":
    async def main():
        prosthodontics_service = RemovableProsthodonticsServices()
        scenario = input("Enter a removable prosthodontics dental scenario: ")
        await prosthodontics_service.run_analysis(scenario)
    
    asyncio.run(main())