import asyncio
import inspect
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Callable, Any, Union, Coroutine
import re
import logging
import os

logger = logging.getLogger(__name__)

class SubtopicRegistry:
    """Registry for managing subtopic activation functions."""
    
    def __init__(self):
        self.subtopics: List[Dict[str, Any]] = []
    
    def register(self, code_range: str, activate_func: Union[Callable, Coroutine], name: str):
        """Register a subtopic with its activation function."""
        if not callable(activate_func):
            raise TypeError(f"activate_func for topic '{name}' must be callable, got {type(activate_func)}")
        
        self.subtopics.append({
            "code_range": code_range,
            "activate_func": activate_func,
            "name": name,
            "is_async": inspect.iscoroutinefunction(activate_func)
        })
        logger.info(f"Registered topic: {name} ({code_range}), Async: {self.subtopics[-1]['is_async']}")
    
    async def activate_all(self, scenario: str, code_ranges_str: str) -> Dict[str, Any]:
        """Activate all relevant subtopics in parallel based on a comma-separated string of code ranges/keys."""
        results_list = []
        activated_subtopics_names = set()
        code_ranges_set = set(cr.strip() for cr in code_ranges_str.split(',') if cr.strip())
        logger.info(f"Activating topics for code ranges: {code_ranges_set}")

        relevant_subtopics = []
        for subtopic in self.subtopics:
            if subtopic["code_range"] in code_ranges_set:
                relevant_subtopics.append(subtopic)

        # Create a fixed ThreadPoolExecutor with maximum workers
        max_workers = min(len(relevant_subtopics), os.cpu_count() or 4)
        thread_pool = ThreadPoolExecutor(max_workers=max_workers)
        loop = asyncio.get_running_loop()

        async def run_subtopic(subtopic: Dict[str, Any]) -> Dict[str, Any]:
            logger.info(f"--> Activating topic: {subtopic['name']} ({subtopic['code_range']}) | Async: {subtopic['is_async']}")
            try:
                if subtopic["is_async"]:
                    # Directly await async function
                    result = await subtopic["activate_func"](scenario)
                else:
                    # Run in thread pool with timeout
                    result = await asyncio.wait_for(
                        loop.run_in_executor(
                            thread_pool, 
                            lambda s=scenario: subtopic["activate_func"](s)
                        ),
                        timeout=30  # Add timeout to prevent hanging
                    )
                
                logger.info(f"<-- Finished activating topic: {subtopic['name']}")
                return {
                    "raw_result": result,
                    "name": subtopic["name"],
                    "code_range": subtopic["code_range"]
                }
            except asyncio.TimeoutError:
                logger.error(f"Timeout occurred during activation of {subtopic['name']}")
                return {
                    "exception": "Timeout Error", 
                    "name": subtopic["name"], 
                    "code_range": subtopic["code_range"]
                }
            except Exception as e:
                logger.error(f"Exception during activation of {subtopic['name']}: {e}", exc_info=True)
                return {
                    "exception": e, 
                    "name": subtopic["name"], 
                    "code_range": subtopic["code_range"]
                }

        try:
            if relevant_subtopics:
                tasks = [run_subtopic(subtopic) for subtopic in relevant_subtopics]
                logger.info(f"Gathering results for {len(tasks)} topic tasks...")
                gathered_results = await asyncio.gather(*tasks)
                logger.info("Finished gathering topic results.")
            else:
                gathered_results = []
                logger.warning("No relevant subtopics found to activate.")

            for result_data in gathered_results:
                topic_name = result_data.get("name", "Unknown")
                code_range = result_data.get("code_range", "Unknown")
                
                if "exception" in result_data:
                    logger.error(f"Activation failed for topic '{topic_name}': {result_data['exception']}")
                    results_list.append({
                        "topic": topic_name,
                        "code_range": code_range,
                        "error": f"Activation failed: {str(result_data['exception'])}"
                    })
                    continue

                raw_result = result_data.get("raw_result")
                logger.debug(f"Parsing result for topic '{topic_name}': {str(raw_result)[:100]}...")
                parsed_result = self._parse_topic_result(raw_result, topic_name, code_range)
                
                if parsed_result:
                    results_list.append(parsed_result)
                    activated_subtopics_names.add(topic_name)
                    logger.debug(f"Successfully parsed result for '{topic_name}'.")
                else:
                    logger.warning(f"Parsing result for '{topic_name}' yielded no meaningful data. Raw result: {str(raw_result)[:100]}...")

            return {
                "topic_result": results_list,
                "activated_subtopics": sorted(list(activated_subtopics_names))
            }
        finally:
            # Ensure thread pool gets shut down
            thread_pool.shutdown(wait=False)
    
    def _parse_topic_result(self, raw_result: Any, topic_name: str, code_range: str) -> Dict[str, Any]:
        """Parse the raw result from a topic activation function into a structured format.
           Ensures raw_data is included within individual code entries if available.
        """
        parsed_topic_result = {
            "topic": topic_name,
            "code_range": code_range,
            "code": None  # Initialize code as null by default
        }
        parsed_codes_list = []

        try:
            if raw_result is None or raw_result == '':
                logger.debug(f"No raw result provided for topic '{topic_name}'.")
                return None

            if isinstance(raw_result, dict):
                logger.debug(f"Parsing dictionary result for topic '{topic_name}'. Keys: {list(raw_result.keys())}")
                if raw_result.get("explanation"): parsed_topic_result["explanation"] = raw_result["explanation"]
                if raw_result.get("doubt"): parsed_topic_result["doubt"] = raw_result["doubt"]
                if raw_result.get("error"): parsed_topic_result["error"] = raw_result.get("error")
                
                topic_level_raw_data = raw_result.get("raw_data")
                if parsed_topic_result.get("error") and topic_level_raw_data:
                    parsed_topic_result["raw_topic_data"] = topic_level_raw_data

                # Check for direct code in the result
                if raw_result.get("code") is not None:
                    # Add to the top level if it's a non-empty string
                    if raw_result.get("code") and raw_result.get("code").lower() != 'none':
                        parsed_topic_result["code"] = raw_result.get("code")
                    
                    code_entry = {
                        "code": raw_result.get("code"),
                        "explanation": raw_result.get("explanation"),
                        "doubt": raw_result.get("doubt"),
                        "raw_data": topic_level_raw_data
                    }
                    cleaned_entry = {k: v for k, v in code_entry.items() if v is not None}
                    if cleaned_entry.get("code") is not None:
                        logger.debug(f"  Parsed single code entry: {cleaned_entry.get('code')}")
                        parsed_codes_list.append(cleaned_entry)
                    else:
                        logger.warning(f"  Found 'code' key but it was None or empty for topic '{topic_name}'.")

                elif "codes" in raw_result and isinstance(raw_result.get("codes"), list):
                    logger.debug(f"  Parsing 'codes' list for topic '{topic_name}'.")
                    for i, sub_code_entry in enumerate(raw_result.get("codes", [])):
                        if isinstance(sub_code_entry, dict):
                            raw_data_for_sub = sub_code_entry.get("raw_data", topic_level_raw_data)
                            code_entry = {
                                "code": sub_code_entry.get("code"),
                                "explanation": sub_code_entry.get("explanation"),
                                "doubt": sub_code_entry.get("doubt"),
                                "raw_data": raw_data_for_sub
                            }
                            cleaned_entry = {k: v for k, v in code_entry.items() if v is not None}
                            if cleaned_entry.get("code") is not None:
                                # For the first valid code, elevate it to the top level
                                if i == 0 and cleaned_entry.get("code") and cleaned_entry.get("code").lower() != 'none':
                                    parsed_topic_result["code"] = cleaned_entry.get("code")
                                
                                logger.debug(f"    Parsed sub-code entry {i}: {cleaned_entry.get('code')}")
                                parsed_codes_list.append(cleaned_entry)
                            else:
                                logger.warning(f"    Sub-code entry {i} in '{topic_name}' had None or empty code.")
                        elif isinstance(sub_code_entry, str):
                            # For the first valid code, elevate it to the top level
                            if i == 0 and sub_code_entry and sub_code_entry.lower() != 'none':
                                parsed_topic_result["code"] = sub_code_entry
                                
                            logger.debug(f"    Parsed sub-code entry {i} as string: {sub_code_entry}")
                            parsed_codes_list.append({"code": sub_code_entry, "raw_data": sub_code_entry})
                        else:
                            logger.warning(f"    Unexpected type for sub-code entry {i} in '{topic_name}': {type(sub_code_entry)}")

                elif topic_level_raw_data and not parsed_codes_list and not parsed_topic_result.get("error"):
                    logger.debug(f"  No codes found for '{topic_name}', storing raw_topic_data.")
                    parsed_topic_result["raw_topic_data"] = topic_level_raw_data

            elif isinstance(raw_result, str):
                logger.debug(f"Parsing string result for topic '{topic_name}'.")
                raw_text = raw_result.strip()
                if raw_text.lower() == 'none':
                    logger.debug(f"  Raw string result was 'none' for '{topic_name}'.")
                    return None

                code_match = re.search(r"CODE:\s*(.*?)(?=\n\s*EXPLANATION:|\n\s*DOUBT:|\Z)", raw_text, re.DOTALL | re.IGNORECASE)
                exp_match = re.search(r"EXPLANATION:\s*(.*?)(?=\n\s*DOUBT:|\Z)", raw_text, re.DOTALL | re.IGNORECASE)
                doubt_match = re.search(r"DOUBT:\s*(.*)", raw_text, re.DOTALL | re.IGNORECASE)

                code = code_match.group(1).strip() if code_match else None
                explanation = exp_match.group(1).strip() if exp_match else None
                doubt = doubt_match.group(1).strip() if doubt_match else None

                # Check if code is 'none' and keep it as null in that case
                if code and code.lower() == 'none':
                    code = None
                else:
                    # For a valid code, also elevate it to the top level
                    if code:
                        parsed_topic_result["code"] = code
                
                explanation = None if explanation and explanation.lower() == 'none' else explanation
                doubt = None if doubt and doubt.lower() == 'none' else doubt
                
                if code is not None:
                    code_entry = {
                        "code": code,
                        "explanation": explanation,
                        "doubt": doubt,
                        "raw_data": raw_text
                    }
                    cleaned_entry = {k: v for k, v in code_entry.items() if v is not None}
                    logger.debug(f"  Parsed single code entry from string: {cleaned_entry.get('code')}")
                    parsed_codes_list.append(cleaned_entry)
                elif raw_text:
                    logger.debug(f"  No code parsed from string for '{topic_name}', storing raw_topic_data.")
                    parsed_topic_result["raw_topic_data"] = raw_text
            else:
                logger.warning(f"Unexpected raw_result type for topic '{topic_name}': {type(raw_result)}")
                parsed_topic_result["error"] = f"Unexpected result type: {type(raw_result)}"

            if parsed_codes_list:
                parsed_topic_result["codes"] = parsed_codes_list
            
            # If no valid codes were found, either set code_range to null or keep it for reference
            # only if there's an explanation or raw data that's meaningful to return
            if not parsed_codes_list:
                # Check if raw string result explicitly says "CODE: none"
                if (isinstance(raw_result, str) and "CODE:" in raw_result and 
                    re.search(r"CODE:\s*none", raw_result, re.IGNORECASE)):
                    # For ICD topics which specifically return "CODE: none" in their raw data
                    # We'll still retain the topic name but remove the code_range to avoid confusion
                    logger.debug(f"Topic '{topic_name}' explicitly returned 'CODE: none'")
                    # Keep the topic name but mark code_range as null
                    # This avoids confusion where a code_range exists but no actual code was found
                    parsed_topic_result["code_range"] = None
                # For other cases where no codes were found but there's meaningful data to return
                elif isinstance(raw_result, dict) and raw_result.get("code") is None and "code" in raw_result:
                    # If the service explicitly returned code=None
                    logger.debug(f"Topic '{topic_name}' returned code: None")
                    parsed_topic_result["code_range"] = None

            is_meaningful = any(key in parsed_topic_result for key in ["codes", "explanation", "doubt", "error", "raw_topic_data"])
            
            if not is_meaningful:
                logger.debug(f"Parsed result for '{topic_name}' deemed not meaningful.")
                return None
            
            logger.debug(f"Final parsed result for '{topic_name}': {parsed_topic_result}")
            return parsed_topic_result

        except Exception as e:
            logger.error(f"Error during parsing of topic result for '{topic_name}': {e}", exc_info=True)
            error_result = {
                "topic": topic_name,
                "code_range": code_range,
                "error": f"Parsing failed: {str(e)}"
            }
            if isinstance(raw_result, str):
                error_result["raw_topic_data"] = raw_result
            elif isinstance(raw_result, dict) and raw_result.get("raw_data"):
                error_result["raw_topic_data"] = raw_result.get("raw_data")
            elif isinstance(raw_result, dict):
                error_result["raw_result_dict"] = raw_result
            return error_result