"""
Module for extracting trauma and related conditions ICD-10 codes.
"""

import os
import sys
import asyncio
import re
from langchain.prompts import PromptTemplate
from llm_services import LLMService, get_service, set_model, set_temperature

# Add the parent directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(parent_dir)

# Import necessary modules
from icdtopics.prompt import PROMPT

# Standardized Helper function to parse LLM topic output
def _parse_llm_topic_output(result_text: str) -> dict:
    """
    Parses the LLM response string to extract CODE, EXPLANATION, and DOUBT.
    Assumes the format defined in prompt.py.
    """
    parsed = {"code": None, "explanation": None, "doubt": None}
    if not isinstance(result_text, str):
        return parsed # Return empty if input is not string

    # Extract Code (handle potential comma-separated codes)
    code_match = re.search(r"CODE:\s*(.*?)(?=\nEXPLANATION:|\nDOUBT:|$)", result_text, re.IGNORECASE | re.DOTALL)
    if code_match:
        code_str = code_match.group(1).strip()
        if code_str.lower() != 'none':
             parsed["code"] = code_str # Keep as string, might be comma-separated

    # Extract Explanation
    explanation_match = re.search(r"EXPLANATION:\s*(.*?)(?=\nDOUBT:|$)", result_text, re.DOTALL | re.IGNORECASE)
    if explanation_match:
        explanation_str = explanation_match.group(1).strip()
        if explanation_str.lower() != 'none':
            parsed["explanation"] = explanation_str

    # Extract Doubt
    doubt_match = re.search(r"DOUBT:\s*(.*)", result_text, re.DOTALL | re.IGNORECASE)
    if doubt_match:
        doubt_str = doubt_match.group(1).strip()
        if doubt_str.lower() != 'none':
            parsed["doubt"] = doubt_str

    # Handle case where only raw text is returned without markers
    if not parsed["code"] and not parsed["explanation"] and not parsed["doubt"] and result_text.strip():
         # Attempt to find a code pattern directly (allowing comma separation)
         direct_code_match = re.findall(r"\b([A-Z]\d{2}(\.\d{1,3})?)\b", result_text)
         if direct_code_match:
             # Join found codes with a comma
             parsed["code"] = ", ".join([match[0] for match in direct_code_match])
         # Note: raw_text is handled outside this parser function now

    return parsed

class TraumaRelatedConditionsServices:
    """Class to analyze and extract Trauma and Related Conditions ICD-10 codes based on dental scenarios."""

    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()

    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing Trauma and Related Conditions."""
        return PromptTemplate(
            template=f"""
You are an expert in dental medical coding, specifically for Trauma and Related Conditions relevant to dental care.
Analyze the given scenario and identify the most appropriate ICD-10 code(s).

Trauma and Related Conditions ICD-10 codes include:
# Fractures
S02.0: Fracture of vault of skull
S02.1: Fracture of base of skull
S02.2: Fracture of nasal bones
S02.3: Fracture of orbital floor
S02.4: Fracture of malar, maxillary and zygoma bones
S02.5: Fracture of tooth (traumatic) (Broken, Chipped, Fractured)
S02.6: Fracture of mandible
S02.8: Fractures of other specified skull and facial bones
S02.9: Fracture of skull and facial bones, part unspecified
# Dislocations and Sprains
S03.0: Dislocation of jaw
S03.1: Dislocation of septal cartilage of nose
S03.2: Dislocation of tooth
S03.4: Sprain of jaw
S03.8: Sprain of other specified parts of head
# Injuries to Nerves and Spinal Cord
S04.0: Injury of optic nerve and pathways
S04.1: Injury of oculomotor nerve
S04.2: Injury of trochlear nerve
S04.3: Injury of trigeminal nerve
S04.4: Injury of abducent nerve
S04.5: Injury of facial nerve
S04.6: Injury of acoustic nerve
S04.7: Injury of accessory nerve
S04.8: Injury of other cranial nerves
S04.9: Injury of unspecified cranial nerve
# Injuries to Blood Vessels
S05.0-S05.9: Injury of eye and orbit
S06.0-S06.9: Intracranial injury
# Crushing Injury & Traumatic Amputation
S07.0: Crushing injury of face
S07.1: Crushing injury of skull
S08.0: Avulsion of scalp
S08.1: Traumatic amputation of ear
S08.8: Traumatic amputation of other parts of head
S08.9: Traumatic amputation of unspecified part of head
# Other Injuries
S00: Superficial injury of head
S01: Open wound of head
S09: Other and unspecified injuries of head
S09.0: Injury of blood vessels of head, not elsewhere classified
S09.1: Injury of muscle and tendon of head
S09.2: Traumatic rupture of ear drum
S09.7: Multiple injuries of head
S09.8: Other specified injuries of head
S09.9: Unspecified injury of head
T14.1: Open wound of unspecified body region (use if site not specified)

