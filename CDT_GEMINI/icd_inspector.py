import os
import logging
from dotenv import load_dotenv
from llm_services import generate_response, get_service, set_model, set_temperature
from typing import Dict, Any, Optional
from llm_services import OPENROUTER_MODEL, DEFAULT_TEMP
from database import MedicalCodingDB

# Load environment variables
load_dotenv()

# Set a specific model for this file (optional)
# set_model_for_file("gemini-2.5-pro-exp-03-25-thinking-exp-01-21")

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

CODES: [comma-separated list of ICD-10-CM codes, with no square brackets around individual codes]

EXPLANATION: [provide a detailed explanation for why each code was selected or rejected. Include specific reasoning for each code mentioned in the topic analysis and explain the clinical significance.]

For example:
CODES: K05.1, Z91.89

EXPLANATION: K05.1 (Chronic gingivitis) is appropriate as the scenario describes inflammation of the gums that has persisted for several months. Z91.89 (Other specified personal risk factors) is included to document the patient's tobacco use which is significant for their periodontal condition. K05.2 was rejected because while there is gum disease, there is no evidence of destruction of the supporting structures required for periodontitis diagnosis.
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

    def _format_topic_analysis(self, topic_analysis: Any) -> str:
        """Format topic analysis data into string"""
        if topic_analysis is None:
            return "No ICD data analysis data available in DB"
        
        # Handle the case when topic_analysis is a string
        if isinstance(topic_analysis, str):
            return topic_analysis
        
        if isinstance(topic_analysis, dict):
            formatted_topics = []
            for category_num, topic_data in topic_analysis.items():
                # Make sure topic_data is a dictionary before using get()
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
        
        # As a fallback, convert to string
        return str(topic_analysis)

    def _format_questioner_data(self, questioner_data: Any) -> str:
        """Format questioner data into string"""
        if questioner_data is None:
            return "No additional information provided."
        
        # Handle the case when questioner_data is already a string
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
        
        # As a fallback for any other type
        return str(questioner_data)

    def _parse_response(self, response: str) -> Dict[str, Any]:
        """Parse the LLM response into structured format"""
        codes_line = ""
        explanation_line = ""
        lines = response.strip().split('\n')
        in_explanation = False
        
        for line in lines:
            line = line.strip()
            if line.upper().startswith("CODES:"):
                codes_line = line.split(":", 1)[1].strip()
            elif line.upper().startswith("EXPLANATION:"):
                in_explanation = True
                explanation_line = line.split(":", 1)[1].strip()
            elif in_explanation and line:
                explanation_line += " " + line
        
        cleaned_codes = self._clean_codes(codes_line)
        explanation = self._extract_explanation(explanation_line, response, codes_line)
        
        self.logger.info(f"Extracted ICD codes: {cleaned_codes}")
        self.logger.info(f"Extracted explanation: {explanation}")
        
        return {
            "codes": cleaned_codes,
            "explanation": explanation
        }

    def _clean_codes(self, codes_line: str) -> list:
        """Clean and format codes from response"""
        cleaned_codes = []
        if codes_line:
            codes_line = codes_line.strip('[]')
            for code in codes_line.split(','):
                clean_code = code.strip().strip('[]')
                if clean_code and clean_code.lower() != 'none':
                    cleaned_codes.append(clean_code)
        return cleaned_codes

    def _extract_explanation(self, explanation_line: str, full_text: str, codes_line: str) -> str:
        """Extract explanation from response using multiple methods"""
        if explanation_line:
            return explanation_line
        
        # Try to find explicit explanation section
        started = False
        collected = []
        for line in full_text.split('\n'):
            if any(line.upper().startswith(prefix) for prefix in ["EXPLANATION:", "REASONING:", "RATIONALE:"]):
                started = True
                collected.append(line.split(":", 1)[1].strip())
            elif started and line.strip():
                collected.append(line.strip())
            elif started and not line.strip() and collected:
                break
        
        if collected:
            return " ".join(collected)
        
        # Use everything after codes as explanation
        if codes_line:
            codes_index = full_text.find("CODES:")
            if codes_index > -1:
                remainder = full_text[codes_index:].split('\n', 1)
                if len(remainder) > 1:
                    rest = remainder[1].strip()
                    if "EXPLANATION:" in rest.upper():
                        return rest.split("EXPLANATION:", 1)[1].strip()
                    return rest
        
        return ""

    def process(self, scenario: str, topic_analysis: Any = None, questioner_data: Any = None, user_id: Optional[str] = None) -> Dict[str, Any]:
        """Process a scenario and return ICD inspection results"""
        try:
            # Log input types for debugging
            self.logger.info(f"Processing scenario with topic_analysis type: {type(topic_analysis)}")
            self.logger.info(f"Questioner data type: {type(questioner_data)}")
            
            # Get user rules if user_id is provided
            user_rules = None
            if user_id:
                user_rules = self.db.get_user_rules(user_id)
                self.logger.info(f"Retrieved user rules for user ID: {user_id}" if user_rules else "No user rules found")
            
            # Pre-process topic_analysis if it's a string to convert to a more useful format
            if isinstance(topic_analysis, str):
                self.logger.info("Received topic_analysis as string, using as-is")
            
            formatted_prompt = self._format_prompt(
                scenario=scenario,
                topic_analysis=topic_analysis,
                questioner_data=questioner_data,
                user_rules=user_rules
            )
            
            response = generate_response(formatted_prompt)
            result = self._parse_response(response)
            
            self.logger.info("ICD analysis completed for scenario")
            return result
            
        except Exception as e:
            import traceback
            error_traceback = traceback.format_exc()
            self.logger.error(f"Error in process: {str(e)}")
            self.logger.error(f"Error traceback: {error_traceback}")
            self.logger.error(f"Input topic_analysis type: {type(topic_analysis)}")
            
            # Include more detailed error information
            return {
                "error": str(e),
                "codes": [],
                "explanation": f"Error occurred: {str(e)}",
                "type": "error",
                "data_source": "error",
                "traceback": error_traceback[:500] if error_traceback else None
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