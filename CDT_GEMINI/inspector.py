import os
import logging
from dotenv import load_dotenv
from llm_services import generate_response, get_service, set_model, set_temperature
from typing import Dict, Any, Optional
from llm_services import OPENROUTER_MODEL, DEFAULT_TEMP

# Load environment variables
load_dotenv()

# Set a specific model for this file (optional)
# set_model_for_file("gemini-2.0-flash-thinking-exp-01-21")

class DentalInspector:
    """Class to handle dental code inspection with configurable prompts and settings"""
    
    PROMPT_TEMPLATE = """
You are the final code selector ("Inspector") with extensive expertise in dental coding. Your task is to perform a thorough analysis of the provided scenario along with the candidate CDT code outputs—including all explanations and doubts—from previous subtopics. Your final output must include only the CDT code(s) that are justified by the scenario, with minimal assumptions.

Scenario:
{scenario}

Topic Analysis Results:
{topic_analysis}

Additional Information from Questions (if any):
{questioner_data}

Instructions:

1) Carefully read the complete clinical scenario provided.

2) Review ALL candidate CDT codes suggested by previous subtopics along with their explanations and any doubts raised. Every code that appears in the Topic Analysis Results is a candidate for selection or rejection.

3) Use ONLY Provided Codes: Only consider and select from the SPECIFIC CDT codes that were actually presented in the topic analysis results. Do not introduce new codes that weren't part of the original analysis.

4) Evaluate EVERY Code: You must evaluate each specific code (like D0160, D7210, etc.) in the topic analysis results and either select it or reject it.

5) Reasonable Assumptions: You may make basic clinical assumptions that are standard in dental practice, but avoid making significant assumptions about unstated procedures.

6) Justification: Select codes that are reasonably supported by the scenario. If a code has minor doubts but is likely correct based on the context, include it.

7) Mutually Exclusive Codes: When presented with mutually exclusive codes, choose the one that is best justified for the specific visit. Do not bill for the same procedure twice.

8) Revenue & Defensibility: Your selection should maximize revenue while ensuring billing is defensible, but don't reject codes unnecessarily.

9) Consider Additional QA: Incorporate any additional information or clarifications provided through the question-answer process.

10) Output the same code multiple times if it is applicable (e.g., 8 scans would include the code 8 times).


IMPORTANT: You must format your response exactly as follows:

EXPLANATION: [provide a detailed explanation for why each code was selected or rejected. Include specific reasoning for each code mentioned in the topic analysis.]

CODES: [comma-separated list of CDT codes that are accepted, with no square brackets around individual codes]

REJECTED CODES: [comma-separated list of CDT codes that were considered but rejected, with no square brackets around individual codes. Only list codes that were actually analyzed in the topic analysis and are explicitly contradicted by the scenario.]

For example:

EXPLANATION: D0120 (periodic oral evaluation) is appropriate as this was a regular dental visit. D0274 (bitewings-four radiographs) is included because the scenario mentions taking four bitewing x-rays. D1110 (prophylaxis-adult) is included as the scenario describes cleaning of teeth for an adult patient. D0140 was rejected because this was not an emergency visit. D0220 was rejected as no periapical films were mentioned. D0230 was rejected as no additional periapical films were mentioned.
CODES: D0120, D0274, D1110
REJECTED CODES: D0140, D0220, D0230
"""

    def __init__(self, model: str = OPENROUTER_MODEL, temperature: float = DEFAULT_TEMP):
        """Initialize the inspector with model and temperature settings"""
        self.service = get_service()
        self.configure(model, temperature)
        self.logger = self._setup_logging()

    def _setup_logging(self) -> logging.Logger:
        """Configure logging for the inspector module"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[logging.StreamHandler()]
        )
        return logging.getLogger(__name__)

    def configure(self, model: Optional[str] = None, temperature: Optional[float] = None) -> None:
        """Configure model and temperature settings"""
        if model:
            set_model(model)
        if temperature is not None:
            set_temperature(temperature)

    def format_prompt(self, scenario: str, topic_analysis: Any, questioner_data: Any = None) -> str:
        """Format the prompt template with the given inputs"""
        topic_analysis_str = self._format_topic_analysis(topic_analysis)
        questioner_data_str = self._format_questioner_data(questioner_data)
        
        return self.PROMPT_TEMPLATE.format(
            scenario=scenario,
            topic_analysis=topic_analysis_str,
            questioner_data=questioner_data_str
        )

    def _format_topic_analysis(self, topic_analysis: Any) -> str:
        """Format topic analysis data with clear emphasis on candidate codes"""
        if topic_analysis is None:
            return "No CDT data analysis data available in DB"
        
        if isinstance(topic_analysis, dict):
            formatted_topics = []
            all_candidate_codes = []
            
            # First collect all specific candidate codes for clear visibility
            for code_range, topic_data in topic_analysis.items():
                result = topic_data.get("result", "")
                if isinstance(result, str) and "[" in result:
                    # This might be a string representation of a list of codes
                    try:
                        # Try to extract codes from the string representation
                        import re
                        code_pattern = r'D\d{4}'  # Pattern to match D followed by 4 digits
                        codes = re.findall(code_pattern, result)
                        all_candidate_codes.extend(codes)
                    except:
                        pass
            
            # Then format the full topic data
            for code_range, topic_data in topic_analysis.items():
                topic_name = topic_data.get("name", "Unknown")
                topic_result = topic_data.get("result", "No result")
                formatted_topics.append(f"{topic_name} ({code_range}):\n{topic_result}")
            
            # Add a clear summary of all candidate codes at the top
            if all_candidate_codes:
                formatted_topics.insert(0, f"ALL CANDIDATE CODES FOR REVIEW: {', '.join(sorted(set(all_candidate_codes)))}\n")
                
            return "\n\n".join(formatted_topics)
        
        return str(topic_analysis)

    def _format_questioner_data(self, questioner_data: Any) -> str:
        """Format questioner data"""
        if questioner_data is None:
            return "No additional information provided."
        
        if isinstance(questioner_data, dict):
            qa_pairs = []
            if questioner_data.get("has_questions", False) and questioner_data.get("has_answers", False):
                answers = questioner_data.get("answers", {})
                
                for q_type in ["cdt_questions", "icd_questions"]:
                    questions = questioner_data.get(q_type, {}).get("questions", [])
                    prefix = q_type.split("_")[0].upper()
                    for question in questions:
                        answer = answers.get(question, "No answer provided")
                        qa_pairs.append(f"{prefix} Q: {question}\nA: {answer}")
                
                return "\n".join(qa_pairs) if qa_pairs else "Questions were asked but no answers were provided."
            elif questioner_data.get("has_questions", False):
                return "Questions were identified but not yet answered."
            return "No additional questions were needed."
        
        return str(questioner_data)

    def parse_response(self, response: str) -> Dict[str, Any]:
        """Parse the LLM response into structured format"""
        codes_line = ""
        explanation_line = ""
        rejected_codes_line = ""
        
        lines = response.strip().split('\n')
        in_explanation = False
        
        for line in lines:
            line = line.strip()
            
            if line.upper().startswith("CODES:"):
                codes_line = line.split(":", 1)[1].strip()
            elif line.upper().startswith("REJECTED CODES:"):
                rejected_codes_line = line.split(":", 1)[1].strip()
            elif line.upper().startswith("EXPLANATION:"):
                in_explanation = True
                explanation_line = line.split(":", 1)[1].strip()
            elif in_explanation and line:
                explanation_line += " " + line

        cleaned_codes = self._clean_codes(codes_line)
        rejected_codes = self._clean_codes(rejected_codes_line)
        
        return {
            "codes": cleaned_codes,
            "rejected_codes": rejected_codes,
            "explanation": explanation_line
        }

    def _clean_codes(self, codes_line: str) -> list:
        """Clean and format codes from response"""
        cleaned = []
        if codes_line:
            codes_line = codes_line.strip('[]')
            for code in codes_line.split(','):
                clean_code = code.strip().strip('[]')
                if clean_code and clean_code.lower() != 'none' and '*' not in clean_code:
                    cleaned.append(clean_code)
        return cleaned

    def process(self, scenario: str, topic_analysis: Any = None, questioner_data: Any = None) -> Dict[str, Any]:
        """Process a dental scenario and return inspection results"""
        try:
            # Print detailed debug info about data going to inspectors
            print("\n" + "*"*50)
            print("**** CDT INSPECTOR RECEIVED DATA ****")
            print("*"*50)
            print(f"SCENARIO TYPE: {type(scenario)}")
            print(f"SCENARIO PREVIEW: {scenario[:100]}...")

            print(f"\nTOPIC_ANALYSIS TYPE: {type(topic_analysis)}")
            if isinstance(topic_analysis, list):
                print(f"TOPIC_ANALYSIS LIST LENGTH: {len(topic_analysis)}")
                if len(topic_analysis) > 0:
                    print(f"FIRST ITEM TYPE: {type(topic_analysis[0])}")
                    if isinstance(topic_analysis[0], dict):
                        print(f"FIRST ITEM KEYS: {list(topic_analysis[0].keys())}")
                        if 'codes' in topic_analysis[0]:
                            print(f"CODES TYPE: {type(topic_analysis[0]['codes'])}")
                            print(f"CODES LENGTH: {len(topic_analysis[0]['codes']) if isinstance(topic_analysis[0]['codes'], list) else 'Not a list'}")
                            if isinstance(topic_analysis[0]['codes'], list) and len(topic_analysis[0]['codes']) > 0:
                                print(f"FIRST CODE KEYS: {list(topic_analysis[0]['codes'][0].keys()) if isinstance(topic_analysis[0]['codes'][0], dict) else 'Not a dict'}")
            elif isinstance(topic_analysis, dict):
                print(f"TOPIC_ANALYSIS DICT KEYS: {list(topic_analysis.keys())}")
                # Print a few key/value pairs for illustration
                for key in list(topic_analysis.keys())[:2]:  # First 2 keys
                    print(f"  KEY: {key}, VALUE TYPE: {type(topic_analysis[key])}")
            else:
                print(f"TOPIC_ANALYSIS VALUE: {str(topic_analysis)[:200]}")

            print(f"\nQUESTIONER_DATA TYPE: {type(questioner_data)}")
            if isinstance(questioner_data, dict):
                print(f"QUESTIONER_DATA KEYS: {list(questioner_data.keys())}")
            else:
                print(f"QUESTIONER_DATA VALUE: {str(questioner_data)[:200]}")
            print("*"*50)
            
            # Print full data content for all three parameters
            print("\n" + "="*80)
            print("FULL DATA RECEIVED BY INSPECTOR")
            print("="*80)
            
            print("\n[SCENARIO FULL TEXT]:")
            print(scenario)
            
            print("\n[TOPIC_ANALYSIS FULL CONTENT]:")
            import json
            if isinstance(topic_analysis, (dict, list)):
                print(json.dumps(topic_analysis, indent=2))
            else:
                print(topic_analysis)
                
            print("\n[QUESTIONER_DATA FULL CONTENT]:")
            if isinstance(questioner_data, (dict, list)):
                print(json.dumps(questioner_data, indent=2))
            else:
                print(questioner_data)
            
            print("="*80)
            
            # Pre-process topic_analysis to ensure all candidate codes are properly represented
            all_candidate_codes = self._extract_all_candidate_codes(topic_analysis)
            self.logger.info(f"Extracted {len(all_candidate_codes)} candidate codes for analysis")
            
            # Format the prompt with all candidate codes clearly presented
            formatted_prompt = self.format_prompt(scenario, topic_analysis, questioner_data)
            
            # Generate the response from the LLM
            response = generate_response(formatted_prompt)
            
            # Parse the response
            result = self.parse_response(response)
            
            # Validate the results against candidate codes
            validated_result = self._validate_results(result, all_candidate_codes)
            
            self.logger.info(f"Dental analysis completed for scenario")
            self.logger.info(f"Extracted codes: {validated_result['codes']}")
            self.logger.info(f"Extracted rejected codes: {validated_result['rejected_codes']}")
            self.logger.info(f"Explanation length: {len(validated_result['explanation'])}")
            
            return validated_result
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            self.logger.error(f"Error in process: {str(e)}")
            self.logger.error(f"STACK TRACE: {error_details}")
            return {
                "error": str(e),
                "codes": [],
                "rejected_codes": [],
                "explanation": f"Error occurred: {str(e)}",
                "type": "error",
                "data_source": "error"
            }
            
    def _extract_all_candidate_codes(self, topic_analysis: Any) -> list:
        """Extract all candidate CDT codes (Dxxxx format) from the topic analysis data."""
        if topic_analysis is None:
            return []
            
        all_codes = set()
        
        if isinstance(topic_analysis, dict):
            # Extract codes from subtopic_data first if present
            if "subtopic_data" in topic_analysis:
                 # Assuming subtopic_data itself might be a dict or a string representation
                 subtopic_data_content = topic_analysis["subtopic_data"]
                 if isinstance(subtopic_data_content, dict):
                     for subtopic_key, codes_list in subtopic_data_content.items():
                         if isinstance(codes_list, list):
                            for code_entry in codes_list:
                                if isinstance(code_entry, dict) and "code" in code_entry:
                                     # Use regex to find the Dxxxx pattern within the code field
                                    code_match = re.search(r'(D\d{4})', str(code_entry["code"]))
                                    if code_match:
                                        all_codes.add(code_match.group(1))
                 elif isinstance(subtopic_data_content, str):
                     # Extract from string representation if it's not a dict
                     codes_from_string = self._extract_codes_from_subtopic_data_string(subtopic_data_content)
                     all_codes.update(codes_from_string)
            
            # Extract codes from other parts of topic_analysis
            for code_range, topic_data in topic_analysis.items():
                 # Skip the subtopic_data key itself if it was processed above
                 if code_range == "subtopic_data":
                     continue
                     
                 result = topic_data.get("result", "")
                 if isinstance(result, str):
                     # Use regex to find all Dxxxx codes directly within the result string
                     import re
                     code_pattern = r'(D\d{4})'
                     codes_in_result = re.findall(code_pattern, result)
                     all_codes.update(codes_in_result)
                     
                     # Additionally, specifically look for codes within quoted "code": fields
                     quoted_code_pattern = r'"code":\s*"(D\d{4})"'
                     quoted_codes = re.findall(quoted_code_pattern, result)
                     all_codes.update(quoted_codes)

        # Ensure codes extracted from different places are unified
        return sorted(list(all_codes))
        
    def _extract_codes_from_subtopic_data_string(self, data_str: str) -> set:
        """Extract Dxxxx codes from a string representation of subtopic data."""
        codes = set()
        import re
        try:
            # Look for codes in the format "code": "Dxxxx"
            quoted_code_pattern = r'"code":\s*"(D\d{4})"'
            quoted_matches = re.findall(quoted_code_pattern, data_str)
            codes.update(quoted_matches)
            
            # Look for codes directly like Dxxxx
            direct_code_pattern = r'(D\d{4})'
            direct_matches = re.findall(direct_code_pattern, data_str)
            codes.update(direct_matches)

            # Attempt to handle the malformed examples specifically if needed,
            # but focusing on valid Dxxxx should be more robust.
            # For example, explicitly ignore lines containing "Overall" or similar keywords
            # if they interfere.
            
        except Exception as e:
            self.logger.error(f"Error extracting codes from subtopic_data string: {str(e)}")
        
        return codes

    def _validate_results(self, result: Dict[str, Any], candidate_codes: list) -> Dict[str, Any]:
        """Validate the results against the candidate codes"""
        # If no candidate codes were found, return the original result
        if not candidate_codes:
            return result
            
        validated_codes = []
        validated_rejected = []
        
        # Process accepted codes
        for code in result["codes"]:
            # Clean the code and ensure it's in the right format
            clean_code = code.strip()
            
            # Remove any description after the code
            if " " in clean_code:
                clean_code = clean_code.split(" ")[0].strip()
                
            # Validate that it's a properly formatted CDT code
            import re
            if re.match(r'D\d{4}', clean_code):
                validated_codes.append(clean_code)
        
        # Process rejected codes
        for code in result["rejected_codes"]:
            # Clean and validate
            clean_code = code.strip()
            
            # Remove any description
            if " " in clean_code:
                clean_code = clean_code.split(" ")[0].strip()
                
            # Validate format
            import re
            if re.match(r'D\d{4}', clean_code) and clean_code.lower() != "n/a":
                validated_rejected.append(clean_code)
        
        # Check for special case where N/A is included
        if len(result["rejected_codes"]) == 1 and (
            result["rejected_codes"][0].lower() == "n/a" or 
            result["rejected_codes"][0].lower() == "none"
        ):
            # Generate the correct rejected codes list
            # This means no codes were explicitly rejected, so all codes not accepted should be rejected
            all_rejected = [code for code in candidate_codes if code not in validated_codes]
            validated_rejected = all_rejected
        
        return {
            "codes": validated_codes,
            "rejected_codes": validated_rejected,
            "explanation": result["explanation"]
        }

    @property
    def current_settings(self) -> Dict[str, Any]:
        """Get current model settings"""
        return {
            "model": self.service.model,
            "temperature": self.service.temperature
        }

class InspectorCLI:
    """Command Line Interface for the DentalInspector"""
    
    def __init__(self):
        self.inspector = DentalInspector()

    def print_settings(self):
        """Print current model settings"""
        settings = self.inspector.current_settings
        print(f"Using model: {settings['model']} with temperature: {settings['temperature']}")

    def print_results(self, result: Dict[str, Any]):
        """Print inspection results in a formatted way"""
        print("\n=== INSPECTION RESULTS ===")
        print("\nAccepted Codes:")
        for code in result["codes"]:
            print(f"- {code}")
        
        print("\nRejected Codes:")
        for code in result["rejected_codes"]:
            print(f"- {code}")
        
        print("\nExplanation:")
        print(result["explanation"])

    def run(self):
        """Run the CLI interface"""
        self.print_settings()
        scenario = input("Enter dental scenario: ")
        topic_analysis = input("Enter topic analysis (or press Enter to skip): ") or None
        questioner_data = input("Enter questioner data (or press Enter to skip): ") or None
        
        result = self.inspector.process(scenario, topic_analysis, questioner_data)
        self.print_results(result)

def main():
    """Main entry point for the script"""
    cli = InspectorCLI()
    cli.run()

if __name__ == "__main__":
    main()





