import os
import sys
import asyncio
import re # Added for parsing
from langchain.prompts import PromptTemplate
from llm_services import LLMService, get_service, set_model, set_temperature

from sub_topic_registry import SubtopicRegistry

# Add the project root to the path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

# Import modules
from topics.prompt import PROMPT

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

class ImplantServices:
    """Class to analyze and activate implant services based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
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
        return PromptTemplate(
            template=f"""
You are a highly experienced dental coding expert with over 15 years of expertise in ADA dental codes. 
Your task is to analyze the given scenario and determine the most applicable implant services code range(s) based on the following classifications:

## **Pre-Surgical Services (D6190)**
**Use when:** Performing radiographic/surgical implant index prior to surgery.
**Check:** Documentation specifies the use of radiographic or surgical guides for implant planning.
**Note:** This code is for the planning phase, not the actual implant placement.
**Activation trigger:** Scenario mentions OR implies any implant planning, guide fabrication, treatment planning for implants, or pre-surgical assessment. INCLUDE this code if there's any indication of preparation or planning for dental implant procedures.

## **Surgical Services (D6010-D6199)**
**Use when:** Placing implant bodies, interim abutments, or performing surgical revisions.
**Check:** Documentation details the surgical approach, implant type, and location.
**Note:** Different codes apply based on whether the implant is endosteal, eposteal, or transosteal. Includes implant removal (D6100) and bone grafting (D6101-D6104).
**Activation trigger:** Scenario mentions OR implies any implant placement, implant surgery, bone grafting for implants, implant removal, or surgical exposure of implants. INCLUDE this range if there's any hint of surgical procedures related to implant placement or preparation.

## **Implant Supported Prosthetics (D6051-D6078)**
**Use when:** Providing restorations that are supported by implants, including abutments.
**Check:** Documentation specifies the type of prosthesis and its connection to the implants/abutments.
**Note:** These codes cover a wide range of prosthetic options from single crowns to full-arch restorations and abutments.
**Activation trigger:** Scenario mentions OR implies any implant-supported restoration, implant crown, implant prosthesis, or abutment placement/modification. INCLUDE this range if there's any suggestion of restorations being attached to or supported by implants or abutments.

## **Implant Supported Removable Dentures (D6110-D6119)**
**Use when:** Providing removable dentures that are supported or retained by implants.
**Check:** Documentation clarifies whether the denture is maxillary or mandibular and the attachment mechanism.
**Note:** These differ from traditional dentures in their connection to implants for stability.
**Activation trigger:** Scenario mentions OR implies any implant-supported overdenture, implant-retained denture, or removable prosthesis attached to implants. INCLUDE this range if there's any indication of removable dentures that utilize implants for support or retention.

## **Implant Supported Fixed Dentures (Maintenance) (D6090-D6095)**
**Use when:** Repairing or modifying existing implant prosthetics.
**Check:** Documentation describes the specific repair or maintenance procedure performed.
**Note:** These services maintain the functionality of existing implant restorations.
**Activation trigger:** Scenario mentions OR implies any repair of implant-supported prosthesis, replacement of broken components, or maintenance of implant restorations. INCLUDE this range if there's any hint of repairs or modifications to existing implant prosthetics.

## **Single Crowns, Abutment Supported (D6058-D6077)**
**Use when:** Providing crown restorations supported by an abutment on an implant.
**Check:** Documentation specifies the material of the crown and nature of the abutment.
**Note:** These differ from implant-supported crowns as they require a separate abutment. Often falls under D6051-D6078 range as well.
**Activation trigger:** Scenario mentions OR implies any abutment-supported crown, crown attached to an implant abutment, or restorations on implant abutments. INCLUDE this range if there's any indication of crowns that are placed on abutments rather than directly on implants.

## **Single Crowns, Implant Supported (D6065-D6067)**
**Use when:** Providing crown restorations attached directly to the implant.
**Check:** Documentation identifies the crown material and direct implant connection.
**Note:** These connect directly to the implant without a separate abutment component. Often falls under D6051-D6078 range as well.
**Activation trigger:** Scenario mentions OR implies any implant-supported crown, crown screwed directly to implant, or single-unit restoration on implant. INCLUDE this range if there's any suggestion of crowns connected directly to implants without intermediate abutments.

