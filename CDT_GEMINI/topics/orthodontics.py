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
    
    def analyze_orthodontic(self, scenario: str) -> dict: # Changed return type
        """Analyze the scenario and return parsed explanation, doubt, and code range."""
        try:
            print(f"Analyzing orthodontic scenario: {scenario[:100]}...")
            raw_result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            parsed_result = _parse_llm_topic_output(raw_result) # Use helper
            print(f"Orthodontic analyze result: Exp={parsed_result['explanation']}, Doubt={parsed_result['doubt']}, Range={parsed_result['code_range']}")
            return parsed_result # Return parsed dictionary
        except Exception as e:
            print(f"Error in analyze_orthodontic: {str(e)}")
            return {"explanation": None, "doubt": None, "code_range": None, "error": str(e)}
    
    async def activate_orthodontic(self, scenario: str) -> dict: # Changed return type and logic
        """Activate relevant subtopics in parallel and return detailed results including explanation and doubt."""
        final_result = {"explanation": None, "doubt": None, "code_range": None, "activated_subtopics": [], "codes": []}
        try:
            # Get the parsed analysis (explanation, doubt, code_range)
            topic_analysis_result = self.analyze_orthodontic(scenario)
            
            # Store analysis results
            final_result["explanation"] = topic_analysis_result.get("explanation")
            final_result["doubt"] = topic_analysis_result.get("doubt")
            final_result["code_range"] = "D8000-D8999" # Main range for this topic
            
            code_range_string = topic_analysis_result.get("code_range")
            
            if code_range_string:
                print(f"Orthodontic activate using code ranges: {code_range_string}")
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
                print("No applicable code ranges found in orthodontic analysis.")
                
            return final_result
            
        except Exception as e:
            print(f"Error in orthodontic activation: {str(e)}")
            final_result["error"] = str(e)
            return final_result
    
    async def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = await self.activate_orthodontic(scenario)
        print(f"\n=== ORTHODONTIC ANALYSIS RESULT ===")
        print(f"EXPLANATION: {result.get('explanation', 'N/A')}")
        print(f"DOUBT: {result.get('doubt', 'N/A')}")
        print(f"CODE RANGE: {result.get('code_range', 'None')}")
        print(f"ACTIVATED SUBTOPICS: {', '.join(result.get('activated_subtopics', []))}")
        print(f"SPECIFIC CODES: {result.get('codes', [])}")

orthodontic_service = OrthodonticServices()
# Example usage
if __name__ == "__main__":
    async def main():
        orthodontic_service = OrthodonticServices()
        scenario = input("Enter an orthodontic scenario: ")
        await orthodontic_service.run_analysis(scenario)
    
    asyncio.run(main())