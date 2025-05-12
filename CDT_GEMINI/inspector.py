import os
import logging
import re
from dotenv import load_dotenv
from llm_services import generate_response, get_service, set_model, set_temperature
from typing import Dict, Any, Optional, List
from llm_services import OPENROUTER_MODEL, DEFAULT_TEMP
from database import MedicalCodingDB

# Load environment variables
load_dotenv()

class DentalInspector:
    """Class to handle CDT code inspection with configurable prompts and settings"""
    
    PROMPT_TEMPLATE = """
You are the final code selector ("Inspector") with extensive expertise in dental coding. Your task is to perform a thorough analysis of the provided scenario along with the candidate CDT code outputs—including all explanations and doubts—from previous subtopics. Your final output must include only the CDT code(s) that are justified by the scenario, with minimal assumptions.

Scenario:
{scenario}

Topic Analysis Results:
{topic_analysis}

Additional Information from Questions (if any):
{questioner_data}

{user_rules}

Instructions:

1) Carefully read the complete clinical scenario provided.
2) Review ALL candidate CDT codes suggested by previous subtopics along with their explanations and any doubts raised. Every code that appears in the Topic Analysis Results is a candidate for selection or rejection.
3) Use ONLY Provided Codes: Ensure your final `CODES:` and `REJECTED CODES:` lists contain ONLY codes explicitly presented as candidates in the 'Topic Analysis Results' section. Do not introduce codes not mentioned there, but *critically evaluate* if the provided candidate codes truly match the scenario based on specificity and accuracy.
4) Evaluate EVERY Code: You must evaluate each specific code (like D0160, D7210, etc.) in the topic analysis results and either select it or reject it.
5) Reasonable Assumptions: You may make basic clinical assumptions that are standard in dental practice, but avoid making significant assumptions about unstated procedures.
6) Justification: Select codes that are reasonably supported by the scenario and represent the most accurate description of the service performed. If a code has minor doubts but is likely correct and the most specific description, include it.
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
        self.db = MedicalCodingDB()

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

    def format_prompt(self, scenario: str, topic_analysis: Any, questioner_data: Any = None, user_rules: Optional[str] = None) -> str:
        """Format the prompt template with the given inputs"""
        topic_analysis_str = self._format_topic_analysis(topic_analysis)
        questioner_data_str = self._format_questioner_data(questioner_data)
        rules_section = f"User-Specific Rules:\n{user_rules}" if user_rules else ""
        
        return self.PROMPT_TEMPLATE.format(
            scenario=scenario,
            topic_analysis=topic_analysis_str,
            questioner_data=questioner_data_str,
            user_rules=rules_section
        )

    def _format_topic_analysis(self, topic_analysis: Any) -> str:
        """Format topic analysis data with clear emphasis on candidate codes"""
        if topic_analysis is None:
            return "No CDT data analysis data available in DB"
        
        if isinstance(topic_analysis, dict):
            formatted_topics = []
            all_candidate_codes = []
            
            for code_range, topic_data in topic_analysis.items():
                result = topic_data.get("result", "")
                if isinstance(result, str) and "[" in result:
                    try:
                        code_pattern = r'D\d{4}'  # Pattern to match D followed by 4 digits
                        codes = re.findall(code_pattern, result)
                        all_candidate_codes.extend(codes)
                    except:
                        pass
            
            for code_range, topic_data in topic_analysis.items():
                topic_name = topic_data.get("name", "Unknown")
                topic_result = topic_data.get("result", "No result")
                formatted_topics.append(f"{topic_name} ({code_range}):\n{topic_result}")
            
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
        raw_response = response
        
        lines = response.strip().split('\n')
        current_section = None
        explanation_parts = []
        codes_parts = []
        rejected_codes_parts = []

        for line in lines:
            line_upper = line.upper().strip()
            if line_upper.startswith("EXPLANATION:"):
                current_section = "explanation"
                explanation_parts.append(line.split(":", 1)[1].strip() if ":" in line else "")
                continue
            elif line_upper.startswith("CODES:"):
                current_section = "codes"
                codes_parts.append(line.split(":", 1)[1].strip() if ":" in line else "")
                continue
            elif line_upper.startswith("REJECTED CODES:"):
                current_section = "rejected_codes"
                rejected_codes_parts.append(line.split(":", 1)[1].strip() if ":" in line else "")
                continue
            
            if current_section == "explanation":
                explanation_parts.append(line.strip())
            elif current_section == "codes":
                codes_parts.append(line.strip())
            elif current_section == "rejected_codes":
                rejected_codes_parts.append(line.strip())

        explanation_line = " ".join(explanation_parts).strip()
        codes_line = " ".join(codes_parts).strip()
        rejected_codes_line = " ".join(rejected_codes_parts).strip()
        
        if not codes_line:
            match = re.search(r"((?:D\d{4}\s*,\s*)*D\d{4}(?:\s+none)?)$", explanation_line, re.IGNORECASE)
            if match:
                potential_codes_part = match.group(1).strip()
                if len(explanation_line) - len(potential_codes_part) > 20:
                    codes_line = potential_codes_part
                    explanation_line = explanation_line[:-len(potential_codes_part)].strip()
                    self.logger.info(f"Fallback: Extracted codes from explanation: {codes_line}")

        cleaned_codes = self._clean_codes(codes_line)
        rejected_codes = self._clean_codes(rejected_codes_line)
        
        return {
            "codes": cleaned_codes,
            "rejected_codes": rejected_codes,
            "explanation": explanation_line,
            "raw_response": raw_response
        }

    def _clean_codes(self, codes_line: str) -> List[str]:
        """Clean and format codes from response"""
        cleaned = []
        if codes_line:
            codes_line = codes_line.strip('[]')
            for code in codes_line.split(','):
                clean_code = code.strip().strip('[]')
                if clean_code and clean_code.lower() != 'none' and '*' not in clean_code:
                    cleaned.append(clean_code)
        return cleaned

    def process(self, scenario: str, topic_analysis: Any = None, questioner_data: Any = None, user_id: Optional[str] = None) -> Dict[str, Any]:
        """Process a dental scenario and return inspection results"""
        try:
            all_candidate_codes = self._extract_all_candidate_codes(topic_analysis)
            self.logger.info(f"Extracted {len(all_candidate_codes)} candidate CDT codes for analysis")
            
            user_rules = None
            if user_id:
                user_rules = self.db.get_user_rules(user_id)
                self.logger.info(f"Retrieved user rules for user ID: {user_id}" if user_rules else "No user rules found")
            
            formatted_prompt = self.format_prompt(
                scenario=scenario, 
                topic_analysis=topic_analysis, 
                questioner_data=questioner_data,
                user_rules=user_rules
            )
            
            response = generate_response(formatted_prompt)
            result = self.parse_response(response)
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
                "raw_response": f"Error occurred, no raw response from LLM: {str(e)}",
                "type": "error",
                "data_source": "error"
            }

    def _extract_all_candidate_codes(self, topic_analysis: Any) -> List[str]:
        """Extract all candidate CDT codes (Dxxxx format) from the topic analysis data"""
        if topic_analysis is None:
            return []
            
        all_codes = set()
        
        if isinstance(topic_analysis, dict):
            if "subtopic_data" in topic_analysis:
                subtopic_data_content = topic_analysis["subtopic_data"]
                if isinstance(subtopic_data_content, dict):
                    for subtopic_key, codes_list in subtopic_data_content.items():
                        if isinstance(codes_list, list):
                            for code_entry in codes_list:
                                if isinstance(code_entry, dict) and "code" in code_entry:
                                    code_match = re.search(r'(D\d{4})', str(code_entry["code"]))
                                    if code_match:
                                        all_codes.add(code_match.group(1))
                elif isinstance(subtopic_data_content, str):
                    codes_from_string = self._extract_codes_from_subtopic_data_string(subtopic_data_content)
                    all_codes.update(codes_from_string)
            
            for code_range, topic_data in topic_analysis.items():
                if code_range == "subtopic_data":
                    continue
                result = topic_data.get("result", "")
                if isinstance(result, str):
                    code_pattern = r'(D\d{4})'
                    codes_in_result = re.findall(code_pattern, result)
                    all_codes.update(codes_in_result)
                    quoted_code_pattern = r'"code":\s*"(D\d{4})"'
                    quoted_codes = re.findall(quoted_code_pattern, result)
                    all_codes.update(quoted_codes)

        return sorted(list(all_codes))
        
    def _extract_codes_from_subtopic_data_string(self, data_str: str) -> set:
        """Extract Dxxxx codes from a string representation of subtopic data"""
        codes = set()
        try:
            quoted_code_pattern = r'"code":\s*"(D\d{4})"'
            quoted_matches = re.findall(quoted_code_pattern, data_str)
            codes.update(quoted_matches)
            
            direct_code_pattern = r'(D\d{4})'
            direct_matches = re.findall(direct_code_pattern, data_str)
            codes.update(direct_matches)
            
        except Exception as e:
            self.logger.error(f"Error extracting codes from subtopic_data string: {str(e)}")
        
        return codes

    def _validate_results(self, result: Dict[str, Any], candidate_codes: List[str]) -> Dict[str, Any]:
        """Validate the results against the candidate codes"""
        if not candidate_codes:
            return result
            
        validated_codes = []
        validated_rejected = []
        
        for code in result["codes"]:
            clean_code = code.strip()
            if " " in clean_code:
                clean_code = clean_code.split(" ")[0].strip()
            if re.match(r'D\d{4}', clean_code):
                validated_codes.append(clean_code)
        
        for code in result["rejected_codes"]:
            clean_code = code.strip()
            if " " in clean_code:
                clean_code = clean_code.split(" ")[0].strip()
            if re.match(r'D\d{4}', clean_code) and clean_code.lower() != "n/a":
                validated_rejected.append(clean_code)
        
        if len(result["rejected_codes"]) == 1 and (
            result["rejected_codes"][0].lower() in ["n/a", "none"]
        ):
            all_rejected = [code for code in candidate_codes if code not in validated_codes]
            validated_rejected = all_rejected
        
        return {
            "codes": validated_codes,
            "rejected_codes": validated_rejected,
            "explanation": result["explanation"],
            "raw_response": result["raw_response"]
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
        self.logger.info(f"Inspector settings - Model: {settings['model']}, Temp: {settings['temperature']}")

    def print_results(self, result: Dict[str, Any]):
        """Print inspection results in a formatted way"""
        if "error" in result:
            self.logger.error(f"Inspection Error: {result['error']}")
            return

        self.logger.info(f"Inspection Accepted Codes: {result['codes']}")
        self.logger.info(f"Inspection Rejected Codes: {result['rejected_codes']}")
        self.logger.info(f"Inspection Explanation: {result['explanation']}")

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