## **Fixed Partial Denture (FPD), Abutment Supported (D6071-D6074)**
**Use when:** Providing fixed bridges supported by implant abutments.
**Check:** Documentation details the span of the bridge and abutment specifications.
**Note:** These use abutments on implants as the support for a multi-unit fixed bridge. Often falls under D6051-D6078 range as well.
**Activation trigger:** Scenario mentions OR implies any implant-supported bridge with abutments, multi-unit restoration on implant abutments, or fixed prosthesis on implant abutments. INCLUDE this range if there's any indication of bridges supported by abutments placed on implants.

## **Fixed Partial Denture (FPD), Implant Supported (D6075)**
**Use when:** Providing fixed bridges attached directly to implants without separate abutments.
**Check:** Documentation specifies the direct connection between the bridge and implants.
**Note:** This prosthesis connects directly to the implant platform. Often falls under D6051-D6078 range as well.
**Activation trigger:** Scenario mentions OR implies any implant-supported bridge without abutments, bridge screwed directly to implants, or multi-unit prosthesis directly on implants. INCLUDE this code if there's any hint of bridges connected directly to implants without intermediate abutments.

## **Other Implant Services (D6080-D6199)**
**Use when:** Providing specialized implant services not covered by other categories, including maintenance.
**Check:** Documentation provides detailed narrative explaining the specialized service.
**Note:** These include implant maintenance (D6080), repairs, removal of prosthesis (D6081), and specialized modifications.
**Activation trigger:** Scenario mentions OR implies any implant maintenance, specialized implant procedure, implant modification, peri-implantitis treatment, or unusual implant service. INCLUDE this range if there's any suggestion of implant-related services that don't clearly fit other categories.

### **Scenario:**
{{scenario}}
{PROMPT}

RESPOND WITH ALL APPLICABLE CODE RANGES from the options above, even if they are only slightly relevant.
List them in order of relevance, with the most relevant first.
""",
            input_variables=["scenario"]
        )
    
    def analyze_implant_services(self, scenario: str) -> dict: # Changed return type
        """Analyze the scenario and return parsed explanation, doubt, and code range."""
        try:
            print(f"Analyzing implant services scenario: {scenario[:100]}...")
            raw_result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            parsed_result = _parse_llm_topic_output(raw_result) # Use helper
            print(f"Implant Services analyze result: Exp={parsed_result['explanation']}, Doubt={parsed_result['doubt']}, Range={parsed_result['code_range']}")
            return parsed_result # Return parsed dictionary
        except Exception as e:
            print(f"Error in analyze_implant_services: {str(e)}")
            return {"explanation": None, "doubt": None, "code_range": None, "error": str(e)}
    
    async def activate_implant_services(self, scenario: str) -> dict: # Changed return type and logic
        """Activate relevant subtopics in parallel and return detailed results including explanation and doubt."""
        final_result = {"explanation": None, "doubt": None, "code_range": None, "activated_subtopics": [], "codes": []}
        try:
            # Get the parsed analysis (explanation, doubt, code_range)
            topic_analysis_result = self.analyze_implant_services(scenario)
            
            # Store analysis results
            final_result["explanation"] = topic_analysis_result.get("explanation")
            final_result["doubt"] = topic_analysis_result.get("doubt")
            final_result["code_range"] = "D6000-D6199" # Main range for this topic
            
            code_range_string = topic_analysis_result.get("code_range")
            
            if code_range_string:
                print(f"Implant Services activate using code ranges: {code_range_string}")
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
                print("No applicable code ranges found in implant services analysis.")
                
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
        print(f"EXPLANATION: {result.get('explanation', 'N/A')}")
        print(f"DOUBT: {result.get('doubt', 'N/A')}")
        print(f"CODE RANGE: {result.get('code_range', 'None')}")
        print(f"ACTIVATED SUBTOPICS: {', '.join(result.get('activated_subtopics', []))}")
        print(f"SPECIFIC CODES: {result.get('codes', [])}")

implant_service = ImplantServices()
# Example usage
if __name__ == "__main__":
    async def main():
        implant_service = ImplantServices()
        scenario = input("Enter an implant services dental scenario: ")
        await implant_service.run_analysis(scenario)
    
    asyncio.run(main())