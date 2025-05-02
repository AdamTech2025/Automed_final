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


# Import subtopics with fallback mechanism
try:
    from subtopics.Endodontics.apexification import apexification_service
    from subtopics.Endodontics.apicoectomy import apicoectomy_service
    from subtopics.Endodontics.endodonticretreatment import endodontic_retreatment_service
    from subtopics.Endodontics.endodontictherapy import endodontic_therapy_service
    from subtopics.Endodontics.otherendodontic import other_endodontic_service
    from subtopics.Endodontics.pulpcapping import pulpcapping_service
    from subtopics.Endodontics.pulpotomy import pulpotomy_service
    from subtopics.Endodontics.primaryteeth import primary_teeth_therapy_service
    from subtopics.Endodontics.pulpalregeneration import pulpal_regeneration_service
except ImportError:
    print("Warning: Could not import subtopics for Endodontics. Using fallback functions.")
    # Define fallback functions
    def activate_pulp_capping(scenario): return None
    def activate_pulpotomy(scenario): return None
    def activate_primary_teeth_therapy(scenario): return None
    def activate_endodontic_therapy(scenario): return None
    def activate_endodontic_retreatment(scenario): return None
    def activate_apexification(scenario): return None
    def activate_pulpal_regeneration(scenario): return None
    def activate_apicoectomy(scenario): return None
    def activate_other_endodontic(scenario): return None

# Helper function removed


class EndodonticServices:
    """Class to analyze and activate endodontic services based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.db = MedicalCodingDB()
        self.prompt_template = self._create_prompt_template()
        self.registry = SubtopicRegistry()
        self._register_subtopics()
        

    def _register_subtopics(self):
        """Register all subtopics for parallel activation."""
        self.registry.register("D3110-D3120", pulpcapping_service.activate_pulp_capping, 
                            "Pulp Capping (D3110-D3120)")
        self.registry.register("D3220-D3222", pulpotomy_service.activate_pulpotomy, 
                            "Pulpotomy (D3220-D3222)")
        self.registry.register("D3230-D3240", primary_teeth_therapy_service.activate_primary_teeth_therapy, 
                            "Endodontic Therapy on Primary Teeth (D3230-D3240)")
        self.registry.register("D3310-D3333", endodontic_therapy_service.activate_endodontic_therapy, 
                            "Endodontic Therapy (D3310-D3333)")
        self.registry.register("D3346-D3348", endodontic_retreatment_service.activate_endodontic_retreatment, 
                            "Endodontic Retreatment (D3346-D3348)")
        self.registry.register("D3351", apexification_service.activate_apexification, 
                            "Apexification/Recalcification (D3351)")
        self.registry.register("D3355-D3357", pulpal_regeneration_service.activate_pulpal_regeneration, 
                            "Pulpal Regeneration (D3355-D3357)")
        self.registry.register("D3410-D3470", apicoectomy_service.activate_apicoectomy, 
                            "Apicoectomy/Periradicular Services (D3410-D3470)")
        self.registry.register("D3910-D3999", other_endodontic_service.activate_other_endodontic, 
                            "Other Endodontic Procedures (D3910-D3999)")
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing endodontic services.""" 
        prompt_data = self.db.get_topic_prompt("endodontic_prompt")
        instruction_data = self.db.get_instruction("instruction_prompt")
        print("###***Prompt Data Successfully Retrived from Database***###, ", "endodontic_prompt")
        if not prompt_data or not prompt_data.get("template"):
            raise ValueError("Failed to retrieve prompt 'endodontic_services_prompt' from database")
        template = prompt_data["template"]
        print(f"Template: {template}")
        return PromptTemplate(
            template=f"""
            {template}
            {instruction_data}
            """,
            input_variables=["scenario"]
        )
    
    def analyze_endodontic(self, scenario: str) -> dict: # Changed return type to dict
        """Analyze the scenario and return raw LLM output and the applicable code range string."""
        result = {"raw_output": None, "code_range": None}
        try:
            print(f"Analyzing endodontic scenario: {scenario[:100]}...")
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
                 print(f"Endodontics analyze result: Found Code Range={code_range_string}")
            else:
                 print("Endodontics analyze result: No applicable code range found in raw output.")
                    
            return result
                    
        except Exception as e:
            print(f"Error in analyze_endodontic: {str(e)}")
            result["error"] = str(e)
            return result
    
    async def activate_endodontic(self, scenario: str) -> dict: # Changed return type and logic
        """Activate relevant subtopics in parallel based on LLM-identified code ranges."""
        # Consistent final result structure
        final_result = {"raw_topic_data": None, "code_range": "D3000-D3999", "activated_subtopics": [], "subtopics_data": [], "error": None}
        try:
            # Get the analysis result dictionary
            analysis_result = self.analyze_endodontic(scenario)
            
            # Store raw output
            final_result["raw_topic_data"] = analysis_result.get("raw_output")

            # Check for analysis errors
            if analysis_result.get("error"):
                final_result["error"] = f"Analysis Error: {analysis_result['error']}"
                return final_result
            
            # Get code range string
            code_range_string = analysis_result.get("code_range")
            
            if code_range_string:
                print(f"Endodontics activate using code ranges: {code_range_string}")
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
                print("No applicable code ranges identified by LLM for endodontic analysis.")
                
            # Clear error key if no error occurred
            if final_result.get("error") is None:
                 try: del final_result["error"]
                 except KeyError: pass

            return final_result
            
        except Exception as e:
            print(f"Error in endodontic activation: {str(e)}")
            final_result["error"] = str(e)
            return final_result
    
    async def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = await self.activate_endodontic(scenario)
        print(f"\n=== ENDODONTIC ANALYSIS RESULT ===")
        # Updated printing logic
        print(f"RAW TOPIC DATA:\n---\n{result.get('raw_topic_data', 'N/A')}\n---")
        print(f"OVERALL TOPIC CODE RANGE: {result.get('code_range', 'None')}")
        print(f"ACTIVATED SUBTOPICS: {', '.join(result.get('activated_subtopics', []))}")
        print(f"SUBTOPICS DATA: {result.get('subtopics_data', [])}")
        if 'error' in result:
            print(f"ERROR: {result['error']}")

endodontic_service = EndodonticServices()
# Example usage
if __name__ == "__main__":
    async def main():
        endo_service = EndodonticServices()
        scenario = input("Enter an endodontic dental scenario: ")
        await endo_service.run_analysis(scenario)
    
    asyncio.run(main())