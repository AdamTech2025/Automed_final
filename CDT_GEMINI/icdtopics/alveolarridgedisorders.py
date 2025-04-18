"""
Module for extracting alveolar ridge disorders ICD-10 codes.
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
    # Adjusted regex to better capture code before Explanation or Doubt
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
         # Basic ICD-10 pattern: Letter followed by digits, optional dot and more digits
         direct_code_match = re.findall(r"\b([A-Z]\d{2}(\.\d{1,3})?)\b", result_text)
         if direct_code_match:
             # Join found codes with a comma
             parsed["code"] = ", ".join([match[0] for match in direct_code_match])
         # Note: raw_text is handled outside this parser function now

    return parsed

class AlveolarRidgeDisordersServices:
    """Class to analyze and extract alveolar ridge disorders ICD-10 codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing alveolar ridge disorders."""
        return PromptTemplate(
            template=f"""
You are a highly experienced medical coding expert specializing in alveolar ridge disorders. 
Analyze the given scenario and determine the most applicable ICD-10 code(s).

6.1 Atrophy of Alveolar Ridge:
- K08.20: Unspecified atrophy of edentulous alveolar ridge
- K08.21: Minimal atrophy of the mandible
- K08.22: Moderate atrophy of the mandible
- K08.23: Severe atrophy of the mandible
- K08.24: Minimal atrophy of maxilla
- K08.25: Moderate atrophy of the maxilla
- K08.26: Severe atrophy of the maxilla

6.2 Alveolar Anomalies:
- M26.71: Alveolar maxillary hyperplasia
- M26.72: Alveolar mandibular hyperplasia
- M26.73: Alveolar maxillary hypoplasia
- M26.74: Alveolar mandibular hypoplasia
- M26.79: Other specified alveolar anomalies

SCENARIO: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    async def extract_alveolar_ridge_disorders_code(self, scenario: str) -> dict:
        """Extract alveolar ridge disorders code(s), explanation, doubt, and include raw data."""
        raw_result = ""
        try:
            print(f"Analyzing alveolar ridge disorders scenario: {scenario[:100]}...")
            raw_result = await self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            parsed_result = _parse_llm_topic_output(raw_result)
            print(f"Alveolar ridge disorders extracted: Code={parsed_result.get('code')}, Exp={parsed_result.get('explanation')}, Doubt={parsed_result.get('doubt')}")
            # Add raw data to the parsed result
            parsed_result['raw_data'] = raw_result
            return parsed_result
        except Exception as e:
            print(f"Error in alveolar ridge disorders code extraction: {str(e)}")
            # Return error structure including raw data
            return {"code": None, "explanation": None, "doubt": None, "error": str(e), "raw_data": raw_result}
    
    async def activate_alveolar_ridge_disorders(self, scenario: str) -> dict:
        """Activate the alveolar ridge disorders analysis and return simplified results."""
        try:
            # Call the extract function which now returns the desired structure
            extraction_result = await self.extract_alveolar_ridge_disorders_code(scenario)
            
            # Check if code exists, otherwise log (or handle as needed)
            if not extraction_result.get("code") and not extraction_result.get("error"):
                 print("No alveolar ridge disorders code or error returned, but raw data might be present.")
                 # If raw_text was the only thing found by the parser (handled inside parser now)
                 # No, raw text is added in extract function always.

            return extraction_result # Return the dict directly
        except Exception as e:
            print(f"Error activating alveolar ridge disorders analysis: {str(e)}")
            # Return error structure
            # Attempt to get raw_data if extraction happened before the activate error
            raw_data_fallback = None
            if 'extraction_result' in locals() and isinstance(extraction_result, dict):
                raw_data_fallback = extraction_result.get('raw_data')
            return {"code": None, "explanation": None, "doubt": None, "error": str(e), "raw_data": raw_data_fallback}
    
    async def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print simplified results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = await self.activate_alveolar_ridge_disorders(scenario)
        print(f"\n=== ALVEOLAR RIDGE DISORDERS ANALYSIS RESULT ===")
        print(f"CODE: {result.get('code', 'N/A')}")
        print(f"EXPLANATION: {result.get('explanation', 'N/A')}")
        print(f"DOUBT: {result.get('doubt', 'N/A')}")
        if result.get('error'): print(f"ERROR: {result.get('error')}")
        # Optional: Print raw data for debugging
        # print(f"RAW_DATA: {result.get('raw_data', 'N/A')}")


alveolar_ridge_disorders_service = AlveolarRidgeDisordersServices()
# Example usage
if __name__ == "__main__":
    async def main(): 
        scenario = input("Enter an alveolar ridge disorders dental scenario: ")
        await alveolar_ridge_disorders_service.run_analysis(scenario)
    asyncio.run(main())
