import json
from llm_services import get_service
from langchain.prompts import PromptTemplate

class DentalCodeManager:
    def _init_(self):
        self.name = ""
        self.strict = False
        self.schema = {
            "explanation": "",
            "doubt": "",
            "code_range": "",
            "activated_subtopics": "",
            "specific_codes": []
        }
        self.llm_service = get_service()
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

    def parse_llm_output(self, raw_output: str) -> dict:
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
                    return parsed_data

            except (json.JSONDecodeError, AttributeError):
                pass

            # Use LLM to parse the raw output if not in JSON format
            parsed_str = self.llm_service.invoke_chain(self.parser_prompt, {"raw_output": raw_output})
            
            # Clean the response to ensure it's valid JSON
            parsed_str = parsed_str.strip()
            if not parsed_str.startswith('{'): 
                parsed_str = parsed_str[parsed_str.find('{'):]
            if not parsed_str.endswith('}'):
                parsed_str = parsed_str[:parsed_str.rfind('}')+1]
            
            try:
                parsed_data = json.loads(parsed_str)
            except json.JSONDecodeError:
                # Fallback parsing using regex if JSON parsing fails
                import re
                codes = re.findall(r'D\d{4}', raw_output)
                explanation = re.search(r'EXPLANATION:\s*(.*?)(?=\s*DOUBT:|$)', raw_output, re.DOTALL | re.IGNORECASE)
                doubt = re.search(r'DOUBT:\s*(.*)', raw_output, re.DOTALL | re.IGNORECASE)
                
                parsed_data = {
                    "specific_codes": codes,
                    "explanation": explanation.group(1).strip() if explanation else "No explanation provided",
                    "doubt": doubt.group(1).strip() if doubt else "None"
                }
            
            # Update the schema with parsed data
            self.update_values(
                name=self.name or "Dental Code Analysis",
                strict=True,
                explanation=parsed_data.get("explanation", ""),
                doubt=parsed_data.get("doubt", "None"),
                code_range=self.schema["code_range"],
                activated_subtopics=self.schema["activated_subtopics"],
                specific_codes=parsed_data.get("specific_codes", [])
            )
            return parsed_data
        except Exception as e:
            print(f"Error parsing LLM output: {str(e)}")
            # Return a valid structure even in case of error
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
            return error_data

    def to_json(self):
        return json.dumps({
            "name": self.name,
            "strict": self.strict,
            "schema": self.schema
        }, indent=4)

dental_manager = DentalCodeManager()