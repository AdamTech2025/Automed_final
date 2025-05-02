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


# Import service objects from subtopics with fallback mechanism
try:
    from subtopics.Prosthodontics_Fixed.fixed_partial_denture_pontics import fixed_partial_denture_pontics_service
    from subtopics.Prosthodontics_Fixed.fixed_partial_denture_retainers_inlays_onlays import fixed_partial_denture_retainers_inlays_onlays_service
    from subtopics.Prosthodontics_Fixed.fixed_partial_denture_retainers_crowns import fixed_partial_denture_retainers_crowns_service
    from subtopics.Prosthodontics_Fixed.other_fixed_partial_denture_services import other_fixed_partial_denture_services_service
except ImportError as e:
    print(f"Warning: Could not import subtopics for Prosthodontics Fixed: {str(e)}")
    print(f"Current sys.path: {sys.path}")
    # Define fallback functions
    def activate_fixed_partial_denture_pontics(scenario): return None
    def activate_fixed_partial_denture_retainers_inlays_onlays(scenario): return None
    def activate_fixed_partial_denture_retainers_crowns(scenario): return None
    def activate_other_fixed_partial_denture_services(scenario): return None

# Helper function removed


class FixedProsthodonticsServices:
    """Class to analyze and activate fixed prosthodontics services based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.db = MedicalCodingDB()
        self.prompt_template = self._create_prompt_template()
        self.registry = SubtopicRegistry()
        self._register_subtopics()
        
    def _register_subtopics(self):
        """Register all subtopics for parallel activation."""
        try:
            self.registry.register("D6205-D6253", fixed_partial_denture_pontics_service.activate_fixed_partial_denture_pontics, 
                                "Fixed Partial Denture Pontics (D6205-D6253)")
            self.registry.register("D6545-D6634", fixed_partial_denture_retainers_inlays_onlays_service.activate_fixed_partial_denture_retainers_inlays_onlays, 
                                "Fixed Partial Denture Retainers — Inlays/Onlays (D6545-D6634)")
            self.registry.register("D6710-D6793", fixed_partial_denture_retainers_crowns_service.activate_fixed_partial_denture_retainers_crowns, 
                                "Fixed Partial Denture Retainers — Crowns (D6710-D6793)")
            self.registry.register("D6920-D6999", other_fixed_partial_denture_services_service.activate_other_fixed_partial_denture_services, 
                                "Other Fixed Partial Denture Services (D6920-D6999)")
        except Exception as e:
            print(f"Error registering subtopics: {str(e)}")
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing fixed prosthodontics services."""
        prompt_data = self.db.get_topic_prompt("prosthodontics_fixed_prompt")           
        instruction_data = self.db.get_instruction("instruction_prompt")
        print("###***Prompt Data Successfully Retrived from Database***###, ", "prosthodontics_fixed_prompt")
        if not prompt_data or not prompt_data.get("template"):
            raise ValueError("Failed to retrieve prompt 'prosthodontics_fixed_prompt' from database")
        template = prompt_data["template"]
        print(f"Template: {template}")
        return PromptTemplate(
            template=f"""
            {template}
            {instruction_data}
            """,
            input_variables=["scenario"]
        )
    
    def analyze_prosthodontics_fixed(self, scenario: str) -> dict: # Changed return type to dict
        """Analyze the scenario and return raw LLM output and the applicable code range string."""
        result = {"raw_output": None, "code_range": None}
        try:
            print(f"Analyzing fixed prosthodontics scenario: {scenario[:100]}...")
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
                 print(f"Prosthodontics Fixed analyze result: Found Code Range={code_range_string}")
            else:
                 print("Prosthodontics Fixed analyze result: No applicable code range found in raw output.")
                    
            return result
                    
        except Exception as e:
            print(f"Error in analyze_prosthodontics_fixed: {str(e)}")
            result["error"] = str(e)
            return result
    
    async def activate_prosthodontics_fixed(self, scenario: str) -> dict: # Changed return type and logic
        """Activate relevant subtopics in parallel based on LLM-identified code ranges."""
        # Consistent final result structure
        final_result = {"raw_topic_data": None, "code_range": "D6200-D6999", "activated_subtopics": [], "subtopics_data": [], "error": None}
        try:
            # Get the analysis result dictionary
            analysis_result = self.analyze_prosthodontics_fixed(scenario)
            
            # Store raw output
            final_result["raw_topic_data"] = analysis_result.get("raw_output")

            # Check for analysis errors
            if analysis_result.get("error"):
                final_result["error"] = f"Analysis Error: {analysis_result['error']}"
                return final_result
            
            # Get code range string
            code_range_string = analysis_result.get("code_range")
            
            if code_range_string:
                print(f"Prosthodontics Fixed activate using code ranges: {code_range_string}")
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
                print("No applicable code ranges identified by LLM for fixed prosthodontics analysis.")
                
            # Clear error key if no error occurred
            if final_result.get("error") is None:
                 try: del final_result["error"]
                 except KeyError: pass

            return final_result
            
        except Exception as e:
            print(f"Error in fixed prosthodontics activation: {str(e)}")
            final_result["error"] = str(e)
            return final_result
    
    async def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = await self.activate_prosthodontics_fixed(scenario)
        print(f"\n=== FIXED PROSTHODONTICS ANALYSIS RESULT ===")
        # Updated printing logic
        print(f"RAW TOPIC DATA:\n---\n{result.get('raw_topic_data', 'N/A')}\n---")
        print(f"OVERALL TOPIC CODE RANGE: {result.get('code_range', 'None')}")
        print(f"ACTIVATED SUBTOPICS: {', '.join(result.get('activated_subtopics', []))}")
        print(f"SUBTOPICS DATA: {result.get('subtopics_data', [])}")
        if 'error' in result:
            print(f"ERROR: {result['error']}")

prosthodontics_service = FixedProsthodonticsServices()
# Example usage
if __name__ == "__main__":
    async def main():
        prosthodontics_service = FixedProsthodonticsServices()
        scenario = input("Enter a fixed prosthodontics dental scenario: ")
        await prosthodontics_service.run_analysis(scenario)
    
    asyncio.run(main())