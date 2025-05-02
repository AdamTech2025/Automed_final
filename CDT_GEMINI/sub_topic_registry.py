import asyncio
import inspect
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Callable, Any, Union, Coroutine
import logging
import os

# logging.basicConfig(level=logging.ERROR) # Removed duplicate config
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
        # logger.info(f"Registered topic: {name} ({code_range}), Async: {self.subtopics[-1]['is_async']}") # Removed info log
    
    async def activate_all(self, scenario: str, code_ranges_str: str) -> List[Dict[str, Any]]:
        """Activate relevant subtopics in parallel and return their raw results or errors."""
        raw_results_list = []
        activated_subtopic_names = set() # Keep track of names for logging/potential future use
        code_ranges_set = set(cr.strip() for cr in code_ranges_str.split(',') if cr.strip())
        # logger.info(f"Activating topics for code ranges: {code_ranges_set}") # Removed info log

        relevant_subtopics = []
        for subtopic in self.subtopics:
            if subtopic["code_range"] in code_ranges_set:
                relevant_subtopics.append(subtopic)
                activated_subtopic_names.add(subtopic["name"])

        # Create a fixed ThreadPoolExecutor with maximum workers
        max_workers = min(len(relevant_subtopics), os.cpu_count() or 4)
        thread_pool = ThreadPoolExecutor(max_workers=max_workers)
        loop = asyncio.get_running_loop()

        async def run_subtopic(subtopic: Dict[str, Any]) -> Dict[str, Any]:
            # logger.info(f"--> Activating topic: {subtopic['name']} ({subtopic['code_range']}) | Async: {subtopic['is_async']}") # Removed info log
            result_entry = {
                "topic": subtopic["name"],
                "code_range": subtopic["code_range"],
                "raw_result": None, # Initialize raw_result
                "error": None # Initialize error
            }
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
                        timeout=60  # Increased timeout to 60 seconds
                    )
                
                # logger.info(f"<-- Finished activating topic: {subtopic['name']}") # Removed info log
                result_entry["raw_result"] = result # Store the raw result

            except asyncio.TimeoutError:
                error_msg = "Timeout Error during activation"
                logger.error(f"{error_msg} of {subtopic['name']}")
                result_entry["error"] = error_msg # Store the error message
            except Exception as e:
                error_msg = f"Exception during activation: {e}"
                logger.error(f"{error_msg} of {subtopic['name']}", exc_info=True)
                result_entry["error"] = error_msg # Store the error message
            
            return result_entry # Return the entry with raw_result or error

        try:
            if relevant_subtopics:
                tasks = [run_subtopic(subtopic) for subtopic in relevant_subtopics]
                # logger.info(f"Gathering results for {len(tasks)} topic tasks...") # Removed info log
                # gathered_results will be a list of dictionaries like result_entry
                gathered_results = await asyncio.gather(*tasks) 
                # logger.info("Finished gathering topic results.") # Removed info log
                raw_results_list.extend(gathered_results) # Add all results (success or error)
            else:
                logger.warning("No relevant subtopics found to activate.")

            # Log summary (optional)
            successful_activations = [r for r in raw_results_list if r["error"] is None]
            failed_activations = [r for r in raw_results_list if r["error"] is not None]
            # logger.info(f"Activation summary: {len(successful_activations)} successful, {len(failed_activations)} failed.") # Removed info log

            # Return the list containing raw results or errors for each activated subtopic
            return raw_results_list 
            
        finally:
            # Ensure thread pool gets shut down
            thread_pool.shutdown(wait=False)