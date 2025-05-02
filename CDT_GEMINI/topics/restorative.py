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


from subtopics.Restorative.amalgam_restorations import AmalgamRestorationsServices
from subtopics.Restorative.resin_based_composite_restorations import ResinBasedCompositeRestorationsServices
from subtopics.Restorative.gold_foil_restorations import GoldFoilRestorationsServices
from subtopics.Restorative.inlays_and_onlays import InlaysAndOnlaysServices
from subtopics.Restorative.crowns import CrownsServices
from subtopics.Restorative.other_restorative_services import OtherRestorativeServices

class RestorativeServices:
    """Class to analyze and activate restorative services based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.db = MedicalCodingDB()
        self.prompt_template = self._create_prompt_template()
    
        # Initialize the subtopic service classes - needed if calling instance methods
        self.amalgam_restorations = AmalgamRestorationsServices(self.llm_service)
        self.resin_based_composite_restorations = ResinBasedCompositeRestorationsServices(self.llm_service)
        self.gold_foil_restorations = GoldFoilRestorationsServices(self.llm_service)
        self.inlays_and_onlays = InlaysAndOnlaysServices(self.llm_service)
        self.crowns = CrownsServices(self.llm_service)
        self.other_restorative_services = OtherRestorativeServices(self.llm_service)
        
        self.registry = SubtopicRegistry()
        self._register_subtopics()
    
    def _register_subtopics(self):
        """Register all subtopics for parallel activation."""
        # Assuming instance methods are used based on __init__
        self.registry.register("D2140-D2161", self.amalgam_restorations.activate_amalgam_restorations, 
                            "Amalgam Restorations (D2140-D2161)")
        self.registry.register("D2330-D2394", self.resin_based_composite_restorations.activate_resin_based_composite_restorations, 
                            "Resin-Based Composite Restorations (D2330-D2394)")
        self.registry.register("D2410-D2430", self.gold_foil_restorations.activate_gold_foil_restorations, 
                            "Gold Foil Restorations (D2410-D2430)")
        self.registry.register("D2510-D2664", self.inlays_and_onlays.activate_inlays_and_onlays, 
                            "Inlays and Onlays (D2510-D2664)")
        self.registry.register("D2710-D2799", self.crowns.activate_crowns, 
                            "Crowns (D2710-D2799)")
        self.registry.register("D2910-D2999", self.other_restorative_services.activate_other_restorative_services, 
                            "Other Restorative Services (D2910-D2999)")
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing restorative services."""
        prompt_data = self.db.get_topic_prompt("restorative_prompt")
        instruction_data = self.db.get_instruction("instruction_prompt")
        print("###***Prompt Data Successfully Retrived from Database***###, ", "restorative_prompt")
        if not prompt_data or not prompt_data.get("template"):
            raise ValueError("Failed to retrieve prompt 'restorative_prompt' from database")
        template = prompt_data["template"]
        print(f"Template: {template}")
        return PromptTemplate(
            template=f"""
            {template}
            {instruction_data}
            """,
            input_variables=["scenario"]
            )
    
    def analyze_restorative(self, scenario: str) -> dict: # Changed return type to dict
        """Analyze the scenario and return raw LLM output and the applicable code range string."""
        result = {"raw_output": None, "code_range": None}
        try:
            print(f"Analyzing restorative scenario: {scenario[:100]}...")
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
                 print(f"Restorative analyze result: Found Code Range={code_range_string}")
            else:
                 print("Restorative analyze result: No applicable code range found in raw output.")
                    
            return result
                    
        except Exception as e:
            print(f"Error in analyze_restorative: {str(e)}")
            result["error"] = str(e)
            return result
    
    async def activate_restorative(self, scenario: str) -> dict: # Changed return type and logic
        """Activate relevant subtopics in parallel based on LLM-identified code ranges."""
        # Consistent final result structure
        final_result = {"raw_topic_data": None, "code_range": "D2000-D2999", "activated_subtopics": [], "subtopics_data": [], "error": None}
        try:
            # Get the analysis result dictionary
            analysis_result = self.analyze_restorative(scenario)
            
            # Store raw output
            final_result["raw_topic_data"] = analysis_result.get("raw_output")

            # Check for analysis errors
            if analysis_result.get("error"):
                final_result["error"] = f"Analysis Error: {analysis_result['error']}"
                return final_result
            
            # Get code range string
            code_range_string = analysis_result.get("code_range")
            
            if code_range_string:
                print(f"Restorative activate using code ranges: {code_range_string}")
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
                print("No applicable code ranges identified by LLM for restorative analysis.")
                
            # Clear error key if no error occurred
            if final_result.get("error") is None:
                 try: del final_result["error"]
                 except KeyError: pass

            return final_result
            
        except Exception as e:
            print(f"Error in restorative activation: {str(e)}")
            final_result["error"] = str(e)
            return final_result
    
    async def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = await self.activate_restorative(scenario)
        print(f"\n=== RESTORATIVE ANALYSIS RESULT ===")
        # Updated printing logic
        print(f"RAW TOPIC DATA:\n---\n{result.get('raw_topic_data', 'N/A')}\n---")
        print(f"OVERALL TOPIC CODE RANGE: {result.get('code_range', 'None')}")
        print(f"ACTIVATED SUBTOPICS: {', '.join(result.get('activated_subtopics', []))}")
        print(f"SUBTOPICS DATA: {result.get('subtopics_data', [])}")
        if 'error' in result:
            print(f"ERROR: {result['error']}")

restorative_service = RestorativeServices()
# Example usage
if __name__ == "__main__":
    async def main():
        restorative_service = RestorativeServices()
        scenario = input("Enter a restorative dental scenario: ")
        await restorative_service.run_analysis(scenario)
    
    asyncio.run(main())