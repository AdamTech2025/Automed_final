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

# Import subtopics with fallback mechanism
try:
    from subtopics.Orthodontics.limited_orthodontic_treatment import limited_orthodontic_treatment
    from subtopics.Orthodontics.comprehensive_orthodontic_treatment import comprehensive_orthodontic_treatment
    from subtopics.Orthodontics.minor_treatment_harmful_habits import minor_treatment_harmful_habits
    from subtopics.Orthodontics.other_orthodontic_services import other_orthodontic_services
except ImportError:
    print("Warning: Could not import subtopics for Orthodontics. Using fallback functions.")
    # Define fallback functions if needed
    def activate_limited_orthodontic_treatment(scenario): return None
    def activate_comprehensive_orthodontic_treatment(scenario): return None
    def activate_minor_treatment_harmful_habits(scenario): return None
    def activate_other_orthodontic_services(scenario): return None

class OrthodonticServices:
    """Class to analyze and activate orthodontic services based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
        self.registry = SubtopicRegistry()
        self._register_subtopics()
    
    def _register_subtopics(self):
        """Register all subtopics for parallel activation."""
        self.registry.register("D8010-D8040", limited_orthodontic_treatment.activate_limited_orthodontic_treatment, 
                            "Limited Orthodontic Treatment (D8010-D8040)")
        self.registry.register("D8070-D8090", comprehensive_orthodontic_treatment.activate_comprehensive_orthodontic_treatment, 
                            "Comprehensive Orthodontic Treatment (D8070-D8090)")
        self.registry.register("D8210-D8220", minor_treatment_harmful_habits.activate_minor_treatment_harmful_habits, 
                            "Minor Treatment to Control Harmful Habits (D8210-D8220)")
        self.registry.register("D8660-D8999", other_orthodontic_services.activate_other_orthodontic_services, 
                            "Other Orthodontic Services (D8660-D8999)")
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing orthodontic services."""
        return PromptTemplate(
            template=f"""
You are a highly experienced dental coding expert with over 15 years of expertise in ADA dental codes. 
Your task is to analyze the given scenario and determine the most applicable orthodontic code range(s) based on the following classifications:

## **Limited Orthodontic Treatment (D8010-D8040)**
**Use when:** Providing partial correction or addressing a specific orthodontic problem.
**Check:** Documentation specifies which dentition stage (primary, transitional, adolescent, adult) is being treated.
**Note:** These procedures focus on limited treatment goals rather than comprehensive correction.
**Activation trigger:** Scenario mentions OR implies any partial orthodontic treatment, minor tooth movement, single arch treatment, or interceptive orthodontics. INCLUDE this range if there's any indication of focused orthodontic care rather than full correction.

## **Comprehensive Orthodontic Treatment (D8070-D8090)**
**Use when:** Providing complete orthodontic correction for the entire dentition.
**Check:** Documentation identifies the dentition stage (transitional, adolescent, adult) being treated.
**Note:** These involve full banding/bracketing of the dentition with regular adjustments.
**Activation trigger:** Scenario mentions OR implies any full orthodontic treatment, complete braces, comprehensive correction, full arch treatment, or extensive alignment. INCLUDE this range if there's any hint of complete orthodontic care addressing overall occlusion.

## **Minor Treatment to Control Harmful Habits (D8210-D8220)**
**Use when:** Correcting deleterious oral habits through appliance therapy.
**Check:** Documentation specifies the habit being addressed and type of appliance used.
**Note:** These procedures target specific habits rather than overall malocclusion.
**Activation trigger:** Scenario mentions OR implies any thumb-sucking, tongue thrusting, habit appliance, habit breaking, or interceptive treatment for parafunctional habits. INCLUDE this range if there's any suggestion of treating harmful oral habits through specialized appliances.

## **Other Orthodontic Services (D8660-D8999)**
**Use when:** Providing supplementary orthodontic services or treatments not specified elsewhere.
**Check:** Documentation details the specific service provided and its purpose.
**Note:** These include consultations, retention, repairs, and additional orthodontic services.
**Activation trigger:** Scenario mentions OR implies any pre-orthodontic visit, retainer placement, bracket repair, adjustment visit, or specialized orthodontic service. INCLUDE this range if there's any indication of orthodontic care beyond the initial appliance placement.

### **Scenario:**
{{scenario}}
{PROMPT}

RESPOND WITH ALL APPLICABLE CODE RANGES from the options above, even if they are only slightly relevant.
List them in order of relevance, with the most relevant first.
""",
            input_variables=["scenario"]
        )
    
    def analyze_orthodontic(self, scenario: str) -> str:
        """Analyze the scenario to determine applicable code ranges."""
        try:
            print(f"Analyzing orthodontic scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code_range = result.strip()
            print(f"Orthodontic analyze_orthodontic result: {code_range}")
            return code_range
        except Exception as e:
            print(f"Error in analyze_orthodontic: {str(e)}")
            return ""
    
    async def activate_orthodontic(self, scenario: str) -> dict:
        """Activate relevant subtopics in parallel and return detailed results."""
        try:
            # Get the code range from the analysis
            orthodontic_result = self.analyze_orthodontic(scenario)
            if not orthodontic_result:
                print("No orthodontic result returned")
                return {}
            
            print(f"Orthodontic Result in activate_orthodontic: {orthodontic_result}")
            
            # Activate subtopics in parallel using the registry
            result = await self.registry.activate_all(scenario, orthodontic_result)
            
            # Return a dictionary with the required fields
            return {
                "code_range": orthodontic_result,
                "activated_subtopics": result["activated_subtopics"],
                "codes": result["topic_result"]
            }
        except Exception as e:
            print(f"Error in orthodontic analysis: {str(e)}")
            return {}
    
    async def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = await self.activate_orthodontic(scenario)
        print(f"\n=== ORTHODONTIC ANALYSIS RESULT ===")
        print(f"CODE RANGE: {result.get('code_range', 'None')}")
        print(f"ACTIVATED SUBTOPICS: {', '.join(result.get('activated_subtopics', []))}")
        print(f"SPECIFIC CODES: {', '.join(result.get('codes', []))}")

orthodontic_service = OrthodonticServices()
# Example usage
if __name__ == "__main__":
    async def main():
        orthodontic_service = OrthodonticServices()
        scenario = input("Enter an orthodontic scenario: ")
        await orthodontic_service.run_analysis(scenario)
    
    asyncio.run(main())