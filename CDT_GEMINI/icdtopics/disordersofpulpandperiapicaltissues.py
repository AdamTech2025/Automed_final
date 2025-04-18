"""
Module for extracting disorders of pulp and periapical tissues ICD-10 codes.
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

# Import modules
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

class DisordersOfPulpAndPeriapicalTissuesServices:
    """Class to analyze and extract disorders of pulp and periapical tissues ICD-10 codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing disorders of pulp and periapical tissues."""
        return PromptTemplate(
            template=f"""
You are an expert in dental medical coding, specifically for Disorders of Pulp and Periapical Tissues.
Analyze the given scenario and identify the most appropriate ICD-10 code(s).

Disorders of Pulp and Periapical Tissues ICD-10 codes include:
K04.0: Pulpitis
K04.1: Necrosis of pulp
K04.2: Pulp degeneration
K04.3: Abnormal hard tissue formation in pulp
K04.4: Acute apical periodontitis of pulpal origin
K04.5: Chronic apical periodontitis
K04.6: Periapical abscess with sinus
K04.7: Periapical abscess without sinus
K04.8: Radicular cyst
K04.9: Other and unspecified diseases of pulp and periapical tissues

SCENARIO: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    # Changed to async and return simplified dict with raw_data
    async def extract_pulp_periapical_code(self, scenario: str) -> dict:
        """Extract pulp/periapical code(s), explanation, doubt, and include raw data."""
        raw_result = ""
        try:
            print(f"Analyzing pulp/periapical scenario: {scenario[:100]}...")
            # Await the call
            raw_result = await asyncio.to_thread(self.llm_service.invoke_chain, self.prompt_template, {"scenario": scenario})
            parsed_result = _parse_llm_topic_output(raw_result) # Use standardized helper
            print(f"Pulp/Periapical extracted: Code={parsed_result.get('code')}, Exp={parsed_result.get('explanation')}, Doubt={parsed_result.get('doubt')}")
            # Add raw data to the parsed result
            parsed_result['raw_data'] = raw_result
            return parsed_result # Return parsed dictionary with raw data
        except Exception as e:
            print(f"Error in pulp/periapical code extraction: {str(e)}")
            # Return error structure including raw data
            return {"code": None, "explanation": None, "doubt": None, "error": str(e), "raw_data": raw_result}
    
    # Changed to async def, returns simplified dict
    async def activate_disorders_of_pulp_and_periapical_tissues(self, scenario: str) -> dict:
        """Activate the pulp/periapical analysis and return simplified results."""
        try:
            # Await the extraction call which now returns the desired structure
            extraction_result = await self.extract_pulp_periapical_code(scenario)

            # Check if code exists, otherwise log (or handle as needed)
            if not extraction_result.get("code") and not extraction_result.get("error") and extraction_result.get("raw_data"):
                 print("No pulp/periapical code or error returned, but raw data might be present.")
            
            return extraction_result # Return the dict directly
        except Exception as e:
            print(f"Error activating pulp/periapical analysis: {str(e)}")
            # Return error structure
            raw_data_fallback = None
            if 'extraction_result' in locals() and isinstance(extraction_result, dict):
                raw_data_fallback = extraction_result.get('raw_data')
            return {"code": None, "explanation": None, "doubt": None, "error": str(e), "raw_data": raw_data_fallback}
    
    # Changed to async, print simplified results
    async def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print simplified results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = await self.activate_disorders_of_pulp_and_periapical_tissues(scenario) # Await the call
        print(f"\n=== PULP/PERIAPICAL TISSUES ANALYSIS RESULT ===")
        # Print simplified structured output
        print(f"CODE: {result.get('code', 'N/A')}")
        print(f"EXPLANATION: {result.get('explanation', 'N/A')}")
        print(f"DOUBT: {result.get('doubt', 'N/A')}")
        if result.get('error'): print(f"ERROR: {result.get('error')}")
        # Optional: Print raw data for debugging
        # print(f"RAW_DATA: {result.get('raw_data', 'N/A')}")

disorders_of_pulp_and_periapical_tissues_service = DisordersOfPulpAndPeriapicalTissuesServices()
# Example usage
if __name__ == "__main__":
    # Make main async
    async def main():
        scenario = input("Enter a scenario for disorders of pulp and periapical tissues: ")
        await disorders_of_pulp_and_periapical_tissues_service.run_analysis(scenario) # Await the call
    asyncio.run(main()) # Run the async main
