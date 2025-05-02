import os
import sys
import asyncio
import re # Added for parsing
from langchain.prompts import PromptTemplate
from llm_services import LLMService, get_service, set_model, set_temperature
from database import MedicalCodingDB
from sub_topic_registry import SubtopicRegistry

# Add the project root to the path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

# Import modules

# Import subtopics - Use absolute imports
try:
    from subtopics.implantservices.pre_surgical import pre_surgical_service
    from subtopics.implantservices.surgical_services import surgical_service
    from subtopics.implantservices.implant_supported_prosthetics import implant_supported_prosthetics_service
    from subtopics.implantservices.removable_dentures import removable_dentures_service
    from subtopics.implantservices.fixed_dentures import fixed_dentures_service
    from subtopics.implantservices.abutment_crowns import abutment_crowns_service
    from subtopics.implantservices.implant_crowns import implant_crowns_service
    from subtopics.implantservices.fpd_abutment import fpd_abutment_service
    from subtopics.implantservices.fpd_implant import fpd_implant_service
    from subtopics.implantservices.other_services import other_implant_services_service
except ImportError as e:
    print(f"Warning: Could not import subtopics for implantservices: {str(e)}")
    print(f"Current sys.path: {sys.path}")
    # Define fallback functions
    def activate_pre_surgical(scenario): return None
    def activate_surgical_services(scenario): return None
    def activate_implant_supported_prosthetics(scenario): return None
    def activate_implant_supported_removable_dentures(scenario): return None
    def activate_implant_supported_fixed_dentures(scenario): return None
    def activate_single_crowns_abutment(scenario): return None
    def activate_single_crowns_implant(scenario): return None
    def activate_fpd_abutment(scenario): return None
    def activate_fpd_implant(scenario): return None
    def activate_other_implant_services(scenario): return None

# Helper function removed


class ImplantServices:
    """Class to analyze and activate implant services based on dental scenarios."""
    
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
            # Note: Correcting range for D6190 as it's a single code, not a range end
            self.registry.register("D6190", pre_surgical_service.activate_pre_surgical, 
                                "Pre-Surgical Services (D6190)") 
            self.registry.register("D6010-D6199", surgical_service.activate_surgical_services, # Overlaps with D6190 slightly, registry should handle priority/uniqueness if needed
                                "Surgical Services (D6010-D6199)")
            self.registry.register("D6051-D6078", implant_supported_prosthetics_service.activate_implant_supported_prosthetics, 
                                "Implant Supported Prosthetics (D6051-D6078)")
            self.registry.register("D6110-D6119", removable_dentures_service.activate_removable_dentures, 
                                "Implant Supported Removable Dentures (D6110-D6119)")
            self.registry.register("D6090-D6095", fixed_dentures_service.activate_implant_supported_fixed_dentures, 
                                "Implant Supported Fixed Dentures (D6090-D6095)")
            self.registry.register("D6058-D6077", abutment_crowns_service.activate_single_crowns_abutment, 
                                "Single Crowns, Abutment Supported (D6058-D6077)")
            self.registry.register("D6065-D6067", implant_crowns_service.activate_single_crowns_implant, 
                                "Single Crowns, Implant Supported (D6065-D6067)")
            self.registry.register("D6071-D6074", fpd_abutment_service.activate_fpd_abutment, 
                                "Fixed Partial Denture, Abutment Supported (D6071-D6074)")
            # Note: Correcting range for D6075 as it's a single code
            self.registry.register("D6075", fpd_implant_service.activate_fpd_implant, 
                                "Fixed Partial Denture, Implant Supported (D6075)")
            self.registry.register("D6080-D6199", other_implant_services_service.activate_other_implant_services, # Also overlaps slightly
                                "Other Implant Services (D6080-D6199)")
        except Exception as e:
            print(f"Error registering subtopics: {str(e)}")
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing implant services."""
        prompt_data = self.db.get_topic_prompt("implant_services_prompt")
        instruction_data = self.db.get_instruction("instruction_prompt")
        print("###***Prompt Data Successfully Retrived from Database***###, ", "implant_services_prompt")
        if not prompt_data or not prompt_data.get("template"):
            raise ValueError("Failed to retrieve prompt 'implant_services_prompt' from database")
        template = prompt_data["template"]
        print(f"Template: {template}")
        return PromptTemplate(
            template=f"""
            {template}
            {instruction_data}
            """,
            input_variables=["scenario"]
        )
    
    def analyze_implant_services(self, scenario: str) -> dict: # Changed return type to dict
        """Analyze the scenario and return raw LLM output and the applicable code range string."""
        result = {"raw_output": None, "code_range": None}
        try:
            print(f"Analyzing implant services scenario: {scenario[:100]}...")
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
                 print(f"Implant Services analyze result: Found Code Range={code_range_string}")
            else:
                 print("Implant Services analyze result: No applicable code range found in raw output.")
                    
            return result
                    
        except Exception as e:
            print(f"Error in analyze_implant_services: {str(e)}")
            result["error"] = str(e)
            return result
    
    async def activate_implant_services(self, scenario: str) -> dict: # Changed return type and logic
        """Activate relevant subtopics in parallel based on LLM-identified code ranges."""
        # Consistent final result structure
        final_result = {"raw_topic_data": None, "code_range": "D6000-D6199", "activated_subtopics": [], "subtopics_data": [], "error": None}
        try:
            # Get the analysis result dictionary
            analysis_result = self.analyze_implant_services(scenario)
            
            # Store raw output
            final_result["raw_topic_data"] = analysis_result.get("raw_output")

            # Check for analysis errors
            if analysis_result.get("error"):
                final_result["error"] = f"Analysis Error: {analysis_result['error']}"
                return final_result
            
            # Get code range string
            code_range_string = analysis_result.get("code_range")
            
            if code_range_string:
                print(f"Implant Services activate using code ranges: {code_range_string}")
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
                print("No applicable code ranges identified by LLM for implant services analysis.")
                
            # Clear error key if no error occurred
            if final_result.get("error") is None:
                 try: del final_result["error"]
                 except KeyError: pass

            return final_result
            
        except Exception as e:
            print(f"Error in implant services activation: {str(e)}")
            final_result["error"] = str(e)
            return final_result
    
    async def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = await self.activate_implant_services(scenario)
        print(f"\n=== IMPLANT SERVICES ANALYSIS RESULT ===")
        # Updated printing logic
        print(f"RAW TOPIC DATA:\n---\n{result.get('raw_topic_data', 'N/A')}\n---")
        print(f"OVERALL TOPIC CODE RANGE: {result.get('code_range', 'None')}")
        print(f"ACTIVATED SUBTOPICS: {', '.join(result.get('activated_subtopics', []))}")
        print(f"SUBTOPICS DATA: {result.get('subtopics_data', [])}")
        if 'error' in result:
            print(f"ERROR: {result['error']}")

implant_service = ImplantServices()
# Example usage
if __name__ == "__main__":
    async def main():
        implant_service = ImplantServices()
        scenario = input("Enter an implant services dental scenario: ")
        await implant_service.run_analysis(scenario)
    
    asyncio.run(main())