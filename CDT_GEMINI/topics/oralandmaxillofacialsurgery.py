import os
import sys
import asyncio
import re # Added for parsing
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from llm_services import LLMService, get_service, set_model, set_temperature
from database import MedicalCodingDB
from sub_topic_registry import SubtopicRegistry

# Load environment variables
load_dotenv()

# Add the root directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)

# Import service objects from subtopics with fallback mechanism
try:
    from subtopics.OralMaxillofacialSurgery.alveoloplasty import alveoloplasty_service
    from subtopics.OralMaxillofacialSurgery.excision_soft_tissue import excision_soft_tissue_service
    from subtopics.OralMaxillofacialSurgery.excision_intra_osseous import excision_intra_osseous_service
    from subtopics.OralMaxillofacialSurgery.excision_bone_tissue import excision_bone_tissue_service
    from subtopics.OralMaxillofacialSurgery.extractions import extractions_service
    from subtopics.OralMaxillofacialSurgery.closed_fractures import closed_fractures_service
    from subtopics.OralMaxillofacialSurgery.open_fractures import open_fractures_service
    from subtopics.OralMaxillofacialSurgery.other_surgical_procedures import other_surgical_procedures_service
    from subtopics.OralMaxillofacialSurgery.surgical_incision import surgical_incision_service
    from subtopics.OralMaxillofacialSurgery.tmj_dysfunctions import tmj_dysfunctions_service
    from subtopics.OralMaxillofacialSurgery.traumatic_wounds import traumatic_wounds_service
    from subtopics.OralMaxillofacialSurgery.complicated_suturing import complicated_suturing_service
    from subtopics.OralMaxillofacialSurgery.other_repair_procedures import other_repair_procedures_service
    from subtopics.OralMaxillofacialSurgery.vestibuloplasty import vestibuloplasty_service
    
except ImportError as e:
    print(f"Warning: Could not import subtopics for OralMaxillofacialSurgery: {str(e)}")
    print(f"Current sys.path: {sys.path}")
    # Define fallback functions
    def activate_extractions(scenario): return None
    def activate_other_surgical_procedures(scenario): return None
    def activate_alveoloplasty(scenario): return None
    def activate_vestibuloplasty(scenario): return None
    def activate_excision_soft_tissue(scenario): return None
    def activate_excision_intra_osseous(scenario): return None
    def activate_excision_bone_tissue(scenario): return None
    def activate_surgical_incision(scenario): return None
    def activate_closed_fractures(scenario): return None
    def activate_open_fractures(scenario): return None
    def activate_tmj_dysfunctions(scenario): return None
    def activate_traumatic_wounds(scenario): return None
    def activate_complicated_suturing(scenario): return None
    def activate_other_repair_procedures(scenario): return None

