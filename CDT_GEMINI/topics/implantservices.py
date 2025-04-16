import os
import sys
import asyncio
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
            self.registry.register("D6190-D6190)", pre_surgical_service.activate_pre_surgical, 
                                "Pre-Surgical Services (D6190-D6190)")
            self.registry.register("D6010-D6199", surgical_service.activate_surgical_services, 
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
            self.registry.register("D6075", fpd_implant_service.activate_fpd_implant, 
                                "Fixed Partial Denture, Implant Supported (D6075)")
            self.registry.register("D6080-D6199", other_implant_services_service.activate_other_implant_services, 
                                "Other Implant Services (D6080-D6199)")
        except Exception as e:
            print(f"Error registering subtopics: {str(e)}")
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing implant services."""
        return PromptTemplate(
            template=f"""
You are a highly experienced dental coding expert with over 15 years of expertise in ADA dental codes. 
Your task is to analyze the given scenario and determine the most applicable implant services code range(s) based on the following classifications:

## **Pre-Surgical Services (D6190-D6190)**
**Use when:** Performing radiographic/surgical implant index prior to surgery.
**Check:** Documentation specifies the use of radiographic or surgical guides for implant planning.
**Note:** This code is for the planning phase, not the actual implant placement.
**Activation trigger:** Scenario mentions OR implies any implant planning, guide fabrication, treatment planning for implants, or pre-surgical assessment. INCLUDE this range if there's any indication of preparation or planning for dental implant procedures.

## **Surgical Services (D6010-D6199)**
**Use when:** Placing implant bodies, interim abutments, or performing surgical revisions.
**Check:** Documentation details the surgical approach, implant type, and location.
**Note:** Different codes apply based on whether the implant is endosteal, eposteal, or transosteal.
**Activation trigger:** Scenario mentions OR implies any implant placement, implant surgery, bone grafting for implants, or surgical exposure of implants. INCLUDE this range if there's any hint of surgical procedures related to implant placement or preparation.

## **Implant Supported Prosthetics (D6051-D6078)**
**Use when:** Providing restorations that are supported by implants.
**Check:** Documentation specifies the type of prosthesis and its connection to the implants.
**Note:** These codes cover a wide range of prosthetic options from single crowns to full-arch restorations.
**Activation trigger:** Scenario mentions OR implies any implant-supported restoration, implant crown, implant prosthesis, or abutment placement. INCLUDE this range if there's any suggestion of restorations being attached to or supported by implants.

## **Implant Supported Removable Dentures (D6110-D6119)**
**Use when:** Providing removable dentures that are supported or retained by implants.
**Check:** Documentation clarifies whether the denture is maxillary or mandibular and the attachment mechanism.
**Note:** These differ from traditional dentures in their connection to implants for stability.
**Activation trigger:** Scenario mentions OR implies any implant-supported overdenture, implant-retained denture, or removable prosthesis attached to implants. INCLUDE this range if there's any indication of removable dentures that utilize implants for support or retention.

## **Implant Supported Fixed Dentures (D6090-D6095)**
**Use when:** Repairing or modifying existing implant prosthetics.
**Check:** Documentation describes the specific repair or maintenance procedure performed.
**Note:** These services maintain the functionality of existing implant restorations.
**Activation trigger:** Scenario mentions OR implies any repair of implant-supported prosthesis, replacement of broken components, or maintenance of implant restorations. INCLUDE this range if there's any hint of repairs or modifications to existing implant prosthetics.

## **Single Crowns, Abutment Supported (D6058-D6077)**
**Use when:** Providing crown restorations supported by an abutment on an implant.
**Check:** Documentation specifies the material of the crown and nature of the abutment.
**Note:** These differ from implant-supported crowns as they require a separate abutment.
**Activation trigger:** Scenario mentions OR implies any abutment-supported crown, crown attached to an implant abutment, or restorations on implant abutments. INCLUDE this range if there's any indication of crowns that are placed on abutments rather than directly on implants.

## **Single Crowns, Implant Supported (D6065-D6067)**
**Use when:** Providing crown restorations attached directly to the implant.
**Check:** Documentation identifies the crown material and direct implant connection.
**Note:** These connect directly to the implant without a separate abutment component.
**Activation trigger:** Scenario mentions OR implies any implant-supported crown, crown screwed directly to implant, or single-unit restoration on implant. INCLUDE this range if there's any suggestion of crowns connected directly to implants without intermediate abutments.

## **Fixed Partial Denture (FPD), Abutment Supported (D6071-D6074)**
**Use when:** Providing fixed bridges supported by implant abutments.
**Check:** Documentation details the span of the bridge and abutment specifications.
**Note:** These use abutments on implants as the support for a multi-unit fixed bridge.
**Activation trigger:** Scenario mentions OR implies any implant-supported bridge with abutments, multi-unit restoration on implant abutments, or fixed prosthesis on implant abutments. INCLUDE this range if there's any indication of bridges supported by abutments placed on implants.

## **Fixed Partial Denture (FPD), Implant Supported (D6075)**
**Use when:** Providing fixed bridges attached directly to implants without separate abutments.
**Check:** Documentation specifies the direct connection between the bridge and implants.
**Note:** These prostheses connect directly to the implant platform.
**Activation trigger:** Scenario mentions OR implies any implant-supported bridge without abutments, bridge screwed directly to implants, or multi-unit prosthesis directly on implants. INCLUDE this range if there's any hint of bridges connected directly to implants without intermediate abutments.

## **Other Implant Services (D6080-D6199)**
**Use when:** Providing specialized implant services not covered by other categories.
**Check:** Documentation provides detailed narrative explaining the specialized service.
**Note:** These include maintenance, repairs, and specialized modifications to implant prosthetics.
**Activation trigger:** Scenario mentions OR implies any implant maintenance, specialized implant procedure, implant modification, peri-implantitis treatment, or unusual implant service. INCLUDE this range if there's any suggestion of implant-related services that don't clearly fit other categories.

### **Scenario:**
{{scenario}}
{PROMPT}

RESPOND WITH ALL APPLICABLE CODE RANGES from the options above, even if they are only slightly relevant.
List them in order of relevance, with the most relevant first.
""",
            input_variables=["scenario"]
        )
    
    def analyze_implant_services(self, scenario: str) -> str:
        """Analyze the scenario to determine applicable code ranges."""
        try:
            print(f"Analyzing implant services scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code_range = result.strip()
            print(f"Implant Services analyze_implant_services result: {code_range}")
            return code_range
        except Exception as e:
            print(f"Error in analyze_implant_services: {str(e)}")
            return ""
    
    async def activate_implant_services(self, scenario: str) -> dict:
        """Activate relevant subtopics in parallel and return detailed results."""
        try:
            # Get the code range from the analysis
            implant_result = self.analyze_implant_services(scenario)
            if not implant_result:
                print("No implant services result returned")
                return {}
            
            print(f"Implant Services Result in activate_implant_services: {implant_result}")
            
            # Activate subtopics in parallel using the registry
            result = await self.registry.activate_all(scenario, implant_result)
            
            # Return a dictionary with the required fields
            return {
                "code_range": implant_result,
                "activated_subtopics": result["activated_subtopics"],
                "codes": result["topic_result"]
            }
        except Exception as e:
            print(f"Error in implant services analysis: {str(e)}")
            return {}
    
    async def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = await self.activate_implant_services(scenario)
        print(f"\n=== IMPLANT SERVICES ANALYSIS RESULT ===")
        print(f"CODE RANGE: {result.get('code_range', 'None')}")
        print(f"ACTIVATED SUBTOPICS: {', '.join(result.get('activated_subtopics', []))}")
        print(f"SPECIFIC CODES: {', '.join(result.get('codes', []))}")

implant_service = ImplantServices()
# Example usage
if __name__ == "__main__":
    async def main():
        implant_service = ImplantServices()
        scenario = input("Enter an implant services dental scenario: ")
        await implant_service.run_analysis(scenario)
    
    asyncio.run(main())