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
    
    def analyze_periodontic(self, scenario: str) -> dict: # Changed return type
        """Analyze the scenario and return parsed explanation, doubt, and code range."""
        try:
            print(f"Analyzing periodontic scenario: {scenario[:100]}...")
            raw_result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            parsed_result = _parse_llm_topic_output(raw_result) # Use helper
            print(f"Periodontic analyze result: Exp={parsed_result['explanation']}, Doubt={parsed_result['doubt']}, Range={parsed_result['code_range']}")
            return parsed_result # Return parsed dictionary
        except Exception as e:
            print(f"Error in analyze_periodontic: {str(e)}")
            return {"explanation": None, "doubt": None, "code_range": None, "error": str(e)}
    
    async def activate_periodontic(self, scenario: str) -> dict: # Changed return type and logic
        """Activate relevant subtopics in parallel and return detailed results including explanation and doubt."""
        final_result = {"explanation": None, "doubt": None, "code_range": None, "activated_subtopics": [], "codes": []}
        try:
            # Get the parsed analysis (explanation, doubt, code_range)
            topic_analysis_result = self.analyze_periodontic(scenario)
            
            # Store analysis results
            final_result["explanation"] = topic_analysis_result.get("explanation")
            final_result["doubt"] = topic_analysis_result.get("doubt")
            final_result["code_range"] = "D4000-D4999" # Main range for this topic
            
            code_range_string = topic_analysis_result.get("code_range")
            
            if code_range_string:
                print(f"Periodontic activate using code ranges: {code_range_string}")
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
                print("No applicable code ranges found in periodontic analysis.")
                
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
        print(f"EXPLANATION: {result.get('explanation', 'N/A')}")
        print(f"DOUBT: {result.get('doubt', 'N/A')}")
        print(f"CODE RANGE: {result.get('code_range', 'None')}")
        print(f"ACTIVATED SUBTOPICS: {', '.join(result.get('activated_subtopics', []))}")
        print(f"SPECIFIC CODES: {result.get('codes', [])}")

periodontic_service = PeriodonticServices()
# Example usage
if __name__ == "__main__":
    async def main():
        scenario = input("Enter a periodontic scenario: ")
        await periodontic_service.run_analysis(scenario)
    
    asyncio.run(main())