class OralMaxillofacialSurgeryServices:
    """Class to analyze and activate oral and maxillofacial surgery services based on dental scenarios."""
    
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
            # Grouping extractions for registration clarity
            self.registry.register("D7111-D7140", extractions_service.activate_extractions, 
                                "Extractions (Simple) (D7111-D7140)")
            self.registry.register("D7210-D7251", extractions_service.activate_extractions, # Assuming same function handles both simple/surgical
                                "Surgical Extractions (D7210-D7251)")
            
            self.registry.register("D7260-D7297", other_surgical_procedures_service.activate_other_surgical_procedures, 
                                "Other Surgical Procedures (D7260-D7297)")
            self.registry.register("D7310-D7321", alveoloplasty_service.activate_alveoloplasty, 
                                "Alveoloplasty (D7310-D7321)")
            self.registry.register("D7340-D7350", vestibuloplasty_service.activate_vestibuloplasty, 
                                "Vestibuloplasty (D7340-D7350)")
            self.registry.register("D7410-D7465", excision_soft_tissue_service.activate_excision_soft_tissue, 
                                "Excision of Soft Tissue Lesions (D7410-D7465)")
            self.registry.register("D7440-D7461", excision_intra_osseous_service.activate_excision_intra_osseous, 
                                "Excision of Intra-Osseous Lesions (D7440-D7461)")
            self.registry.register("D7471-D7490", excision_bone_tissue_service.activate_excision_bone_tissue, 
                                "Excision of Bone Tissue (D7471-D7490)")
            self.registry.register("D7510-D7560", surgical_incision_service.activate_surgical_incision, 
                                "Surgical Incision (D7510-D7560)")
            # Grouping fractures
            self.registry.register("D7610-D7780", closed_fractures_service.activate_closed_fractures, 
                                "Treatment of Closed Fractures (D7610-D7780)")
            self.registry.register("D7610-D7780", open_fractures_service.activate_open_fractures, # Registry needs to handle duplicate range keys if logic differs
                                "Treatment of Open Fractures (D7610-D7780)")
            # Note: Range D7810-D7880 covers TMJ issues, not just dislocation reduction
            self.registry.register("D7810-D7880", tmj_dysfunctions_service.activate_tmj_dysfunctions, 
                                "TMJ Treatment (D7810-D7880)") 
            self.registry.register("D7910-D7912", traumatic_wounds_service.activate_traumatic_wounds, 
                                "Repair of Traumatic Wounds (D7910-D7912)")
            self.registry.register("D7911-D7912", complicated_suturing_service.activate_complicated_suturing, # Overlaps with above 
                                "Complicated Suturing (D7911-D7912)")
            self.registry.register("D7920-D7999", other_repair_procedures_service.activate_other_repair_procedures, 
                                "Other Repair Procedures (D7920-D7999)")
        except Exception as e:
            print(f"Error registering subtopics: {str(e)}")
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing oral and maxillofacial surgery services."""
        prompt_data = self.db.get_topic_prompt("oral_maxillofacial_surgery_prompt")
        instruction_data = self.db.get_instruction("instruction_prompt")
        print("###***Prompt Data Successfully Retrived from Database***###, ", "oral_maxillofacial_surgery_prompt")
        if not prompt_data or not prompt_data.get("template"):
            raise ValueError("Failed to retrieve prompt 'oral_maxillofacial_surgery_prompt' from database")
        template = prompt_data["template"]
        print(f"Template: {template}")
        return PromptTemplate(
            template=f"""
            {template}
            {instruction_data}
            """,
            input_variables=["scenario"]
        )
    
    def analyze_oral_maxillofacial_surgery(self, scenario: str) -> dict: # Changed return type to dict
        """Analyze the scenario and return raw LLM output and the applicable code range string."""
        result = {"raw_output": None, "code_range": None}
        try:
            print(f"Analyzing oral and maxillofacial surgery scenario: {scenario[:100]}...")
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
                 print(f"Oral & Maxillofacial Surgery analyze result: Found Code Range={code_range_string}")
            else:
                 print("Oral & Maxillofacial Surgery analyze result: No applicable code range found in raw output.")
                    
            return result
                    
        except Exception as e:
            print(f"Error in analyze_oral_maxillofacial_surgery: {str(e)}")
            result["error"] = str(e)
            return result
    
    async def activate_oral_maxillofacial_surgery(self, scenario: str) -> dict: # Changed return type and logic
        """Activate relevant subtopics in parallel based on LLM-identified code ranges."""
        # Consistent final result structure
        final_result = {"raw_topic_data": None, "code_range": "D7000-D7999", "activated_subtopics": [], "subtopics_data": [], "error": None}
        try:
            # Get the analysis result dictionary
            analysis_result = self.analyze_oral_maxillofacial_surgery(scenario)
            
            # Store raw output
            final_result["raw_topic_data"] = analysis_result.get("raw_output")

            # Check for analysis errors
            if analysis_result.get("error"):
                final_result["error"] = f"Analysis Error: {analysis_result['error']}"
                return final_result
            
            # Get code range string
            code_range_string = analysis_result.get("code_range")
            
            if code_range_string:
                print(f"Oral & Maxillofacial Surgery activate using code ranges: {code_range_string}")
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
                print("No applicable code ranges identified by LLM for oral surgery analysis.")

            # Clear error key if no error occurred
            if final_result.get("error") is None:
                 try: del final_result["error"]
                 except KeyError: pass

            return final_result
            
        except Exception as e:
            print(f"Error in oral and maxillofacial surgery activation: {str(e)}")
            final_result["error"] = str(e)
            return final_result
    
    async def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = await self.activate_oral_maxillofacial_surgery(scenario)
        print(f"\n=== ORAL & MAXILLOFACIAL SURGERY ANALYSIS RESULT ===")
        # Updated printing logic
        print(f"RAW TOPIC DATA:\n---\n{result.get('raw_topic_data', 'N/A')}\n---")
        print(f"OVERALL TOPIC CODE RANGE: {result.get('code_range', 'None')}")
        print(f"ACTIVATED SUBTOPICS: {', '.join(result.get('activated_subtopics', []))}")
        print(f"SUBTOPICS DATA: {result.get('subtopics_data', [])}")
        if 'error' in result:
            print(f"ERROR: {result['error']}")

oral_surgery_service = OralMaxillofacialSurgeryServices()
# Example usage
if __name__ == "__main__":
    async def main():
        oral_surgery_service = OralMaxillofacialSurgeryServices()
        scenario = input("Enter an oral and maxillofacial surgery scenario: ")
        await oral_surgery_service.run_analysis(scenario)
    
    asyncio.run(main())