(Remember to add the 7th character for encounter type: A=initial, D=subsequent, S=sequela)

SCENARIO: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )

    # Changed to async and return simplified dict with raw_data
    async def extract_trauma_related_conditions_code(self, scenario: str) -> dict:
        """Extract Trauma/Related Conditions code(s), explanation, doubt, and include raw data."""
        raw_result = ""
        try:
            print(f"Analyzing trauma/related conditions scenario: {scenario[:100]}...")
            # Run synchronous LLM call in a separate thread
            raw_result = await asyncio.to_thread(self.llm_service.invoke_chain, self.prompt_template, {"scenario": scenario})
            parsed_result = _parse_llm_topic_output(raw_result) # Use standardized helper
            print(f"Trauma/Related Conditions extracted: Code={parsed_result.get('code')}, Exp={parsed_result.get('explanation')}, Doubt={parsed_result.get('doubt')}")
            # Add raw data to the parsed result
            parsed_result['raw_data'] = raw_result
            return parsed_result # Return parsed dictionary with raw data
        except Exception as e:
            print(f"Error in Trauma Related Conditions code extraction: {str(e)}")
            # Return error structure including raw data
            return {"code": None, "explanation": None, "doubt": None, "error": str(e), "raw_data": raw_result}

    # Changed to async def, returns simplified dict
    async def activate_trauma_and_related_conditions(self, scenario: str) -> dict:
        """Activate the Trauma/Related Conditions analysis and return simplified results."""
        try:
            # Await the extraction call which now returns the desired structure
            extraction_result = await self.extract_trauma_related_conditions_code(scenario)

            # Check if code exists, otherwise log (or handle as needed)
            if not extraction_result.get("code") and not extraction_result.get("error") and extraction_result.get("raw_data"):
                 print("No Trauma Related Conditions code or error returned, but raw data might be present.")

            return extraction_result # Return the dict directly
        except Exception as e:
            print(f"Error activating Trauma Related Conditions analysis: {str(e)}")
            # Return error structure
            raw_data_fallback = None
            if 'extraction_result' in locals() and isinstance(extraction_result, dict):
                raw_data_fallback = extraction_result.get('raw_data')
            return {"code": None, "explanation": None, "doubt": None, "error": str(e), "raw_data": raw_data_fallback}

    # Changed to async, print simplified results
    async def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print simplified results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = await self.activate_trauma_and_related_conditions(scenario) # Await the call
        print(f"\n=== TRAUMA AND RELATED CONDITIONS ANALYSIS RESULT ===")
        # Print simplified structured output
        print(f"CODE: {result.get('code', 'N/A')}")
        print(f"EXPLANATION: {result.get('explanation', 'N/A')}")
        print(f"DOUBT: {result.get('doubt', 'N/A')}")
        if result.get('error'): print(f"ERROR: {result.get('error')}")
        # Optional: Print raw data for debugging
        # print(f"RAW_DATA: {result.get('raw_data', 'N/A')}")

trauma_related_conditions_service = TraumaRelatedConditionsServices()
# Example usage
if __name__ == "__main__":
    # Make main async
    async def main():
        scenario = input("Enter a scenario for Trauma and Related Conditions: ")
        await trauma_related_conditions_service.run_analysis(scenario) # Await the call
    asyncio.run(main()) # Run the async main
