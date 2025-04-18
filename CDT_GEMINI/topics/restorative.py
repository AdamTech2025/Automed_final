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
from subtopics.Restorative.amalgam_restorations import AmalgamRestorationsServices
from subtopics.Restorative.resin_based_composite_restorations import ResinBasedCompositeRestorationsServices
from subtopics.Restorative.gold_foil_restorations import GoldFoilRestorationsServices
from subtopics.Restorative.inlays_and_onlays import InlaysAndOnlaysServices
from subtopics.Restorative.crowns import CrownsServices
from subtopics.Restorative.other_restorative_services import OtherRestorativeServices

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

class RestorativeServices:
    """Class to analyze and activate restorative services based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
        
        # Initialize the subtopic service classes - needed if calling instance methods
        self.amalgam_restorations = AmalgamRestorationsServices(self.llm_service)
        self.resin_based_composite_restorations = ResinBasedCompositeRestorationsServices(self.llm_service)
        self.gold_foil_restorations = GoldFoilRestorationsServices(self.llm_service)
        self.inlays_and_onlays = InlaysAndOnlaysServices(self.llm_service)
        self.crowns = CrownsServices(self.llm_service)
        self.other_restorative_services = OtherRestorativeServices(self.llm_service)
        
        self.registry = SubtopicRegistry()
        self._register_subtopics()
    
    def _register_subtopics(self):
        """Register all subtopics for parallel activation."""
        # Assuming instance methods are used based on __init__
        self.registry.register("D2140-D2161", self.amalgam_restorations.activate_amalgam_restorations, 
                            "Amalgam Restorations (D2140-D2161)")
        self.registry.register("D2330-D2394", self.resin_based_composite_restorations.activate_resin_based_composite_restorations, 
                            "Resin-Based Composite Restorations (D2330-D2394)")
        self.registry.register("D2410-D2430", self.gold_foil_restorations.activate_gold_foil_restorations, 
                            "Gold Foil Restorations (D2410-D2430)")
        self.registry.register("D2510-D2664", self.inlays_and_onlays.activate_inlays_and_onlays, 
                            "Inlays and Onlays (D2510-D2664)")
        self.registry.register("D2710-D2799", self.crowns.activate_crowns, 
                            "Crowns (D2710-D2799)")
        self.registry.register("D2910-D2999", self.other_restorative_services.activate_other_restorative_services, 
                            "Other Restorative Services (D2910-D2999)")
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing restorative services."""
        return PromptTemplate(
            template=f"""
You are a highly experienced dental coding expert with over 15 years of expertise in ADA dental codes. 
Your task is to analyze the given scenario and determine the most applicable restorative code range(s) based on the following classifications:

## **Amalgam Restorations (D2140-D2161)**
**Use when:** Placing silver-colored metal alloy fillings.
**Check:** Documentation specifies the number of surfaces involved and tooth location.
**Note:** These durable restorations are typically used for posterior teeth.
**Activation trigger:** Scenario mentions OR implies any amalgam filling, silver filling, metallic restoration, posterior filling, or direct restoration with amalgam. INCLUDE this range if there's any indication of silver-colored fillings being placed.

## **Resin-Based Composite Restorations (D2330-D2394)**
**Use when:** Placing tooth-colored fillings made of composite resin.
**Check:** Documentation details the number of surfaces involved and tooth location.
**Note:** These esthetic restorations can be used in anterior or posterior teeth.
**Activation trigger:** Scenario mentions OR implies any composite filling, tooth-colored restoration, resin restoration, bonded filling, or esthetic direct restoration. INCLUDE this range if there's any hint of tooth-colored fillings being placed.

## **Gold Foil Restorations (D2410-D2430)**
**Use when:** Placing pure gold restorations through direct techniques.
**Check:** Documentation identifies the number of surfaces and specific gold foil technique.
**Note:** These are specialized, less common restorations using pure gold.
**Activation trigger:** Scenario mentions OR implies any gold foil, direct gold restoration, or traditional gold filling technique. INCLUDE this range if there's any suggestion of pure gold being used in a direct restoration technique.

## **Inlays and Onlays (D2510-D2664)**
**Use when:** Providing laboratory-fabricated partial coverage restorations.
**Check:** Documentation specifies the material used and extent of cuspal coverage.
**Note:** These indirect restorations offer precision fit for moderate to large lesions.
**Activation trigger:** Scenario mentions OR implies any inlay, onlay, indirect restoration, laboratory-fabricated partial coverage, or precision-fitted restoration. INCLUDE this range if there's any indication of indirect partial coverage restorations.

## **Crowns (D2710-D2799)**
**Use when:** Providing full-coverage restorations for damaged teeth.
**Check:** Documentation details the crown material and reason for full coverage.
**Note:** These restore severely damaged teeth requiring complete coronal protection.
**Activation trigger:** Scenario mentions OR implies any crown, full coverage restoration, cap, coronal coverage, or complete tooth restoration. INCLUDE this range if there's any hint of full coverage restorations being provided.

## **Other Restorative Services (D2910-D2999)**
**Use when:** Providing additional services related to restorations.
**Check:** Documentation specifies the exact service and its purpose.
**Note:** These include repairs, recementations, cores, posts, and specialized services.
**Activation trigger:** Scenario mentions OR implies any core buildup, post and core, resin infiltration, temporary restoration, crown repair, veneer, reattachment of fragment, or specialized restorative service. INCLUDE this range if there's any suggestion of restorative services beyond standard fillings or crowns.

### **Scenario:**
{{scenario}}
{PROMPT}

RESPOND WITH ALL APPLICABLE CODE RANGES from the options above, even if they are only slightly relevant.
List them in order of relevance, with the most relevant first.
""",
            input_variables=["scenario"]
        )
    
    def analyze_restorative(self, scenario: str) -> dict: # Changed return type
        """Analyze the scenario and return parsed explanation, doubt, and code range."""
        try:
            print(f"Analyzing restorative scenario: {scenario[:100]}...")
            raw_result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            parsed_result = _parse_llm_topic_output(raw_result) # Use helper
            print(f"Restorative analyze result: Exp={parsed_result['explanation']}, Doubt={parsed_result['doubt']}, Range={parsed_result['code_range']}")
            return parsed_result # Return parsed dictionary
        except Exception as e:
            print(f"Error in analyze_restorative: {str(e)}")
            return {"explanation": None, "doubt": None, "code_range": None, "error": str(e)}
    
    async def activate_restorative(self, scenario: str) -> dict: # Changed return type and logic
        """Activate relevant subtopics in parallel and return detailed results including explanation and doubt."""
        final_result = {"explanation": None, "doubt": None, "code_range": None, "activated_subtopics": [], "codes": []}
        try:
            # Get the parsed analysis (explanation, doubt, code_range)
            topic_analysis_result = self.analyze_restorative(scenario)
            
            # Store analysis results
            final_result["explanation"] = topic_analysis_result.get("explanation")
            final_result["doubt"] = topic_analysis_result.get("doubt")
            final_result["code_range"] = "D2000-D2999" # Main range for this topic
            
            code_range_string = topic_analysis_result.get("code_range")
            
            if code_range_string:
                print(f"Restorative activate using code ranges: {code_range_string}")
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
                print("No applicable code ranges found in restorative analysis.")
                
            return final_result
            
        except Exception as e:
            print(f"Error in restorative activation: {str(e)}")
            final_result["error"] = str(e)
            return final_result
    
    async def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = await self.activate_restorative(scenario)
        print(f"\n=== RESTORATIVE ANALYSIS RESULT ===")
        print(f"EXPLANATION: {result.get('explanation', 'N/A')}")
        print(f"DOUBT: {result.get('doubt', 'N/A')}")
        print(f"CODE RANGE: {result.get('code_range', 'None')}")
        print(f"ACTIVATED SUBTOPICS: {', '.join(result.get('activated_subtopics', []))}")
        print(f"SPECIFIC CODES: {result.get('codes', [])}")

restorative_service = RestorativeServices()
# Example usage
if __name__ == "__main__":
    async def main():
        restorative_service = RestorativeServices()
        scenario = input("Enter a restorative dental scenario: ")
        await restorative_service.run_analysis(scenario)
    
    asyncio.run(main())