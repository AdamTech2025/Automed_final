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

# Helper function removed


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
    
    def analyze_periodontic(self, scenario: str) -> dict: # Changed return type to dict
        """Analyze the scenario and return raw LLM output and the applicable code range string."""
        result = {"raw_output": None, "code_range": None}
        try:
            print(f"Analyzing periodontic scenario: {scenario[:100]}...")
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
                 print(f"Periodontic analyze result: Found Code Range={code_range_string}")
            else:
                 print("Periodontic analyze result: No applicable code range found in raw output.")
                    
            return result
                    
        except Exception as e:
            print(f"Error in analyze_periodontic: {str(e)}")
            result["error"] = str(e)
            return result
    
    async def activate_periodontic(self, scenario: str) -> dict: # Changed return type and logic
        """Activate relevant subtopics in parallel based on LLM-identified code ranges."""
        # Consistent final result structure
        final_result = {"raw_topic_data": None, "code_range": "D4000-D4999", "activated_subtopics": [], "subtopics_data": [], "error": None}
        try:
            # Get the analysis result dictionary
            analysis_result = self.analyze_periodontic(scenario)
            
            # Store raw output
            final_result["raw_topic_data"] = analysis_result.get("raw_output")

            # Check for analysis errors
            if analysis_result.get("error"):
                final_result["error"] = f"Analysis Error: {analysis_result['error']}"
                return final_result
            
            # Get code range string
            code_range_string = analysis_result.get("code_range")
            
            if code_range_string:
                print(f"Periodontic activate using code ranges: {code_range_string}")
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
                print("No applicable code ranges identified by LLM for periodontic analysis.")
                
            # Clear error key if no error occurred
            if final_result.get("error") is None:
                 try: del final_result["error"]
                 except KeyError: pass

            return final_result
            
        except Exception as e:
            print(f"Error in periodontic activation: {str(e)}")
            final_result["error"] = str(e)
            return final_result
    
    async def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = await self.activate_periodontic(scenario)
        print(f"\n=== PERIODONTIC ANALYSIS RESULT ===")
        # Updated printing logic
        print(f"RAW TOPIC DATA:\n---\n{result.get('raw_topic_data', 'N/A')}\n---")
        print(f"OVERALL TOPIC CODE RANGE: {result.get('code_range', 'None')}")
        print(f"ACTIVATED SUBTOPICS: {', '.join(result.get('activated_subtopics', []))}")
        print(f"SUBTOPICS DATA: {result.get('subtopics_data', [])}")
        if 'error' in result:
            print(f"ERROR: {result['error']}")

periodontic_service = PeriodonticServices()
# Example usage
if __name__ == "__main__":
    async def main():
        scenario = input("Enter a periodontic scenario: ")
        await periodontic_service.run_analysis(scenario)
    
    asyncio.run(main())