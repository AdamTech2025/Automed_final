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

class RemovableProsthodonticsServices:
    """Class to analyze and activate removable prosthodontics services based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
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
        return PromptTemplate(
            template=f"""
You are a highly experienced dental coding expert with over 15 years of expertise in ADA dental codes. 
Your task is to analyze the given scenario and determine the most applicable removable prosthodontics code range(s) based on the following classifications:

## IMPORTANT GUIDELINES:
- You should activate ALL code ranges that have any potential relevance to the scenario
- Even if a code range is only slightly related, include it in your response
- Only exclude a code range if it is DEFINITELY NOT relevant to the scenario
- When in doubt, INCLUDE the code range rather than exclude it
- Multiple code ranges can and should be activated if they have any potential applicability
- Your goal is to ensure no potentially relevant codes are missed

## **Complete Dentures (D5110-D5140)**
**Use when:** Providing full arch prostheses for edentulous patients.
**Check:** Documentation specifies maxillary/mandibular and immediate/conventional status.
**Note:** These address complete tooth loss in an arch with full tissue coverage prostheses.
**Activation trigger:** Scenario mentions OR implies any full denture, complete denture, edentulous treatment, immediate denture, or replacement of all teeth in an arch. INCLUDE this range if there's any indication of complete tooth replacement in either arch.

## **Partial Denture (D5211-D5286)**
**Use when:** Providing removable prostheses for partially edentulous patients.
**Check:** Documentation details the framework material and arch being restored.
**Note:** These replace some but not all teeth in an arch while utilizing remaining natural teeth for support.
**Activation trigger:** Scenario mentions OR implies any partial denture, RPD, removable partial, cast framework prosthesis, or flexible base partial. INCLUDE this range if there's any hint of replacing some but not all teeth with a removable appliance.

## **Adjustments to Dentures (D5410-D5422)**
**Use when:** Modifying existing dentures to improve fit or function.
**Check:** Documentation specifies the type of denture being adjusted.
**Note:** These address minor issues without remaking or significantly altering the prosthesis.
**Activation trigger:** Scenario mentions OR implies any denture adjustment, fit correction, comfort adjustment, occlusal adjustment of prosthesis, or minor modification of denture. INCLUDE this range if there's any suggestion of minor alterations to existing dentures.

## **Repairs to Complete Dentures (D5511-D5520)**
**Use when:** Fixing damaged complete dentures.
**Check:** Documentation identifies the specific damage and repair performed.
**Note:** These restore function to damaged complete dentures without replacement.
**Activation trigger:** Scenario mentions OR implies any denture repair, broken denture, cracked denture base, replacement of broken teeth in denture, or fixing complete denture. INCLUDE this range if there's any indication of repairing damage to a complete denture.

## **Repairs to Partial Dentures (D5611-D5671)**
**Use when:** Fixing damaged partial dentures.
**Check:** Documentation details the specific component repaired or replaced.
**Note:** These restore function to damaged partial dentures by addressing specific components.
**Activation trigger:** Scenario mentions OR implies any partial denture repair, broken clasp, damaged framework, resin base repair, or adding components to existing partial. INCLUDE this range if there's any hint of repairing or modifying components of a partial denture.

## **Denture Rebase Procedures (D5710-D5725)**
**Use when:** Completely replacing the base material of an existing denture.
**Check:** Documentation indicates complete replacement of the base while maintaining the original teeth.
**Note:** These procedures address significant changes in ridge morphology requiring new base adaptation.
**Activation trigger:** Scenario mentions OR implies any denture rebase, replacing entire denture base, new base for existing denture, or complete base replacement. INCLUDE this range if there's any suggestion of replacing the entire base material while keeping the original teeth.

## **Denture Reline Procedures (D5730-D5761)**
**Use when:** Adding new material to the tissue surface of a denture to improve fit.
**Check:** Documentation specifies whether chairside or laboratory reline and type of denture.
**Note:** These procedures add material rather than completely replacing the base.
**Activation trigger:** Scenario mentions OR implies any denture reline, adding material to denture base, improving fit with new lining, chairside or lab reline. INCLUDE this range if there's any indication of adding material to the tissue surface of a denture.

