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

class ICDInspector:
    """Class to handle ICD code inspection with configurable prompts and settings"""
    
    PROMPT_TEMPLATE = """
You are a highly experienced medical coding expert with over 15 years of expertise in ICD-10-CM codes for dental scenarios. 
Your task is to analyze the given dental scenario and provide final ICD-10-CM code recommendations.

Scenario:
{scenario}

Topic Analysis Results:
{topic_analysis}

Additional Information from Questions (if any):
{questioner_data}

{user_rules}

Please provide a thorough analysis of this scenario by:
1. Only select the suitable ICD-10-CM code(s) from the suggested answers in the topic analysis
2. Be very specific, your answer is final so be careful, no errors can be tolerated
3. Don't assume anything that is not explicitly stated in the scenario
4. If a code has doubt or mentions information is not specifically stated, do not include that code
5. Choose the best between mutually exclusive codes, don't bill for the same condition twice
6. Consider any additional information provided through the question-answer process

IMPORTANT: You must format your response exactly as follows:

EXPLANATION: [provide a detailed explanation for why each code was selected or rejected. Include specific reasoning for each code mentioned in the topic analysis and explain the clinical significance.]

CODES: [comma-separated list of ICD-10-CM codes, with no square brackets around individual codes]

REJECTED CODES: [comma-separated list of ICD-10-CM codes that were considered but rejected, with no square brackets around individual codes. Only list codes that were analyzed in the topic analysis and are explicitly contradicted by the scenario.]

For example:
EXPLANATION: K05.1 (Chronic gingivitis) is appropriate as the scenario describes inflammation of the gums that has persisted for several months. Z91.89 (Other specified personal risk factors) is included to document the patient's tobacco use which is significant for their periodontal condition. K05.2 was rejected because while there is gum disease, there is no evidence of destruction of the supporting structures required for periodontitis diagnosis.
CODES: K05.1, Z91.89
REJECTED CODES: K05.2
"""

    def __init__(self, model: str = OPENROUTER_MODEL, temperature: float = DEFAULT_TEMP):
        """Initialize the inspector with model and temperature settings"""
        self.service = get_service()
        self.configure(model, temperature)
        self.logger = self._setup_logging()
        self.db = MedicalCodingDB()

    def _setup_logging(self) -> logging.Logger:
        """Configure logging for the ICD inspector module"""
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

    def _format_prompt(self, scenario: str, topic_analysis: Any, questioner_data: Any = None, user_rules: Optional[str] = None) -> str:
        """Format the prompt template with all inputs including user rules"""
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
        """Format topic analysis data into string with candidate codes emphasized"""
        if topic_analysis is None:
            return "No ICD data analysis data available in DB"
        
        if isinstance(topic_analysis, str):
            return topic_analysis
        
        if isinstance(topic_analysis, dict):
            formatted_topics = []
            all_candidate_codes = self._extract_all_candidate_codes(topic_analysis)
            
            if all_candidate_codes:
                formatted_topics.append(f"ALL CANDIDATE CODES FOR REVIEW: {', '.join(sorted(set(all_candidate_codes)))}\n")
            
            for category_num, topic_data in topic_analysis.items():
                if not isinstance(topic_data, dict):
                    formatted_topics.append(f"Category {category_num}: {str(topic_data)}")
                    continue
                    
                topic_name = topic_data.get("name", "Unknown")
                topic_result = topic_data.get("result", "No result")
                parsed_result = topic_data.get("parsed_result", {})
                
                parsed_lines = []
                if parsed_result and isinstance(parsed_result, dict):
                    for key in ["code", "explanation", "doubt"]:
                        if key in parsed_result and parsed_result[key]:
                            parsed_lines.append(f"{key.upper()}: {parsed_result[key]}")
                
                topic_info = [
                    f"Category {category_num}: {topic_name}",
                    "PARSED RESULT:" if parsed_lines else "",
                    *parsed_lines,
                    "RAW RESULT:",
                    topic_result
                ]
                formatted_topics.append("\n".join(filter(None, topic_info)))
            
            return "\n\n".join(formatted_topics)
        
        return str(topic_analysis)

    def _format_questioner_data(self, questioner_data: Any) -> str:
        """Format questioner data into string"""
        if questioner_data is None:
            return "No additional information provided."
        
        if isinstance(questioner_data, str):
            return questioner_data
        
        if isinstance(questioner_data, dict):
            if questioner_data.get("has_questions", False) and questioner_data.get("has_answers", False):
                qa_pairs = []
                answers = questioner_data.get("answers", {})
                
                for q_type in ["cdt_questions", "icd_questions"]:
                    prefix = q_type.split("_")[0].upper()
                    questions = questioner_data.get(q_type, {}).get("questions", [])
                    for question in questions:
                        answer = answers.get(question, "No answer provided")
                        qa_pairs.append(f"{prefix} Q: {question}\nA: {answer}")
                
                return "\n".join(qa_pairs) if qa_pairs else "Questions were asked but no answers were provided."
            elif questioner_data.get("has_questions", False):
                return "Questions were identified but not yet answered."
            return "No additional questions were needed."
        
        return str(questioner_data)

    def _parse_response(self, response: str) -> Dict[str, Any]:
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
        
        cleaned_codes = self._clean_codes(codes_line)
        cleaned_rejected_codes = self._clean_codes(rejected_codes_line)
        
        self.logger.info(f"Extracted ICD codes: {cleaned_codes}")
        self.logger.info(f"Extracted rejected ICD codes: {cleaned_rejected_codes}")
        self.logger.info(f"Extracted explanation: {explanation_line}")
        
        return {
            "codes": cleaned_codes,
            "rejected_codes": cleaned_rejected_codes,
            "explanation": explanation_line,
            "raw_response": raw_response
        }

    def _clean_codes(self, codes_line: str) -> List[str]:
        """Clean and format codes from response"""
        cleaned_codes = []
        if codes_line:
            codes_line = codes_line.strip('[]')
            for code in codes_line.split(','):
                clean_code = code.strip().strip('[]')
                if clean_code and clean_code.lower() != 'none':
                    cleaned_codes.append(clean_code)
        return cleaned_codes

    def _extract_all_candidate_codes(self, topic_analysis: Any) -> List[str]:
        """Extract all candidate ICD-10 codes from the topic analysis data"""
        if topic_analysis is None:
            return []
            
        all_codes = set()
        
        if isinstance(topic_analysis, dict):
            for key, topic_data in topic_analysis.items():
                result = topic_data.get("result", "") if isinstance(topic_data, dict) else str(topic_data)
                if isinstance(result, str):
                    code_pattern = r'[A-Z]\d{2}(?:\.\d)?'  # Basic ICD-10 pattern (e.g., K05.1, R52.9)
                    codes = re.findall(code_pattern, result)
                    all_codes.update(codes)
                    
                    quoted_code_pattern = r'"code":\s*"([A-Z]\d{2}(?:\.\d)?)"'
                    quoted_codes = re.findall(quoted_code_pattern, result)
                    all_codes.update(quoted_codes)
        
        return sorted(list(all_codes))

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
            if re.match(r'[A-Z]\d{2}(?:\.\d)?', clean_code):
                validated_codes.append(clean_code)
        
        for code in result["rejected_codes"]:
            clean_code = code.strip()
            if " " in clean_code:
                clean_code = clean_code.split(" ")[0].strip()
            if re.match(r'[A-Z]\d{2}(?:\.\d)?', clean_code) and clean_code.lower() != "n/a":
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

    def process(self, scenario: str, topic_analysis: Any = None, questioner_data: Any = None, user_id: Optional[str] = None) -> Dict[str, Any]:
        """Process a scenario and return ICD inspection results"""
        try:
            all_candidate_codes = self._extract_all_candidate_codes(topic_analysis)
            self.logger.info(f"Extracted {len(all_candidate_codes)} candidate ICD codes for analysis")
            
            user_rules = None
            if user_id:
                user_rules = self.db.get_user_rules(user_id)
                self.logger.info(f"Retrieved user rules for user ID: {user_id}" if user_rules else "No user rules found")
            
            formatted_prompt = self._format_prompt(
                scenario=scenario,
                topic_analysis=topic_analysis,
                questioner_data=questioner_data,
                user_rules=user_rules
            )
            
            response = generate_response(formatted_prompt)
            result = self._parse_response(response)
            validated_result = self._validate_results(result, all_candidate_codes)
            
            self.logger.info(f"ICD analysis completed for scenario")
            self.logger.info(f"Extracted codes: {validated_result['codes']}")
            self.logger.info(f"Extracted rejected codes: {validated_result['rejected_codes']}")
            self.logger.info(f"Explanation length: {len(validated_result['explanation'])}")
            
            return validated_result
            
        except Exception as e:
            import traceback
            error_traceback = traceback.format_exc()
            self.logger.error(f"Error in process: {str(e)}")
            self.logger.error(f"Error traceback: {error_traceback}")
            return {
                "error": str(e),
                "codes": [],
                "rejected_codes": [],
                "explanation": f"Error occurred: {str(e)}",
                "raw_response": f"Error occurred, no raw response from LLM: {str(e)}",
                "type": "error",
                "data_source": "error"
            }

    @property
    def current_settings(self) -> Dict[str, Any]:
        """Get current model settings"""
        return {
            "model": self.service.model,
            "temperature": self.service.temperature
        }

class ICDInspectorCLI:
    """Command Line Interface for the ICDInspector"""
    
    def __init__(self):
        self.inspector = ICDInspector()

    def print_settings(self):
        """Print current model settings"""
        settings = self.inspector.current_settings
        print(f"Using model: {settings['model']} with temperature: {settings['temperature']}")

    def print_results(self, result: Dict[str, Any]):
        """Print inspection results in a formatted way"""
        if "error" in result:
            print(f"\nError: {result['error']}")
            return

        print("\n=== ICD INSPECTION RESULTS ===")
        print("\nCodes:")
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
    cli = ICDInspectorCLI()
    cli.run()

if __name__ == "__main__":
    main()