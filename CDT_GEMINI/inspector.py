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

11) Coding Rules:
    - Consider standard bundling rules but don't be overly strict
    - Assume medical necessity for standard procedures
    - Consider emergency/post-op status if implied by context
    - You MUST include ALL appropriate codes that appeared in the topic analysis and reject all inappropriate codes

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
        """Extract all candidate codes from the topic analysis data"""
        if topic_analysis is None:
            return []
            
        all_codes = set()
        
        if isinstance(topic_analysis, dict):
            # Extract codes from subtopics
            for code_range, topic_data in topic_analysis.items():
                result = topic_data.get("result", "")
                
                # Special handling for subtopic_data structure
                if "subtopic_data" in str(result):
                    subtopic_codes = self._extract_codes_from_subtopic_data(result)
                    all_codes.update(subtopic_codes)
                    continue
                
                # Check if it's a string representation of a list
                if isinstance(result, str):
                    # Use regex to find all CDT codes (D followed by 4 digits)
                    import re
                    code_pattern = r'D\d{4}'
                    codes = re.findall(code_pattern, result)
                    all_codes.update(codes)
                    
                    # Also look for codes with name
                    code_with_name_pattern = r'"code":\s*"([^"]+)"'
                    code_matches = re.findall(code_with_name_pattern, result)
                    
                    for code in code_matches:
                        # Clean and filter valid codes
                        if code and code.strip() and code.strip().lower() != 'none' and code.strip().startswith('D'):
                            all_codes.add(code.strip())
                
                # If it's a more complex structure serialized as string
                if "code" in result or "CODE:" in result:
                    # Try to extract codes from a different format
                    code_lines = result.split('\n')
                    for line in code_lines:
                        if "code" in line.lower() or "CODE:" in line:
                            parts = line.split(':', 1)
                            if len(parts) > 1:
                                code_part = parts[1].strip()
                                # Clean the code
                                import re
                                code_match = re.search(r'D\d{4}', code_part)
                                if code_match:
                                    all_codes.add(code_match.group())
        
        return sorted(list(all_codes))
        
    def _extract_codes_from_subtopic_data(self, data_str: str) -> set:
        """Extract codes specifically from the subtopic_data structure"""
        codes = set()
        
        try:
            # Use regex to find all code entries in the format: "code": "D1234"
            import re
            code_pattern = r'"code":\s*"([^"]+)"'
            code_matches = re.findall(code_pattern, data_str)
            
            for code in code_matches:
                # Clean and filter valid codes
                clean_code = code.strip()
                if clean_code and clean_code.lower() != 'none' and clean_code != 'Unknown':
                    # For codes like "D0160", extract just the CDT code
                    if clean_code.startswith('D'):
                        # If the code has a description (like "D0160 - Description"), extract just the code
                        if " - " in clean_code:
                            clean_code = clean_code.split(" - ")[0].strip()
                        codes.add(clean_code)
            
            # Also look for other formats like "D1234" directly in the text
            direct_code_pattern = r'D\d{4}'
            direct_codes = re.findall(direct_code_pattern, data_str)
            codes.update(direct_codes)
            
        except Exception as e:
            self.logger.error(f"Error extracting codes from subtopic_data: {str(e)}")
        
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





