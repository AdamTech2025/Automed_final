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
    from subtopics.AdjunctiveGeneralServices.anesthesia import anesthesia_service
    from subtopics.AdjunctiveGeneralServices.drugs import drugs_service
    from subtopics.AdjunctiveGeneralServices.miscellaneous_services import misc_service
    from subtopics.AdjunctiveGeneralServices.non_clinical_procedures import non_clinical_service
    from subtopics.AdjunctiveGeneralServices.professional_consultation import professional_consultation_service
    from subtopics.AdjunctiveGeneralServices.professional_visits import professional_visits_service
    from subtopics.AdjunctiveGeneralServices.unclassified_treatment import unclassified_service
except ImportError:
    print("Warning: Could not import subtopics for AdjunctiveGeneralServices. Using fallback functions.")
    # Define fallback functions if needed
    def activate_unclassified_treatment(scenario): return None
    def activate_anesthesia(scenario): return None
    def activate_professional_consultation(scenario): return None
    def activate_professional_visits(scenario): return None
    def activate_drugs(scenario): return None
    def activate_miscellaneous_services(scenario): return None
    def activate_non_clinical_procedures(scenario): return None

# Helper function to parse LLM activation results
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

class AdjunctiveGeneralServices:
    """Class to analyze and activate adjunctive general services based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
        self.registry = SubtopicRegistry()
        self._register_subtopics()
    
    def _register_subtopics(self):
        """Register all subtopics for parallel activation."""
        self.registry.register("D9110-D9130", unclassified_service.activate_unclassified_treatment, 
                            "Unclassified Treatment (D9110-D9130)")
        self.registry.register("D9210-D9248", anesthesia_service.activate_anesthesia, 
                            "Anesthesia (D9210-D9248)")
        self.registry.register("D9310-D9311", professional_consultation_service.activate_professional_consultation, 
                            "Professional Consultation (D9310-D9311)")
        self.registry.register("D9410-D9450", professional_visits_service.activate_professional_visits, 
                            "Professional Visits (D9410-D9450)")
        self.registry.register("D9610-D9630", drugs_service.activate_drugs, 
                            "Drugs (D9610-D9630)")
        self.registry.register("D9910-D9973", misc_service.activate_miscellaneous_services, 
                            "Miscellaneous Services (D9910-D9973)")
        self.registry.register("D9961-D9999", non_clinical_service.activate_non_clinical_procedures, 
                            "Non-clinical Procedures (D9961-D9999)")
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing adjunctive general services."""
        return PromptTemplate(
            template=f"""
You are a highly experienced dental coding expert with over 15 years of expertise in ADA dental codes. 
Your task is to analyze the given scenario and determine the most applicable adjunctive general services code range(s) based on the following detailed classifications:

## **Unclassified Treatment (D9110-D9130)**
**Use when:** Providing emergency palliative treatment or applying desensitizing medicament.
**Check:** Documentation clearly specifies the treatment provided to alleviate acute pain or address sensitivity.
**Note:** These codes are used for managing immediate comfort rather than definitive treatment.
**Activation trigger:** Scenario mentions OR implies any emergency pain relief, acute dental discomfort, or tooth sensitivity treatment. INCLUDE this range if there's any indication of palliative care or emergency pain management.

## **Anesthesia (D9210-D9248)**
**Use when:** Administering various forms of anesthesia or sedation for dental procedures.
**Check:** Documentation specifies the type of anesthesia used and the rationale for its selection.
**Note:** Different codes apply based on the type of anesthesia and administration method.
**Activation trigger:** Scenario mentions OR implies any anesthesia, sedation, numbing, pain control during procedures, nitrous oxide, or IV sedation. INCLUDE this range if there's any indication of pain control measures beyond topical agents.

## **Professional Consultation (D9310-D9311)**
**Use when:** Providing consultation services to other healthcare professionals or conducting specialized patient consultations.
**Check:** Documentation shows a consultation was specifically requested and details the findings/recommendations.
**Note:** These codes reflect services provided by a dentist other than the treating dentist.
**Activation trigger:** Scenario mentions OR implies any specialist consultation, second opinion, or referral for expert evaluation. INCLUDE this range if there's any suggestion of consultation services.

## **Professional Visits (D9410-D9450)**
**Use when:** Providing dental services outside the dental office or performing specialized case management.
**Check:** Documentation details the location of services or the specific case management provided.
**Note:** These codes reflect services provided in alternative settings or specialized case presentation.
**Activation trigger:** Scenario mentions OR implies any house calls, nursing facility visits, hospital visits, or specialized case presentations. INCLUDE this range if services are provided outside a standard dental office.

## **Drugs (D9610-D9630)**
**Use when:** Administering therapeutic drugs or dispensing medications for home use.
**Check:** Documentation specifies the medication, dosage, and clinical rationale.
**Note:** These codes exclude anesthetics used for procedures, which have their own codes.
**Activation trigger:** Scenario mentions OR implies any therapeutic drug administration, medication dispensing, or prescribed pharmaceuticals. INCLUDE this range if there's any indication of drug delivery or medication management.

## **Miscellaneous Services (D9910-D9973)**
**Use when:** Providing specialized services that don't fit into other categories.
**Check:** Documentation details the specific service and clinical necessity.
**Note:** These codes cover a wide range of adjunctive services from desensitization to bleaching.
**Activation trigger:** Scenario mentions OR implies any desensitization, occlusal analysis, cleaning or repair of prosthetics, bleaching, or other specialized adjunctive procedures. INCLUDE this range if there's any mention of specialized services that don't fit elsewhere.

## **Non-clinical Procedures (D9961-D9999)**
**Use when:** Performing administrative, preventive, or unclassified procedures.
**Check:** Documentation justifies the use of these codes with detailed explanations.
**Note:** These include specialized administrative services as well as unspecified procedures.
**Activation trigger:** Scenario mentions OR implies any duplicate appliances, dental case management, unspecified adjunctive procedures, or administrative services. INCLUDE this range if there's any suggestion of non-clinical management or undefined procedures.

### **Scenario:**
{{scenario}}
{PROMPT}
RESPOND WITH ALL APPLICABLE CODE RANGES from the options above, even if they are only slightly relevant.
List them in order of relevance, with the most relevant first.
Example: "D9210-D9248, D9110-D9130, D9610-D9630"
""",
            input_variables=["scenario"]
        )
    
    def analyze_adjunctive_general_services(self, scenario: str) -> dict: # Changed return type
        """Analyze the scenario and return parsed explanation, doubt, and code range."""
        try:
            print(f"Analyzing adjunctive general services scenario: {scenario[:100]}...")
            raw_result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            parsed_result = _parse_llm_topic_output(raw_result) # Use helper
            print(f"Adjunctive analyze result: Exp={parsed_result['explanation']}, Doubt={parsed_result['doubt']}, Range={parsed_result['code_range']}")
            return parsed_result # Return parsed dictionary
        except Exception as e:
            print(f"Error in analyze_adjunctive_general_services: {str(e)}")
            return {"explanation": None, "doubt": None, "code_range": None, "error": str(e)}
    
    async def activate_adjunctive_general_services(self, scenario: str) -> dict:
        """Activate relevant subtopics in parallel and return detailed results including explanation and doubt."""
        final_result = {"explanation": None, "doubt": None, "code_range": None, "activated_subtopics": [], "codes": []}
        try:
            # Get the parsed analysis (explanation, doubt, code_range)
            topic_analysis_result = self.analyze_adjunctive_general_services(scenario)
            
            # Store analysis results
            final_result["explanation"] = topic_analysis_result.get("explanation")
            final_result["doubt"] = topic_analysis_result.get("doubt")
            final_result["code_range"] = "D9000-D9999" # Main range for this topic
            
            code_range_string = topic_analysis_result.get("code_range")
            
            if code_range_string:
                print(f"Adjunctive activate using code ranges: {code_range_string}")
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
                print("No applicable code ranges found in adjunctive analysis.")
                
            return final_result
            
        except Exception as e:
            print(f"Error in adjunctive general services activation: {str(e)}")
            final_result["error"] = str(e)
            return final_result
    
    async def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = await self.activate_adjunctive_general_services(scenario)
        print(f"\n=== ADJUNCTIVE GENERAL SERVICES ANALYSIS RESULT ===")
        print(f"EXPLANATION: {result.get('explanation', 'N/A')}")
        print(f"DOUBT: {result.get('doubt', 'N/A')}")
        print(f"CODE RANGE: {result.get('code_range', 'None')}")
        print(f"ACTIVATED SUBTOPICS: {', '.join(result.get('activated_subtopics', []))}")
        print(f"SPECIFIC CODES: {result.get('codes', [])}") # Print list directly for clarity

adjunctive_general_services_service = AdjunctiveGeneralServices()
# Example usage
if __name__ == "__main__":
    async def main():
        scenario = input("Enter an adjunctive general services dental scenario: ")
        await adjunctive_general_services_service.run_analysis(scenario)
    
    asyncio.run(main())