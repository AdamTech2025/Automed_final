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
from subtopics.Maxillofacial_Prosthetics.general_prosthetics import general_prosthetics_service
from subtopics.Maxillofacial_Prosthetics.carriers import carriers_service

class MaxillofacialProstheticsServices:
    """Class to analyze and activate maxillofacial prosthetics services based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
        self.registry = SubtopicRegistry()
        self._register_subtopics()
    
    def _register_subtopics(self):
        """Register all subtopics for parallel activation."""
        self.registry.register("D5992-D5937", general_prosthetics_service.activate_general_prosthetics, 
                            "General Maxillofacial Prosthetics (D5992-D5937)")
        self.registry.register("D5986-D5999", carriers_service.activate_carriers, 
                            "Carriers (D5986-D5999)")
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing maxillofacial prosthetics services."""
        return PromptTemplate(
            template=f"""
You are a highly experienced dental coding expert with over 15 years of expertise in ADA dental codes. 
Your task is to analyze the given scenario and determine the most applicable maxillofacial prosthetics code range(s) based on the following classifications:

## **General Maxillofacial Prosthetics (D5992-D5937)**
**Use when:** Creating or adjusting prosthetic replacements for missing facial or oral structures.
**Check:** Documentation describes the specific prosthesis type and its purpose in restoring function or aesthetics.
**Note:** These prostheses address complex defects resulting from surgery, trauma, or congenital conditions.
**Activation trigger:** Scenario mentions OR implies any facial prosthesis, oral-maxillofacial defect, obturator, speech aid, radiation shield, or post-surgical rehabilitation. INCLUDE this range if there's any indication of specialized prostheses for maxillofacial defects.

## **Carriers (D5986-D5999)**
**Use when:** Fabricating devices for delivery of therapeutic agents or specialized treatments.
**Check:** Documentation specifies the purpose of the carrier and what it's designed to deliver.
**Note:** These include custom trays for medication delivery or protection of tissues.
**Activation trigger:** Scenario mentions OR implies any fluoride carrier, medicament delivery device, specialized tray, or custom carrier for therapeutic agents. INCLUDE this range if there's any hint of devices designed to hold or deliver medications or treatments.

### **Scenario:**
{{scenario}}
{PROMPT}

RESPOND WITH ALL APPLICABLE CODE RANGES from the options above, even if they are only slightly relevant.
List them in order of relevance, with the most relevant first.
""",
            input_variables=["scenario"]
        )
    
    def analyze_maxillofacial_prosthetics(self, scenario: str) -> str:
        """Analyze the scenario to determine applicable code ranges."""
        try:
            print(f"Analyzing maxillofacial prosthetics scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code_range = result.strip()
            print(f"Maxillofacial Prosthetics analyze_maxillofacial_prosthetics result: {code_range}")
            return code_range
        except Exception as e:
            print(f"Error in analyze_maxillofacial_prosthetics: {str(e)}")
            return ""
    
    async def activate_maxillofacial_prosthetics(self, scenario: str) -> dict:
        """Activate relevant subtopics in parallel and return detailed results."""
        try:
            # Get the code range from the analysis
            maxillofacial_result = self.analyze_maxillofacial_prosthetics(scenario)
            if not maxillofacial_result:
                print("No maxillofacial prosthetics result returned")
                return {}
            
            print(f"Maxillofacial Prosthetics Result in activate_maxillofacial_prosthetics: {maxillofacial_result}")
            
            # Activate subtopics in parallel using the registry
            result = await self.registry.activate_all(scenario, maxillofacial_result)
            
            # Return a dictionary with the required fields
            return {
                "code_range": maxillofacial_result,
                "activated_subtopics": result["activated_subtopics"],
                "codes": result["topic_result"]
            }
        except Exception as e:
            print(f"Error in maxillofacial prosthetics analysis: {str(e)}")
            return {}
    
    async def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = await self.activate_maxillofacial_prosthetics(scenario)
        print(f"\n=== MAXILLOFACIAL PROSTHETICS ANALYSIS RESULT ===")
        print(f"CODE RANGE: {result.get('code_range', 'None')}")
        print(f"ACTIVATED SUBTOPICS: {', '.join(result.get('activated_subtopics', []))}")
        print(f"SPECIFIC CODES: {', '.join(result.get('codes', []))}")

maxillofacial_service = MaxillofacialProstheticsServices()
# Example usage
if __name__ == "__main__":
    async def main():
        maxillofacial_service = MaxillofacialProstheticsServices()
        scenario = input("Enter a dental maxillofacial prosthetics scenario: ")
        await maxillofacial_service.run_analysis(scenario)
    
    asyncio.run(main())