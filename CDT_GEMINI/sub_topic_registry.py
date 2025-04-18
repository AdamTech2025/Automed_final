import asyncio
import inspect
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Callable, Any, Union, Coroutine

class SubtopicRegistry:
    """Registry for managing subtopic activation functions."""
    
    def __init__(self):
        self.subtopics: List[Dict[str, Any]] = []
    
    def register(self, code_range: str, activate_func: Union[Callable, Coroutine], name: str):
        """Register a subtopic with its activation function."""
        self.subtopics.append({
            "code_range": code_range,
            "activate_func": activate_func,
            "name": name,
            "is_async": inspect.iscoroutinefunction(activate_func)
        })
    
    async def activate_all(self, scenario: str, code_ranges: str) -> Dict[str, Any]:
        """Activate all relevant subtopics in parallel."""
        results_list = []
        activated_subtopics = []
        
        async def run_subtopic(subtopic: Dict[str, Any]) -> Dict[str, Any]:
            if subtopic["code_range"] in code_ranges:
                print(f"Activating subtopic: {subtopic['name']}")
                
                # Handle the function based on whether it's async or not
                if subtopic["is_async"]:
                    # If it's an async function, await it directly
                    result = await subtopic["activate_func"](scenario)
                else:
                    # If it's a synchronous function, run it in a thread pool
                    loop = asyncio.get_running_loop()
                    with ThreadPoolExecutor() as pool:
                        result = await loop.run_in_executor(pool, lambda: subtopic["activate_func"](scenario))
                
                # Format the result properly based on response structure
                return {
                    "raw_result": result,
                    "name": subtopic["name"],
                    "code_range": subtopic["code_range"]
                }
            return None
        
        # Run all relevant subtopics concurrently
        tasks = [run_subtopic(subtopic) for subtopic in self.subtopics]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        for result in results:
            if isinstance(result, Exception):
                print(f"Error in subtopic activation: {result}")
                continue
                
            if result and result.get("raw_result"):
                # Parse the raw result to extract properly formatted data
                parsed_result = self._parse_topic_result(result["raw_result"], result["name"], result["code_range"])
                if parsed_result:
                    results_list.append(parsed_result)
                    activated_subtopics.append(result["name"])
        
        return {
            "topic_result": results_list,
            "activated_subtopics": activated_subtopics
        }
    
    def _parse_topic_result(self, raw_result: str, topic_name: str, code_range: str) -> Dict[str, Any]:
        """Parse the raw result from topic activation into a properly structured format."""
        try:
            # Handle empty responses
            if not raw_result:
                return None
                
            # If the result is already a dictionary, use it directly
            if isinstance(raw_result, dict):
                # Ensure the dict has the proper format
                if "topic" not in raw_result:
                    raw_result["topic"] = topic_name
                if "code_range" not in raw_result:
                    raw_result["code_range"] = code_range
                # Remove subtopic field if it exists
                if "subtopic" in raw_result:
                    del raw_result["subtopic"]
                return raw_result
            
            # Otherwise, parse the text format
            explanation = ""
            doubt = ""
            parsed_codes = []
            
            if "EXPLANATION:" in raw_result:
                parts = raw_result.split("EXPLANATION:")
                for part in parts[1:]:  # Skip the first empty part
                    code_part = ""
                    exp_part = ""
                    doubt_part = ""
                    
                    if "DOUBT:" in part:
                        exp_doubt_parts = part.split("DOUBT:")
                        exp_part = exp_doubt_parts[0].strip()
                        
                        if "CODE:" in exp_doubt_parts[1]:
                            doubt_code_parts = exp_doubt_parts[1].split("CODE:")
                            doubt_part = doubt_code_parts[0].strip()
                            code_part = doubt_code_parts[1].strip() if len(doubt_code_parts) > 1 else ""
                        else:
                            doubt_part = exp_doubt_parts[1].strip()
                    elif "CODE:" in part:
                        exp_code_parts = part.split("CODE:")
                        exp_part = exp_code_parts[0].strip()
                        code_part = exp_code_parts[1].strip() if len(exp_code_parts) > 1 else ""
                    else:
                        exp_part = part.strip()
                    
                    if code_part:
                        # Split multiple codes if they exist
                        code_values = [c.strip() for c in code_part.split(",")]
                        for code in code_values:
                            parsed_codes.append({
                                "explanation": exp_part,
                                "doubt": doubt_part,
                                "code": code
                            })
            
            # If we couldn't parse codes but still have a result
            if not parsed_codes and raw_result.strip():
                return {
                    "topic": topic_name,
                    "explanation": "",
                    "doubt": "",
                    "code_range": code_range, 
                    "raw_text": raw_result.strip(),
                    "codes": []
                }
            
            # Extract main explanation and doubt from the topic level if available
            topic_explanation = ""
            topic_doubt = ""
            
            # Try to extract topic-level explanation and doubt
            if "TOPIC EXPLANATION:" in raw_result:
                topic_parts = raw_result.split("TOPIC EXPLANATION:")
                if len(topic_parts) > 1:
                    if "TOPIC DOUBT:" in topic_parts[1]:
                        topic_exp_doubt = topic_parts[1].split("TOPIC DOUBT:")
                        topic_explanation = topic_exp_doubt[0].strip()
                        topic_doubt = topic_exp_doubt[1].strip() if len(topic_exp_doubt) > 1 else ""
                    else:
                        topic_explanation = topic_parts[1].strip()
            
            # Return a flattened structure without nested codes
            result = {
                "topic": topic_name,
                "explanation": topic_explanation,
                "doubt": topic_doubt,
                "code_range": code_range,
                "codes": parsed_codes
            }
            
            return result
            
        except Exception as e:
            print(f"Error parsing topic result: {str(e)}")
            # Return the raw result as a fallback
            return {
                "topic": topic_name,
                "explanation": "",
                "doubt": "",
                "code_range": code_range,
                "error": str(e),
                "raw_text": raw_result,
                "codes": []
            }