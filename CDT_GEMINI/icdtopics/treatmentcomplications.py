"""
Module for extracting treatment complications ICD-10 codes.
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

class TreatmentComplicationsServices:
    """Class to analyze and extract Treatment Complications ICD-10 codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing Treatment Complications."""
        return PromptTemplate(
            template=f"""
You are an expert in dental medical coding, specifically for Treatment Complications related to dental procedures.
Analyze the given scenario and identify the most appropriate ICD-10 code(s).

Treatment Complications ICD-10 codes include:
T81: Complications of procedures, not elsewhere classified
T81.1: Postprocedural shock
T81.3: Disruption of operation wound, not elsewhere classified
T81.4: Infection following a procedure
T81.5: Foreign body accidentally left in body cavity or operation wound following procedure
T81.6: Acute reaction to foreign substance accidentally left during a procedure
T81.7: Vascular complications following a procedure, not elsewhere classified
T81.8: Other complications of procedures, not elsewhere classified (e.g., T81.83 Persistent postprocedural fistula)
T81.9: Unspecified complication of procedure
K91: Intraoperative and postprocedural complications and disorders of digestive system, not elsewhere classified
K91.840: Postprocedural hemorrhage of a digestive system organ or structure following a digestive system procedure
K91.841: Postprocedural hemorrhage of a digestive system organ or structure following other procedure
K91.89: Other postprocedural complications and disorders of digestive system
M96: Intraoperative and postprocedural complications and disorders of musculoskeletal system, not elsewhere classified
M96.830: Postprocedural hemorrhage of a musculoskeletal structure following a musculoskeletal system procedure
M96.831: Postprocedural hemorrhage of a musculoskeletal structure following other procedure
G97: Intraoperative and postprocedural complications and disorders of nervous system, not elsewhere classified
G97.0: Cerebrospinal fluid leak from spinal puncture
G97.1: Other reaction to spinal and lumbar puncture
G97.2: Intracranial hypotension following ventricular shunting
G97.81: Postprocedural hemorrhage of a nervous system organ or structure following a nervous system procedure
G97.82: Postprocedural hemorrhage of a nervous system organ or structure following other procedure
(Remember to add the 7th character for encounter type: A=initial, D=subsequent, S=sequela for T codes)

SCENARIO: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    async def extract_treatment_complications_code(self, scenario: str) -> dict:
        """Extract Treatment Complications code(s), explanation, doubt, and include raw data."""
        raw_result = ""
        try:
            print(f"Analyzing Treatment Complications scenario: {scenario[:100]}...")
            # Await the call
            raw_result = await self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            parsed_result = _parse_llm_topic_output(raw_result) # Use standardized helper
            print(f"Treatment Complications extracted: Code={parsed_result.get('code')}, Exp={parsed_result.get('explanation')}, Doubt={parsed_result.get('doubt')}")
            # Add raw data to the parsed result
            parsed_result['raw_data'] = raw_result
            return parsed_result # Return parsed dictionary with raw data
        except Exception as e:
            print(f"Error in Treatment Complications code extraction: {str(e)}")
            # Return error structure including raw data
            return {"code": None, "explanation": None, "doubt": None, "error": str(e), "raw_data": raw_result}
    
    async def activate_treatment_complications(self, scenario: str) -> dict:
        """Activate the Treatment Complications analysis and return simplified results."""
        try:
            # Await the extraction call which now returns the desired structure
            extraction_result = await self.extract_treatment_complications_code(scenario)

            # Check if code exists, otherwise log (or handle as needed)
            if not extraction_result.get("code") and not extraction_result.get("error") and extraction_result.get("raw_data"):
                 print("No Treatment Complications code or error returned, but raw data might be present.")

            return extraction_result # Return the dict directly
        except Exception as e:
            print(f"Error activating Treatment Complications analysis: {str(e)}")
            # Return error structure
            raw_data_fallback = None
            if 'extraction_result' in locals() and isinstance(extraction_result, dict):
                raw_data_fallback = extraction_result.get('raw_data')
            return {"code": None, "explanation": None, "doubt": None, "error": str(e), "raw_data": raw_data_fallback}
    
    async def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print simplified results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = await self.activate_treatment_complications(scenario) # Await the call
        print(f"\n=== TREATMENT COMPLICATIONS ANALYSIS RESULT ===")
        # Print simplified structured output
        print(f"CODE: {result.get('code', 'N/A')}")
        print(f"EXPLANATION: {result.get('explanation', 'N/A')}")
        print(f"DOUBT: {result.get('doubt', 'N/A')}")
        if result.get('error'): print(f"ERROR: {result.get('error')}")
        # Optional: Print raw data for debugging
        # print(f"RAW_DATA: {result.get('raw_data', 'N/A')}")


treatment_complications_service = TreatmentComplicationsServices()
# Example usage
if __name__ == "__main__":
    # Make main async
    async def main():
        scenario = input("Enter a scenario for Treatment Complications: ")
        await treatment_complications_service.run_analysis(scenario) # Await the call
    asyncio.run(main()) # Run the async main 