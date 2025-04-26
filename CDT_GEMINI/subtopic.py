import json
import re
from langchain.prompts import PromptTemplate
import copy

class DentalCodeManager:
    def __init__(self):
        self.name = ""
        self.strict = False
        self.schema = {
            "explanation": "",
            "doubt": "",
            "code_range": "",
            "activated_subtopics": "",
            "specific_codes": []
        }
        # Placeholder for llm_service (commented out since get_service is not provided)
        # self.llm_service = get_service()
        self.parser_prompt = PromptTemplate(
            template="""You are a dental coding expert. Parse the following raw output into a structured format.
Extract all CDT codes (D####), explanations, and any doubts.
If multiple codes are found, include all of them.

Raw Output:
{raw_output}

IMPORTANT: You must respond with ONLY a valid JSON object in exactly this format (no other text):
{{
    "specific_codes": ["D####"],
    "explanation": "clear explanation of why these codes",
    "doubt": "any doubts or None"
}}

Rules:
1. specific_codes must be an array, even for single codes
2. If no codes found, use empty array []
3. Never include line breaks in explanation or doubt
4. Do not include any text outside the JSON object
5. Always include all three fields
""",
            input_variables=["raw_output"]
        )

    def update_values(self, name, strict, explanation, doubt, code_range, activated_subtopics, specific_codes):
        self.name = name
        self.strict = strict
        self.schema["explanation"] = explanation
        self.schema["doubt"] = doubt
        self.schema["code_range"] = code_range
        self.schema["activated_subtopics"] = activated_subtopics
        self.schema["specific_codes"] = specific_codes

    def parse_llm_output(self, raw_output: str) -> list:
        try:
            # First try to parse as JSON if it's already in JSON format
            try:
                if isinstance(raw_output, str):
                    pre_parsed = json.loads(raw_output)
                else:
                    pre_parsed = raw_output
                
                # If it's from diagnostic services, extract codes from topic_result
                if isinstance(pre_parsed, dict) and "topic_result" in pre_parsed:
                    codes = []
                    explanation = []
                    for result in pre_parsed["topic_result"].values():
                        if isinstance(result, dict):
                            if "codes" in result:
                                codes.extend(code["code"] for code in result["codes"] if isinstance(code, dict) and "code" in code)
                            if "explanation" in result:
                                explanation.append(result["explanation"])
                    
                    parsed_data = {
                        "specific_codes": codes,
                        "explanation": " ".join(explanation) if explanation else "Codes extracted from diagnostic services",
                        "doubt": "None"
                    }
                    
                    self.update_values(
                        name=self.name or "Dental Code Analysis",
                        strict=True,
                        explanation=parsed_data["explanation"],
                        doubt=parsed_data["doubt"],
                        code_range=self.schema["code_range"],
                        activated_subtopics=self.schema["activated_subtopics"],
                        specific_codes=parsed_data["specific_codes"]
                    )
                    return [parsed_data]  # Return as a list for consistency

            except (json.JSONDecodeError, AttributeError):
                pass

            # Regex-based parsing for raw_output
            sections = re.split(r'(?=EXPLANATION:)', raw_output.strip())
            parsed_data_list = []

            for section in sections:
                if not section.strip():
                    continue
                
                # Extract code
                code_match = re.search(r'CODE:\s*(D\d{4}|none)', section, re.IGNORECASE)
                code = [code_match.group(1)] if code_match and code_match.group(1) != 'none' else []
                
                # Extract explanation
                explanation_match = re.search(r'EXPLANATION:\s*(.*?)(?=\s*DOUBT:|\s*CODE:|$)', section, re.DOTALL | re.IGNORECASE)
                explanation = explanation_match.group(1).strip().replace('\n', ' ') if explanation_match else "No explanation provided"
                
                # Extract doubt
                doubt_match = re.search(r'DOUBT:\s*(.*?)(?=\s*CODE:|$)', section, re.DOTALL | re.IGNORECASE)
                doubt = doubt_match.group(1).strip().replace('\n', ' ') if doubt_match else "None"
                
                # Include all sections, even those with no codes
                parsed_data = {
                    "specific_codes": code,
                    "explanation": explanation,
                    "doubt": doubt
                }
                parsed_data_list.append(parsed_data)

            if not parsed_data_list:
                parsed_data_list.append({
                    "specific_codes": [],
                    "explanation": "No codes or explanation found in the provided raw output",
                    "doubt": "None"
                })

            # Update DentalCodeManager with the first parsed data
            if parsed_data_list:
                self.update_values(
                    name=self.name or "Dental Code Analysis",
                    strict=True,
                    explanation=parsed_data_list[0]["explanation"],
                    doubt=parsed_data_list[0]["doubt"],
                    code_range=self.schema["code_range"],
                    activated_subtopics=self.schema["activated_subtopics"],
                    specific_codes=parsed_data_list[0]["specific_codes"]
                )

            return parsed_data_list

        except Exception as e:
            error_data = {
                "specific_codes": [],
                "explanation": f"Error parsing output: {str(e)}",
                "doubt": "Error occurred during parsing"
            }
            self.update_values(
                name=self.name or "Dental Code Analysis",
                strict=False,
                explanation=error_data["explanation"],
                doubt=error_data["doubt"],
                code_range=self.schema["code_range"],
                activated_subtopics=self.schema["activated_subtopics"],
                specific_codes=[]
            )
            return [error_data]

    def transform_json_list(self, input_json_list: list) -> list:
        """
        Transform a list of topic JSONs by replacing each subtopic's raw_result with a list of parsed JSON objects.
        """
        output_json_list = copy.deepcopy(input_json_list)
        
        for topic_json in output_json_list:
            subtopics_data = topic_json['raw_result']['subtopics_data']
            for subtopic in subtopics_data:
                raw_result = subtopic['raw_result']
                parsed_results = self.parse_llm_output(raw_result)
                subtopic['raw_result'] = parsed_results
        
        return output_json_list

# Example usage with multiple topics
    

# Initialize DentalCodeManager
dental_manager = DentalCodeManager()

# Transform the JSON list
