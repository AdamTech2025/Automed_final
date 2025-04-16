import os
import sys
import asyncio
from langchain.prompts import PromptTemplate
from llm_services import LLMService, get_service, set_model, set_temperature

from sub_topic_registry import SubtopicRegistry

# Add the root directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)

# Import modules
from topics.prompt import PROMPT

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

class FixedProsthodonticsServices:
    """Class to analyze and activate fixed prosthodontics services based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
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
        return PromptTemplate(
            template=f"""
You are a highly experienced dental coding expert with over 15 years of expertise in ADA dental codes. 
Your task is to analyze the given scenario and determine the most applicable fixed prosthodontics code range(s) based on the following classifications:

## **Fixed Partial Denture Pontics (D6205-D6253)**
**Use when:** Providing artificial replacement teeth in a fixed bridge.
**Check:** Documentation specifies pontic material and design for the edentulous area.
**Note:** These are the artificial teeth in a bridge that replace missing natural teeth.
**Activation trigger:** Scenario mentions OR implies any bridge pontic, artificial tooth in a bridge, tooth replacement in fixed prosthesis, or pontic design/material. INCLUDE this range if there's any indication of replacement teeth in a fixed bridge.

## **Fixed Partial Denture Retainers — Inlays/Onlays (D6545-D6634)**
**Use when:** Using inlays or onlays as the retaining elements for a fixed bridge.
**Check:** Documentation details the inlay/onlay material and design as a bridge retainer.
**Note:** These are more conservative than full crowns but still provide retention for the bridge.
**Activation trigger:** Scenario mentions OR implies any inlay retainer, onlay abutment, partial coverage retainer for bridge, or conservative bridge attachment. INCLUDE this range if there's any hint of inlays or onlays being used to support a fixed bridge.

## **Fixed Partial Denture Retainers — Crowns (D6710-D6793)**
**Use when:** Using full coverage crowns as the retaining elements for a fixed bridge.
**Check:** Documentation specifies crown material and design as bridge abutments.
**Note:** These provide maximum retention but require more tooth reduction.
**Activation trigger:** Scenario mentions OR implies any crown retainer, abutment crown, full coverage bridge support, or crown preparation for bridge. INCLUDE this range if there's any suggestion of full crowns being used to support a fixed bridge.

## **Other Fixed Partial Denture Services (D6920-D6999)**
**Use when:** Providing additional services related to fixed bridges.
**Check:** Documentation details the specific service and its purpose for the bridge.
**Note:** These include repairs, recementations, and specialized bridge components.
**Activation trigger:** Scenario mentions OR implies any bridge repair, recementation, stress breaker, precision attachment, or maintenance of existing bridge. INCLUDE this range if there's any indication of services for fixed bridges beyond the initial fabrication.

### **Scenario:**
{{scenario}}
{PROMPT}

RESPOND WITH ALL APPLICABLE CODE RANGES from the options above, even if they are only slightly relevant.
List them in order of relevance, with the most relevant first.
""",
            input_variables=["scenario"]
        )
    
    def analyze_prosthodontics_fixed(self, scenario: str) -> str:
        """Analyze the scenario to determine applicable code ranges."""
        try:
            print(f"Analyzing fixed prosthodontics scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code_range = result.strip()
            print(f"Prosthodontics Fixed analyze_prosthodontics_fixed result: {code_range}")
            return code_range
        except Exception as e:
            print(f"Error in analyze_prosthodontics_fixed: {str(e)}")
            return ""
    
    async def activate_prosthodontics_fixed(self, scenario: str) -> dict:
        """Activate relevant subtopics in parallel and return detailed results."""
        try:
            # Get the code range from the analysis
            prosthodontics_result = self.analyze_prosthodontics_fixed(scenario)
            if not prosthodontics_result:
                print("No prosthodontics result returned")
                return {}
            
            print(f"Prosthodontics Fixed Result in activate_prosthodontics_fixed: {prosthodontics_result}")
            
            # Activate subtopics in parallel using the registry
            result = await self.registry.activate_all(scenario, prosthodontics_result)
            
            # Return a dictionary with the required fields
            return {
                "code_range": prosthodontics_result,
                "activated_subtopics": result["activated_subtopics"],
                "codes": result["topic_result"]
            }
        except Exception as e:
            print(f"Error in prosthodontics fixed analysis: {str(e)}")
            return {}
    
    async def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = await self.activate_prosthodontics_fixed(scenario)
        print(f"\n=== FIXED PROSTHODONTICS ANALYSIS RESULT ===")
        print(f"CODE RANGE: {result.get('code_range', 'None')}")
        print(f"ACTIVATED SUBTOPICS: {', '.join(result.get('activated_subtopics', []))}")
        print(f"SPECIFIC CODES: {', '.join(result.get('codes', []))}")

prosthodontics_service = FixedProsthodonticsServices()
# Example usage
if __name__ == "__main__":
    async def main():
        prosthodontics_service = FixedProsthodonticsServices()
        scenario = input("Enter a fixed prosthodontics dental scenario: ")
        await prosthodontics_service.run_analysis(scenario)
    
    asyncio.run(main())