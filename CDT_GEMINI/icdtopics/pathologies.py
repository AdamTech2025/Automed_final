"""
Module for extracting pathologies ICD-10 codes.
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

class PathologiesServices:
    """Class to analyze and extract Pathologies ICD-10 codes based on dental scenarios."""

    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()

    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing Pathologies."""
        return PromptTemplate(
            template=f"""
You are an expert in dental medical coding, specifically for Oral Pathologies.
Analyze the given scenario and identify the most appropriate ICD-10 code(s).

Oral Pathologies ICD-10 codes include:
# Inflammatory Conditions (Covered in K05, K06, K12, K13)
# Neoplasms (Covered in C00-C14, D00, D10, D16, D37, D48)
# Developmental Anomalies (Covered in K00, K01, K07, K10, Q35-Q38)
# Cysts
K09.0: Developmental odontogenic cysts (e.g., Dentigerous cyst, Eruption cyst, Primordial cyst)
K09.1: Developmental (nonodontogenic) cysts of oral region (e.g., Nasopalatine duct cyst, Globulomaxillary cyst)
K09.2: Other cysts of jaw (e.g., Aneurysmal bone cyst, Traumatic bone cyst)
K09.8: Other cysts of oral region, not elsewhere classified (e.g., Dermoid cyst, Lymphoepithelial cyst)
K09.9: Cyst of oral region, unspecified
K04.8: Radicular cyst (associated with non-vital tooth)
# Salivary Gland Diseases
K11.0: Atrophy of salivary gland
K11.1: Hypertrophy of salivary gland
K11.2: Sialoadenitis (Inflammation)
K11.3: Abscess of salivary gland
K11.4: Fistula of salivary gland
K11.5: Sialolithiasis (Salivary stones)
K11.6: Mucocele of salivary gland
K11.7: Disturbances of salivary secretion (Xerostomia, Ptyalism)
K11.8: Other diseases of salivary glands (e.g., Sialectasia, Sialosis)
K11.9: Disease of salivary gland, unspecified
# Other Oral Lesions
K13.0: Diseases of lips (Cheilitis, Angular cheilitis)
K13.1: Cheek and lip biting
K13.2: Leukoplakia and other disturbances of oral epithelium, including tongue
K13.3: Hairy leukoplakia
K13.4: Granuloma and granuloma-like lesions of oral mucosa (Pyogenic granuloma)
K13.5: Oral submucous fibrosis
K13.6: Irritative hyperplasia of oral mucosa
K13.7: Other and unspecified lesions of oral mucosa (e.g., Erythroplakia, Focal epithelial hyperplasia)
K14.0: Glossitis (Inflammation of tongue)
K14.1: Geographic tongue
K14.3: Hypertrophy of tongue papillae (Black hairy tongue)
K14.4: Atrophy of tongue papillae
K14.5: Plicated tongue (Fissured tongue)
K14.6: Glossodynia (Burning mouth syndrome)
K14.8: Other diseases of tongue
K14.9: Disease of tongue, unspecified
B00.2: Herpesviral gingivostomatitis and pharyngotonsillitis
B37.0: Candidal stomatitis (Thrush)

SCENARIO: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )

    # Changed to async and return simplified dict with raw_data
    async def extract_pathologies_code(self, scenario: str) -> dict:
        """Extract Pathologies code(s), explanation, doubt, and include raw data."""
        raw_result = ""
        try:
            print(f"Analyzing pathologies scenario: {scenario[:100]}...")
            # Run synchronous LLM call in a separate thread
            raw_result = await asyncio.to_thread(self.llm_service.invoke_chain, self.prompt_template, {"scenario": scenario})
            parsed_result = _parse_llm_topic_output(raw_result) # Use standardized helper
            print(f"Pathologies extracted: Code={parsed_result.get('code')}, Exp={parsed_result.get('explanation')}, Doubt={parsed_result.get('doubt')}")
            # Add raw data to the parsed result
            parsed_result['raw_data'] = raw_result
            return parsed_result # Return parsed dictionary with raw data
        except Exception as e:
            print(f"Error in Pathologies code extraction: {str(e)}")
            # Return error structure including raw data
            return {"code": None, "explanation": None, "doubt": None, "error": str(e), "raw_data": raw_result}

    # Changed to async def, returns simplified dict
    async def activate_pathologies(self, scenario: str) -> dict:
        """Activate the Pathologies analysis and return simplified results."""
        try:
            # Await the extraction call which now returns the desired structure
            extraction_result = await self.extract_pathologies_code(scenario)

            # Check if code exists, otherwise log (or handle as needed)
            if not extraction_result.get("code") and not extraction_result.get("error") and extraction_result.get("raw_data"):
                 print("No Pathologies code or error returned, but raw data might be present.")

            return extraction_result # Return the dict directly
        except Exception as e:
            print(f"Error activating Pathologies analysis: {str(e)}")
            # Return error structure
            raw_data_fallback = None
            if 'extraction_result' in locals() and isinstance(extraction_result, dict):
                raw_data_fallback = extraction_result.get('raw_data')
            return {"code": None, "explanation": None, "doubt": None, "error": str(e), "raw_data": raw_data_fallback}

    # Changed to async, print simplified results
    async def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print simplified results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = await self.activate_pathologies(scenario) # Await the call
        print(f"\n=== PATHOLOGIES ANALYSIS RESULT ===")
        # Print simplified structured output
        print(f"CODE: {result.get('code', 'N/A')}")
        print(f"EXPLANATION: {result.get('explanation', 'N/A')}")
        print(f"DOUBT: {result.get('doubt', 'N/A')}")
        if result.get('error'): print(f"ERROR: {result.get('error')}")
        # Optional: Print raw data for debugging
        # print(f"RAW_DATA: {result.get('raw_data', 'N/A')}")

pathologies_service = PathologiesServices()
# Example usage
if __name__ == "__main__":
    # Make main async
    async def main():
        scenario = input("Enter a scenario for Oral Pathologies: ")
        await pathologies_service.run_analysis(scenario) # Await the call
    asyncio.run(main()) # Run the async main
