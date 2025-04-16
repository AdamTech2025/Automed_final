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
    from subtopics.Periodontics.surgical_services import surgical_services
    from subtopics.Periodontics.non_surgical_services import non_surgical_services
    from subtopics.Periodontics.other_periodontal_services import other_periodontal_services
except ImportError:
    print("Warning: Could not import subtopics for Periodontics. Using fallback functions.")
    # Define fallback functions if needed
    def activate_surgical_services(scenario): return None
    def activate_non_surgical_services(scenario): return None
    def activate_other_periodontal_services(scenario): return None

class PeriodonticServices:
    """Class to analyze and activate periodontic services based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
        self.registry = SubtopicRegistry()
        self._register_subtopics()
    
    def _register_subtopics(self):
        """Register all subtopics for parallel activation."""
        self.registry.register("D4210-D4286", surgical_services.activate_surgical_services, 
                            "Surgical Services (D4210-D4286)")
        self.registry.register("D4322-D4381", non_surgical_services.activate_non_surgical_services, 
                            "Non-Surgical Services (D4322-D4381)")
        self.registry.register("D4910-D4999", other_periodontal_services.activate_other_periodontal_services, 
                            "Other Periodontal Services (D4910-D4999)")
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing periodontic services."""
        return PromptTemplate(
            template=f"""
You are a highly experienced dental coding expert with over 15 years of expertise in ADA dental codes. 
Your task is to analyze the given scenario and determine the most applicable periodontal code range(s) based on the following classifications:

## **Surgical Services (D4210-D4286)**
**Use when:** Performing invasive periodontal procedures involving incisions and flap elevation.
**Check:** Documentation details the specific surgical approach, tissues involved, and treatment goals.
**Note:** These procedures address moderate to severe periodontal disease through surgical intervention.
**Activation trigger:** Scenario mentions OR implies any gum surgery, periodontal surgery, flap procedure, gingivectomy, graft placement, or surgical treatment of periodontal disease. INCLUDE this range if there's any indication of invasive treatment of gum or periodontal tissues.

## **Non-Surgical Periodontal Services (D4322-D4381)**
**Use when:** Providing non-invasive treatment for periodontal disease.
**Check:** Documentation specifies the extent of treatment and instruments/methods used.
**Note:** These procedures treat periodontal disease without surgical intervention.
**Activation trigger:** Scenario mentions OR implies any scaling and root planing, deep cleaning, periodontal debridement, non-surgical periodontal therapy, or treatment of gum disease without surgery. INCLUDE this range if there's any hint of non-surgical treatment of periodontal conditions.

## **Other Periodontal Services (D4910-D4999)**
**Use when:** Providing specialized periodontal care beyond routine treatment.
**Check:** Documentation details the specific service and its therapeutic purpose.
**Note:** These include maintenance treatments following active therapy and specialized interventions.
**Activation trigger:** Scenario mentions OR implies any periodontal maintenance, antimicrobial delivery, gingival irrigation, local drug delivery, or follow-up periodontal care. INCLUDE this range if there's any suggestion of ongoing periodontal management or specialized treatments.

### **Scenario:**
{{scenario}}
{PROMPT}

RESPOND WITH ALL APPLICABLE CODE RANGES from the options above, even if they are only slightly relevant.
List them in order of relevance, with the most relevant first.
Example: "D4322-D4381, D4910-D4999, D4210-D4286"
""",
            input_variables=["scenario"]
        )
    
    def analyze_periodontic(self, scenario: str) -> str:
        """Analyze the scenario to determine applicable code ranges."""
        try:
            print(f"Analyzing periodontic scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code_range = result.strip()
            print(f"Periodontic analyze_periodontic result: {code_range}")
            return code_range
        except Exception as e:
            print(f"Error in analyze_periodontic: {str(e)}")
            return ""
    
    async def activate_periodontic(self, scenario: str) -> dict:
        """Activate relevant subtopics in parallel and return detailed results."""
        try:
            # Get the code range from the analysis
            periodontic_result = self.analyze_periodontic(scenario)
            if not periodontic_result:
                print("No periodontic result returned")
                return {}
            
            print(f"Periodontic Result in activate_periodontic: {periodontic_result}")
            
            # Activate subtopics in parallel using the registry
            result = await self.registry.activate_all(scenario, periodontic_result)
            
            # Return a dictionary with the required fields
            return {
                "code_range": periodontic_result,
                "activated_subtopics": result["activated_subtopics"],
                "codes": result["topic_result"]
            }
        except Exception as e:
            print(f"Error in periodontic analysis: {str(e)}")
            return {}
    
    async def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = await self.activate_periodontic(scenario)
        print(f"\n=== PERIODONTIC ANALYSIS RESULT ===")
        print(f"CODE RANGE: {result.get('code_range', 'None')}")
        print(f"ACTIVATED SUBTOPICS: {', '.join(result.get('activated_subtopics', []))}")
        print(f"SPECIFIC CODES: {', '.join(result.get('codes', []))}")

periodontic_service = PeriodonticServices()
# Example usage
if __name__ == "__main__":
    async def main():
        scenario = input("Enter a periodontic scenario: ")
        await periodontic_service.run_analysis(scenario)
    
    asyncio.run(main())