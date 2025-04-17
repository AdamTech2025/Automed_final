import asyncio
import inspect
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Callable, Any, Union, Coroutine
import re

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
                parsed_result = self._parse_topic_result(result["name"], result["raw_result"], result["code_range"])
                if parsed_result:
                    results_list.append(parsed_result)
                    activated_subtopics.append(result["name"])
        
        return {
            "topic_result": results_list,
            "activated_subtopics": activated_subtopics
        }
    
    def _parse_topic_result(self, topic_name: str, raw_result: Any, code_range: str) -> Dict[str, Any]:
        """Parse the raw LLM text output (expected string) for a topic into structured data."""
        
        # --- Input Type Validation ---
        if not isinstance(raw_result, str):
            print(f"Error parsing topic result for '{topic_name}': Expected raw_result to be a string, but got {type(raw_result)}.")
            # Fallback: return basic structure with error and raw input (converted to str for safety)
            return {
                "topic": topic_name,
                "explanation": "",
                "doubt": "",
                "code_range": code_range,
                "error": f"Parsing Error: Invalid input type - Expected string, got {type(raw_result).__name__}",
                "raw_text": str(raw_result), # Store the problematic input as string
                "codes": []
            }
        # --- End Validation ---

        parsed_codes = []
        current_explanation = ""
        current_doubt = ""
        
        lines = raw_result.strip().split('\n')

        try:
            for line in lines:
                stripped_line = line.strip()
                
                # Case-insensitive matching for markers
                if stripped_line.upper().startswith("EXPLANATION:"):
                    # Capture explanation, potentially overwriting previous if multiple are found before a code
                    current_explanation = stripped_line[len("EXPLANATION:"):].strip()
                elif stripped_line.upper().startswith("DOUBT:"):
                    # Capture doubt
                    current_doubt = stripped_line[len("DOUBT:"):].strip()
                elif stripped_line.upper().startswith("CODE:"):
                    code_part = stripped_line[len("CODE:"):].strip()
                    
                    # Ignore "none" or empty code parts
                    if code_part.lower() == "none" or not code_part:
                        continue
                        
                    # Extract potential codes (split by comma, handle potential surrounding text)
                    potential_codes = [c.strip() for c in code_part.split(',')]
                    
                    for pc in potential_codes:
                        # Basic validation: check if it looks like a code (e.g., Dxxxx or Kxx.x)
                        # This is a simple check and might need refinement for stricter validation
                        if re.match(r'^[A-Z][0-9]{1,}[A-Z0-9\.]*$', pc, re.IGNORECASE):
                            # Check if it's just "none" after stripping/validation
                             if pc.lower() != 'none':
                                parsed_codes.append({
                                    "code": pc,
                                    "explanation": current_explanation, 
                                    "doubt": current_doubt
                                })
                        # else: Consider logging codes that didn't match the pattern? 
                            
                    # Reset explanation/doubt after processing a CODE line 
                    # so they don't carry over to subsequent unrelated codes
                    # current_explanation = "" # Keep the last explanation/doubt until a new one is found
                    # current_doubt = "" 

            # If no codes were parsed, return the raw text for inspection
            if not parsed_codes and raw_result.strip():
                return {
                    "topic": topic_name,
                    "explanation": "", # Keep top-level fields for consistent structure
                    "doubt": "",
                    "code_range": code_range, 
                    "raw_text": raw_result.strip(), # Include raw text if parsing failed
                    "codes": []
                }

            # Return the structured result with the list of codes
            return {
                "topic": topic_name,
                "explanation": "", # Keep top-level explanation/doubt empty now
                "doubt": "",
                "code_range": code_range,
                "codes": parsed_codes 
            }
            
        except Exception as e:
            print(f"Error parsing topic result for '{topic_name}': {str(e)}")
            # Fallback: return basic structure with error and raw text
            return {
                "topic": topic_name,
                "explanation": "",
                "doubt": "",
                "code_range": code_range,
                "error": f"Parsing Error: {str(e)}",
                "raw_text": raw_result,
                "codes": []
            }