## **Interim Prosthesis (D5810-D5821)**
**Use when:** Providing temporary dentures during treatment phases.
**Check:** Documentation clarifies the interim nature and purpose of the prosthesis.
**Note:** These are not intended as definitive restorations but as transitional appliances.
**Activation trigger:** Scenario mentions OR implies any temporary denture, interim prosthesis, transitional denture, provisional appliance, or temporary tooth replacement. INCLUDE this range if there's any hint of temporary dentures during transition to final prostheses.

## **Other Removable Prosthetic Services (D5863-D5876, D5850-D5851, D5899)**
**Use when:** Providing specialized prosthetic services not covered in other categories.
**Check:** Documentation details the specific service and its therapeutic purpose.
**Note:** These include tissue conditioning (D5850-D5851), precision attachments (D5863-D5866), overdentures (D5876), and other advanced procedures (D5899 for unspecified).
**Activation trigger:** Scenario mentions OR implies any tissue conditioning, precision attachment, specialized denture procedure, overdenture, or unusual prosthetic technique. INCLUDE the relevant sub-range(s) (D5863-D5876, D5850-D5851, or D5899) if there's any suggestion of specialized removable prosthetic services beyond standard dentures and partials.

### **Scenario:**
{{scenario}}
{PROMPT}

RESPOND WITH ALL APPLICABLE CODE RANGES from the options above, even if they are only slightly relevant.
List them in order of relevance, with the most relevant first.
""",
            input_variables=["scenario"]
        )
    
    def analyze_prosthodontics_removable(self, scenario: str) -> dict: # Changed return type
        """Analyze the scenario and return parsed explanation, doubt, and code range."""
        try:
            print(f"Analyzing removable prosthodontics scenario: {scenario[:100]}...")
            raw_result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            parsed_result = _parse_llm_topic_output(raw_result) # Use helper
            print(f"Prosthodontics Removable analyze result: Exp={parsed_result['explanation']}, Doubt={parsed_result['doubt']}, Range={parsed_result['code_range']}")
            return parsed_result # Return parsed dictionary
        except Exception as e:
            print(f"Error in analyze_prosthodontics_removable: {str(e)}")
            return {"explanation": None, "doubt": None, "code_range": None, "error": str(e)}
    
    async def activate_prosthodontics_removable(self, scenario: str) -> dict: # Changed return type and logic
        """Activate relevant subtopics in parallel and return detailed results including explanation and doubt."""
        final_result = {"explanation": None, "doubt": None, "code_range": None, "activated_subtopics": [], "codes": []}
        try:
            # Get the parsed analysis (explanation, doubt, code_range)
            topic_analysis_result = self.analyze_prosthodontics_removable(scenario)
            
            # Store analysis results
            final_result["explanation"] = topic_analysis_result.get("explanation")
            final_result["doubt"] = topic_analysis_result.get("doubt")
            final_result["code_range"] = topic_analysis_result.get("code_range") # This is the string of ranges
            
            code_range_string = topic_analysis_result.get("code_range")
            
            if code_range_string:
                print(f"Prosthodontics Removable activate using code ranges: {code_range_string}")
                # Activate subtopics in parallel using the registry with the parsed code range string
                subtopic_results = await self.registry.activate_all(scenario, code_range_string)
                final_result["activated_subtopics"] = subtopic_results.get("activated_subtopics", [])
                final_result["codes"] = subtopic_results.get("topic_result", []) # Assuming 'topic_result' holds the list of codes
            else:
                print("No applicable code ranges found in removable prosthodontics analysis.")
                
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
        print(f"EXPLANATION: {result.get('explanation', 'N/A')}")
        print(f"DOUBT: {result.get('doubt', 'N/A')}")
        print(f"CODE RANGE: {result.get('code_range', 'None')}")
        print(f"ACTIVATED SUBTOPICS: {', '.join(result.get('activated_subtopics', []))}")
        print(f"SPECIFIC CODES: {result.get('codes', [])}")

prosthodontics_service = RemovableProsthodonticsServices()
# Example usage
if __name__ == "__main__":
    async def main():
        prosthodontics_service = RemovableProsthodonticsServices()
        scenario = input("Enter a removable prosthodontics dental scenario: ")
        await prosthodontics_service.run_analysis(scenario)
    
    asyncio.run(main())