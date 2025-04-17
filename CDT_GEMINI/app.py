from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import asyncio
from typing import Dict, Any, List, Tuple
import json
import datetime
import time  # Import the time module
import traceback # Import traceback

# Import the data cleaner and cdt classifier
from data_cleaner import DentalScenarioProcessor
from cdt_classifier import CDTClassifier
from icd_classifier import ICDClassifier
from sub_topic_registry import SubtopicRegistry
from questioner import Questioner
from inspector import DentalInspector
from icd_inspector import ICDInspector
# Import database
from database import MedicalCodingDB

# Import topic functions
from topics.diagnostics import diagnostic_service
from topics.preventive import preventive_service
from topics.restorative import restorative_service
from topics.endodontics import endodontic_service
from topics.periodontics import periodontic_service
from topics.prosthodonticsremovable import prosthodontics_service
from topics.maxillofacialprosthetics import maxillofacial_service
from topics.implantservices import implant_service
from topics.prosthodonticsfixed import prosthodontics_service
from topics.oralandmaxillofacialsurgery import oral_surgery_service
from topics.orthodontics import orthodontic_service
from topics.adjunctivegeneralservices import adjunctive_general_services_service

# Import the add_code functionality
from add_codes.add_code_data import Add_code_data

# Initialize FastAPI app
app = FastAPI(title="Dental Code Extractor API")

# Initialize data cleaner, classifiers and database connection
cleaner = DentalScenarioProcessor()
cdt_classifier = CDTClassifier()
icd_classifier = ICDClassifier()
questioner = Questioner()
cdt_inspector = DentalInspector()
icd_inspector = ICDInspector()
# Initialize database connection
db = MedicalCodingDB()

# Create TopicRegistry for parallel activation
topic_registry = SubtopicRegistry()

# Map CDT code ranges to topic functions
CDT_TOPIC_MAPPING = {
    "D0100-D0999": {"func": diagnostic_service.activate_diagnostic, "name": "Diagnostic"},
    "D1000-D1999": {"func": preventive_service.activate_preventive, "name": "Preventive"},
    "D2000-D2999": {"func": restorative_service.activate_restorative, "name": "Restorative"},
    "D3000-D3999": {"func": endodontic_service.activate_endodontic, "name": "Endodontics"},
    "D4000-D4999": {"func": periodontic_service.activate_periodontic, "name": "Periodontics"},
    "D5000-D5899": {"func": prosthodontics_service.activate_prosthodontics_fixed, "name": "Prosthodontics Removable"},
    "D5900-D5999": {"func": maxillofacial_service.activate_maxillofacial_prosthetics, "name": "Maxillofacial Prosthetics"},
    "D6000-D6199": {"func": implant_service.activate_implant_services, "name": "Implant Services"},
    "D6200-D6999": {"func": prosthodontics_service.activate_prosthodontics_fixed, "name": "Prosthodontics Fixed"},
    "D7000-D7999": {"func": oral_surgery_service.activate_oral_maxillofacial_surgery, "name": "Oral and Maxillofacial Surgery"},
    "D8000-D8999": {"func": orthodontic_service.activate_orthodontic, "name": "Orthodontics"},
    "D9000-D9999": {"func": adjunctive_general_services_service.activate_adjunctive_general_services, "name": "Adjunctive General Services"}
}

# Register all topics with the registry
for code_range, topic_info in CDT_TOPIC_MAPPING.items():
    topic_registry.register(code_range, topic_info["func"], topic_info["name"])

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://dentalcoder.vercel.app", 
        "https://automed.adamtechnologies.in", 
        "http://automed.adamtechnologies.in",
        os.getenv("FRONTEND_URL", "")  # Get from environment variable
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper function to map specific CDT codes to their broader category
def map_to_cdt_category(specific_code: str) -> str:
    """Maps a specific CDT code or range to its broader category."""
    # Extract the base code without the range
    if "-" in specific_code:
        base_code = specific_code.split("-")[0]
    else:
        base_code = specific_code
    
    # Get the first 2 characters
    category_prefix = base_code[:2]
    
    # Map to the corresponding category
    if category_prefix == "D0":
        return "D0100-D0999"
    elif category_prefix == "D1":
        return "D1000-D1999"
    elif category_prefix == "D2":
        return "D2000-D2999"
    elif category_prefix == "D3":
        return "D3000-D3999"
    elif category_prefix == "D4":
        return "D4000-D4999"
    elif category_prefix == "D5":
        # Check if it's in the range D5000-D5899 or D5900-D5999
        if len(base_code) > 1 and base_code[1].isdigit() and int(base_code[1]) < 9:
            return "D5000-D5899" # Simplified check for D50xx-D58xx
        else:
            return "D5900-D5999"
    elif category_prefix == "D6":
        # Check if it's in the range D6000-D6199 or D6200-D6999
        if len(base_code) > 1 and base_code[1].isdigit() and int(base_code[1]) < 2:
             return "D6000-D6199" # Simplified check for D60xx-D61xx
        else:
            return "D6200-D6999"
    elif category_prefix == "D7":
        return "D7000-D7999"
    elif category_prefix == "D8":
        return "D8000-D8999"
    elif category_prefix == "D9":
        return "D9000-D9999"
    else:
        return None

# Request model
class ScenarioRequest(BaseModel):
    scenario: str

class BatchScenarioRequest(BaseModel):
    scenarios: List[str]

class QuestionAnswersRequest(BaseModel):
    answers: str

# Request model for adding custom codes
class CustomCodeRequest(BaseModel):
    code: str
    scenario: str
    record_id: str

# Request model for storing code status
class CodeStatusRequest(BaseModel):
    record_id: str
    cdt_codes: List[str] = []
    icd_codes: List[str] = []
    rejected_cdt_codes: List[str] = []
    rejected_icd_codes: List[str] = []

# --- Refactored Processing Steps ---

async def clean_scenario(scenario: str) -> dict:
    """Step 1: Process the input through data_cleaner."""
    start_time = time.time()
    print(f"🔍 Cleaning Scenario: {scenario[:50]}...")
    try:
        processed_result = cleaner.process(scenario)
        processed_scenario = processed_result["standardized_scenario"]
        print(f"✅ Cleaned Scenario in {time.time() - start_time:.2f}s: {processed_scenario[:50]}...")
        return {
            "original_scenario": scenario,
            "processed_scenario": processed_scenario,
            "status": "success"
        }
    except Exception as e:
        print(f"❌ Error cleaning scenario: {str(e)}")
        error_details = traceback.format_exc()
        return {
            "original_scenario": scenario,
            "processed_scenario": None,
            "status": "error",
            "message": f"Data Cleaning Error: {str(e)}",
            "details": error_details
        }

async def classify_scenario(processed_scenario: str) -> Tuple[dict, dict]:
    """Step 2: Process the cleaned scenario with CDT and ICD classifiers in parallel."""
    start_time = time.time()
    print(f"🔬 Classifying Scenario: {processed_scenario[:50]}...")
    if not processed_scenario:
         print(f"⚠️ Skipping classification due to missing processed_scenario")
         return {"error": "Missing processed scenario", "status": "error"}, {"error": "Missing processed scenario", "status": "error"}
    try:
        async def run_cdt_classification():
            return cdt_classifier.process(processed_scenario)

        async def run_icd_classification():
            return icd_classifier.process(processed_scenario)

        cdt_task = asyncio.create_task(run_cdt_classification())
        icd_task = asyncio.create_task(run_icd_classification())

        cdt_result, icd_result = await asyncio.gather(cdt_task, icd_task)
        print(f"✅ Classified Scenario in {time.time() - start_time:.2f}s")
        # Add status to results
        cdt_result["status"] = "success" if not cdt_result.get("error") else "error"
        icd_result["status"] = "success" if not icd_result.get("error") else "error"
        return cdt_result, icd_result
    except Exception as e:
        print(f"❌ Error classifying scenario: {str(e)}")
        error_details = traceback.format_exc()
        error_msg = f"Classification Error: {str(e)}"
        return {"error": error_msg, "details": error_details, "status": "error"}, {"error": error_msg, "details": error_details, "status": "error"}

async def activate_topics_for_scenario(processed_scenario: str, cdt_result: dict) -> dict:
    """Step 3: Activate topics in parallel based on code ranges."""
    start_time = time.time()
    print(f"⚡ Activating Topics for Scenario: {processed_scenario[:50]}...")
    if not processed_scenario or not cdt_result or "range_codes_string" not in cdt_result or cdt_result.get("status") == "error":
        print(f"⚠️ Skipping topic activation due to missing/invalid data")
        return {"error": "Missing processed scenario or valid CDT classification results", "status": "error"}
    try:
        range_codes = cdt_result["range_codes_string"].split(",")
        category_ranges = set()
        for range_code in range_codes:
            category = map_to_cdt_category(range_code.strip())
            if category:
                category_ranges.add(category)
        category_ranges_str = ",".join(category_ranges)

        topic_results_data = await topic_registry.activate_all(processed_scenario, category_ranges_str)

        activated_subtopics = topic_results_data.get('activated_subtopics', [])
        topic_result_list = topic_results_data.get('topic_result', [])

        # Process topic_result to extract codes by subtopic
        subtopic_data = {}
        for topic_item in topic_result_list:
            if "codes" in topic_item:
                for subtopic_code in topic_item["codes"]:
                    subtopic_name = subtopic_code.get("topic", "Unknown Subtopic")
                    code_range = subtopic_code.get("code_range", "")
                    subtopic_key = f"{subtopic_name} ({code_range})"

                    if "codes" in subtopic_code:
                        codes_list = []
                        for code_entry in subtopic_code["codes"]:
                            code = code_entry.get("code", "Unknown")
                            if isinstance(code, str):
                                if " - " in code:
                                    code = code.split(" - ")[0].strip()
                            explanation = code_entry.get("explanation", "")
                            doubt = code_entry.get("doubt", "")
                            codes_list.append({"code": code, "explanation": explanation, "doubt": doubt})

                        if subtopic_key not in subtopic_data:
                            subtopic_data[subtopic_key] = []
                        subtopic_data[subtopic_key].extend(codes_list)

        # Remove codes arrays from topic_result to avoid duplication in main structure
        cleaned_topic_result = []
        for topic_item in topic_result_list:
            cleaned_item = {
                "topic": topic_item.get("topic", "Unknown"),
                "code_range": topic_item.get("code_range", ""),
                "activated_subtopics": topic_item.get("activated_subtopics", []) # Keep this for context if needed
            }
            cleaned_topic_result.append(cleaned_item)

        print(f"✅ Topics Activated in {time.time() - start_time:.2f}s")
        return {
            "activated_subtopics": activated_subtopics,
            "topic_result": cleaned_topic_result, # Use cleaned version
            "subtopic_data": subtopic_data,
            "status": "success"
        }
    except Exception as e:
        print(f"❌ Error activating topics: {str(e)}")
        error_details = traceback.format_exc()
        return {
            "error": f"Topic Activation Error: {str(e)}",
            "details": error_details,
            "status": "error"
        }

async def save_initial_data(scenario_data: dict) -> dict:
    """Step 4a: Save initial analysis data to the database."""
    print(f"💾 Saving initial data for scenario: {scenario_data.get('original_scenario', '')[:50]}...")
    record_id = None
    try:
        # Ensure previous steps were successful
        if (scenario_data.get("status") == "error" or
            scenario_data.get("cdt_result", {}).get("status") == "error" or
            scenario_data.get("topic_activation_result", {}).get("status") == "error"):
            raise ValueError("Cannot save data due to errors in previous steps.")


        # Prepare CDT data
        formatted_cdt_results = []
        cdt_classifier_results = scenario_data.get("cdt_result", {}).get("formatted_results", [])
        if cdt_classifier_results:
             for result in cdt_classifier_results:
                 formatted_cdt_results.append({
                    "code_range": result.get("code_range", ""),
                    "explanation": result.get("explanation", ""),
                    "doubt": result.get("doubt", "")
                 })

        topic_activation_result = scenario_data.get("topic_activation_result", {})
        db_topic_result = topic_activation_result.get("topic_result", []) # Already cleaned

        complete_cdt_data = {
            "cdt_classification": {
                "CDT_classifier": formatted_cdt_results,
                 "range_codes_string": scenario_data.get("cdt_result", {}).get("range_codes_string", "")
            },
            "topics_results": {
                "topic_result": db_topic_result,
                "subtopic_data": topic_activation_result.get("subtopic_data", {}),
                "activated_subtopics": topic_activation_result.get("activated_subtopics", [])
            }
        }

        # Prepare ICD data
        complete_icd_data = {}
        icd_result = scenario_data.get("icd_result", {})
        primary_icd_code = ""
        primary_explanation = ""
        primary_doubt = ""

        if icd_result and icd_result.get("status") == "success":
            # Simplified logic for primary ICD code extraction (can be enhanced)
            # Attempt extraction from parsed topic result first
            if "icd_topics_results" in icd_result and icd_result["icd_topics_results"]:
                if "category_numbers_string" in icd_result and icd_result["category_numbers_string"]:
                    categories = icd_result["category_numbers_string"].split(",")
                    if categories:
                        primary_category = categories[0]
                        if primary_category in icd_result["icd_topics_results"]:
                            topic_data = icd_result["icd_topics_results"][primary_category]
                            if "parsed_result" in topic_data:
                                parsed = topic_data["parsed_result"]
                                primary_icd_code = parsed.get("code", "")
                                primary_explanation = parsed.get("explanation", "")
                                primary_doubt = parsed.get("doubt", "")

            # Fallback to direct classification result if topic result didn't yield code
            if not primary_icd_code:
                if "icd_codes" in icd_result and icd_result["icd_codes"]:
                    primary_icd_code = icd_result["icd_codes"][0]
                if "explanations" in icd_result and icd_result["explanations"]:
                    primary_explanation = icd_result["explanations"][0]
                if "doubts" in icd_result and icd_result["doubts"]:
                    primary_doubt = icd_result["doubts"][0]


            complete_icd_data = {
                "simplified": {
                    "code": primary_icd_code,
                    "explanation": primary_explanation,
                    "doubt": primary_doubt
                },
                # Store full result if needed later, but keep simplified for consistency
                # "full_result": icd_result # Optional: Store the raw result too
            }
        else:
            # Store error information if ICD classification failed
             complete_icd_data = {"error": icd_result.get("error", "ICD data unavailable")}


        cdt_json = json.dumps(complete_cdt_data)
        icd_json = json.dumps(complete_icd_data)

        db_data = {
            "user_question": scenario_data.get("original_scenario", "Missing original scenario"),
            "processed_clean_data": scenario_data.get("processed_scenario", "Missing processed scenario"),
            "cdt_result": cdt_json,
            "icd_result": icd_json
        }

        db_result_list = db.create_analysis_record(db_data)
        if db_result_list and isinstance(db_result_list, list) and len(db_result_list) > 0 and "id" in db_result_list[0]:
            record_id = db_result_list[0]["id"]
            print(f"✅ Data saved successfully with ID: {record_id}")
            return {"record_id": record_id, "status": "success", "cdt_data": complete_cdt_data, "icd_data": complete_icd_data}
        else:
            print(f"❌ Failed to save data to database or get ID back. DB response: {db_result_list}")
            return {"record_id": None, "status": "error", "message": "Failed to save data or retrieve valid record ID"}
    except Exception as e:
        print(f"❌ Database error during initial save: {str(e)}")
        error_details = traceback.format_exc()
        return {"record_id": None, "status": "error", "message": f"Database Save Error: {str(e)}", "details": error_details}

async def generate_questions_for_scenario(record_id: str, processed_scenario: str, cdt_data: dict, icd_data: dict) -> dict:
    """Step 4b: Generate questions using the Questioner module."""
    print(f"❓ Generating Questions for Record ID: {record_id}...")
    if not record_id or not processed_scenario:
         print(f"⚠️ Skipping question generation due to missing data (record_id: {record_id}, processed_scenario: {bool(processed_scenario)})")
         # Create a standard 'no questions' result structure but mark status as error
         no_question_result = {
             "cdt_questions": {"questions": [], "explanation": "Missing required data", "has_questions": False},
             "icd_questions": {"questions": [], "explanation": "Missing required data", "has_questions": False},
             "has_questions": False
         }
         return {
             "questioner_result": no_question_result,
             "status": "error",
             "message": "Missing record ID or processed scenario for question generation",
             "should_run_inspectors_immediately": False # Can't run inspectors without full context
         }
    try:
        # Format simplified data for the questioner
        simplified_cdt_data = {
            "code_ranges": cdt_data.get("cdt_classification", {}).get("range_codes_string", ""),
            "activated_subtopics": cdt_data.get("topics_results", {}).get("activated_subtopics", []),
            "subtopics": ", ".join(list(cdt_data.get("topics_results", {}).get("subtopic_data", {}).keys())) if cdt_data.get("topics_results", {}).get("subtopic_data") else "None",
             "formatted_cdt_results": [
                 f"{res.get('code_range')}: {res.get('explanation')}"
                 for res in cdt_data.get("cdt_classification", {}).get("CDT_classifier", [])
             ]
        }
        simplified_icd_data = icd_data.get("simplified", {"code": "", "explanation": "", "doubt": ""})

        # Ensure ICD data passed is not the error structure
        if "error" in simplified_icd_data:
             simplified_icd_data = {"code": "", "explanation": f"ICD Error: {simplified_icd_data['error']}", "doubt": ""}


        questioner_result = questioner.process(
            processed_scenario,
            simplified_cdt_data,
            simplified_icd_data
        )

        # Save questioner data to the database
        questioner_json = json.dumps(questioner_result)
        db.update_questioner_data(record_id, questioner_json)
        print(f"✅ Saved questioner data to DB for record ID: {record_id} (Has Questions: {questioner_result.get('has_questions', False)})")

        # Check if inspectors should run immediately (no questions generated)
        should_run_inspectors = not questioner_result.get("has_questions", False)

        return {
            "questioner_result": questioner_result,
            "status": "success",
            "should_run_inspectors_immediately": should_run_inspectors
         }

    except Exception as e:
        print(f"❌ Error in questioner processing for record {record_id}: {str(e)}")
        error_details = traceback.format_exc()
        # Create error state structure
        error_q_result = {
            "cdt_questions": {"questions": [], "explanation": f"Error occurred: {str(e)}", "has_questions": False},
            "icd_questions": {"questions": [], "explanation": f"Error occurred: {str(e)}", "has_questions": False},
            "has_questions": False,
            "error": f"Questioner Error: {str(e)}",
            "details": error_details
        }
        try:
             db.update_questioner_data(record_id, json.dumps(error_q_result))
             print(f"⚠️ Saved error state for questioner data for record ID: {record_id}")
        except Exception as db_e:
             print(f"❌ Failed to save questioner error state to DB for {record_id}: {db_e}")

        return {
            "questioner_result": error_q_result,
            "status": "error",
            "message": f"Questioner Error: {str(e)}",
            "details": error_details,
            "should_run_inspectors_immediately": False # Don't run inspectors if questioner failed
        }

async def run_inspectors_for_scenario(record_id: str) -> dict:
    """Step 5: Run CDT and ICD inspectors in parallel for a given record."""
    print(f"🕵️ Running Inspectors for Record ID: {record_id}...")
    if not record_id:
        return {"status": "error", "message": "Missing record ID for inspection"}
    try:
        # Use the refactored function
        inspector_run_result = await run_inspectors(record_id)

        # Get complete record data for response (similar to submit_question_answers)
        complete_data = db.get_complete_analysis(record_id)
        if not complete_data:
            return {"status": "error", "message": f"Failed to retrieve complete analysis for record ID: {record_id}"}

        # Parse JSON safely
        cdt_result = {}
        icd_result = {}
        questioner_data = {}
        final_inspector_results = {}
        try:
             cdt_result = json.loads(complete_data.get("cdt_result", "{}"))
             icd_result = json.loads(complete_data.get("icd_result", "{}"))
             questioner_data = json.loads(complete_data.get("questioner_data", "{}"))
             # Get inspector results from dedicated column first
             if complete_data.get('inspector_results'):
                 final_inspector_results = json.loads(complete_data['inspector_results'])
             elif inspector_run_result.get('status') == 'success': # Fallback
                  final_inspector_results = inspector_run_result
        except json.JSONDecodeError as e:
             print(f"❌ Error decoding JSON from DB on trigger_inspectors for {record_id}: {e}")
             # Handle error appropriately

        # Extract data for response structure
        cdt_classification = cdt_result.get("cdt_classification", {})
        topics_results = cdt_result.get("topics_results", {})
        icd_classification = icd_result.get("simplified", {})

        response_data = {
            "record_id": record_id,
            "processed_scenario": complete_data.get("processed_clean_data", ""),
            "cdt_classification": cdt_classification,
            "topics_results": topics_results,
            "icd_classification": icd_classification,
            "questioner_data": questioner_data,
            "inspector_results": final_inspector_results # From DB or the run result
        }

        # Check the status from the inspector run itself as well
        if inspector_run_result.get("status") != "success":
             print(f"⚠️ Inspector run triggered for {record_id} completed with status: {inspector_run_result.get('status')} - Message: {inspector_run_result.get('message')}")
             # The inspector_results in response_data might contain error details

        # Return success as the trigger endpoint worked, even if inspectors had issues internally
        return {"status": "success", "data": response_data}

    except Exception as e:
        error_details = traceback.format_exc()
        print(f"❌ ERROR triggering inspectors: {str(e)}")
        print(f"STACK TRACE: {error_details}")
        return {"status": "error", "message": str(e), "details": error_details}


# --- Existing Endpoints (Modified where needed) ---

@app.post("/api/analyze")
async def analyze_web(request: ScenarioRequest):
    """Process a single dental scenario using the refactored steps."""
    start_time = time.time()
    record_id = None # Initialize record_id
    final_status = "success" # Assume success initially
    error_message = None
    error_details = None

    try:
        # Step 1: Clean
        clean_result = await clean_scenario(request.scenario)
        if clean_result["status"] == "error":
            raise ValueError(f"Cleaning failed: {clean_result['message']}", clean_result.get("details"))
        processed_scenario = clean_result["processed_scenario"]

        # Step 2: Classify
        cdt_result, icd_result = await classify_scenario(processed_scenario)
        if cdt_result.get("status") == "error" or icd_result.get("status") == "error":
             error_msg = cdt_result.get("error") or icd_result.get("error", "Unknown classification error")
             details = cdt_result.get("details") or icd_result.get("details")
             raise ValueError(f"Classification failed: {error_msg}", details)

        # Step 3: Activate Topics
        topic_activation_result = await activate_topics_for_scenario(processed_scenario, cdt_result)
        if topic_activation_result["status"] == "error":
             raise ValueError(f"Topic Activation failed: {topic_activation_result['error']}", topic_activation_result.get("details"))

        # Step 4a: Save Initial Data
        initial_save_data = {
            "original_scenario": request.scenario,
            "processed_scenario": processed_scenario,
            "cdt_result": cdt_result,
            "icd_result": icd_result,
            "topic_activation_result": topic_activation_result,
            "status": "success" # Indicate previous steps were successful
        }
        save_result = await save_initial_data(initial_save_data)
        if save_result["status"] == "error":
            # Log the error but maybe continue to provide partial results? Or return error.
            print(f"⚠️ Database save failed for single request: {save_result['message']}")
            # Let's raise the error to be caught by the main handler
            raise ValueError(f"Database Save failed: {save_result['message']}", save_result.get("details"))

        record_id = save_result["record_id"]
        complete_cdt_data = save_result["cdt_data"] # Get the formatted data back
        complete_icd_data = save_result["icd_data"] # Get the formatted data back

        # Step 4b: Generate Questions
        question_gen_result = await generate_questions_for_scenario(
            record_id, processed_scenario, complete_cdt_data, complete_icd_data
        )
        questioner_result = question_gen_result["questioner_result"]
        if question_gen_result["status"] == "error":
             print(f"⚠️ Question generation failed for {record_id}: {question_gen_result['message']}")
             # Don't raise error, but store the questioner result containing the error info

        # Step 5: Run Inspectors (Conditionally)
        inspector_results = {"cdt": {}, "icd": {}, "status": "not_run"} # Default state
        if question_gen_result.get("should_run_inspectors_immediately"):
            print(f"✅ No questions generated for {record_id}, running inspectors immediately.")
            inspector_run_result = await run_inspectors_for_scenario(record_id)
            inspector_results = inspector_run_result # Contains status and results/errors
            if inspector_run_result.get("status") != "success":
                 print(f"⚠️ Inspector run failed for {record_id}: {inspector_run_result.get('message')}")
                 # Error details might be within inspector_results structure inside inspector_run_result_data


        # Step 6: Prepare final response
        # Consolidate data collected during the process
        response_data = {
            "record_id": record_id,
            "processed_scenario": processed_scenario,
            "cdt_classification": complete_cdt_data.get("cdt_classification", {}),
            "topics_results": complete_cdt_data.get("topics_results", {}),
            "icd_classification": complete_icd_data.get("simplified", {}),
            "questioner_data": questioner_result,
            "inspector_results": inspector_results.get("inspector_results") if isinstance(inspector_results, dict) and inspector_results.get("status") == "success" else inspector_results # Handle different shapes of inspector_results
        }

    except ValueError as ve: # Catch specific ValueErrors raised in steps
        final_status = "error"
        error_message = str(ve.args[0]) if ve.args else "Processing Error"
        error_details = ve.args[1] if len(ve.args) > 1 else None
        print(f"❌ ERROR in analyze_web step: {error_message}")
        if error_details: print(f"DETAILS: {error_details}")

    except Exception as e:
        final_status = "error"
        error_details = traceback.format_exc()
        error_message = f"Unexpected Error: {str(e)}"
        print(f"❌ UNHANDLED ERROR in analyze_web: {str(e)}")
        print(f"STACK TRACE: {error_details}")

    total_time = time.time() - start_time
    print(f"⏱️ TOTAL analyze_web TIME: {total_time:.2f} seconds (Status: {final_status})")

    if final_status == "success":
        return {"status": "success", "data": response_data}
    else:
         # Try to return error with record_id if available
        return {
            "status": "error",
            "record_id": record_id, # Include record_id if available
            "message": error_message,
            "details": error_details
        }


@app.get("/")
def test():
    return {"message": "Dental Code Extractor API is running"}

# Endpoint for submitting answers (should remain largely the same, but ensure run_inspectors call works)
@app.post("/api/answer-questions/{record_id}")
async def submit_question_answers(record_id: str, request: QuestionAnswersRequest):
    """Process the answers to questions and update the analysis."""
    try:
        print(f"\n*************************** PROCESSING ANSWERS FOR RECORD {record_id} ***************************")
        analysis = db.get_complete_analysis(record_id)
        if not analysis:
            return {"status": "error", "message": f"No analysis found with ID: {record_id}"}

        # Parse the answers JSON string safely
        try:
            answers = json.loads(request.answers)
        except json.JSONDecodeError:
             return {"status": "error", "message": "Invalid JSON format for answers"}

        # Parse existing questioner data safely
        try:
            questioner_data = json.loads(analysis.get("questioner_data", "{}"))
            if not isinstance(questioner_data, dict): # Basic check
                 raise ValueError("Questioner data is not a valid dictionary")
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error parsing existing questioner data for {record_id}: {e}")
            return {"status": "error", "message": "Invalid or missing questioner data found for this analysis"}

        # Add the answers to the questioner data
        questioner_data["answers"] = answers
        questioner_data["answered"] = True
        questioner_data["has_answers"] = True # Mark that answers are present

        # Update the database
        db.update_questioner_data(record_id, json.dumps(questioner_data))
        print(f"✅ Updated questioner data with answers for record ID: {record_id}")

        # Proceed to inspector step after answers are saved
        inspector_run_result = await run_inspectors_for_scenario(record_id)

        # Get the complete updated record data for response
        complete_data = db.get_complete_analysis(record_id)
        if not complete_data:
             return {"status": "error", "message": f"Failed to retrieve complete analysis for record ID: {record_id} after update"}

        # Parse all the necessary JSON data
        cdt_result = {}
        icd_result = {}
        updated_questioner_data = {}
        final_inspector_results = {}
        try:
             cdt_result = json.loads(complete_data.get("cdt_result", "{}"))
             icd_result = json.loads(complete_data.get("icd_result", "{}"))
             updated_questioner_data = json.loads(complete_data.get("questioner_data", "{}")) # Re-fetch updated data
             # Get inspector results from dedicated column first
             if complete_data.get('inspector_results'):
                 final_inspector_results = json.loads(complete_data['inspector_results'])
             # Fallback to result from the run if DB column is empty (e.g., if update failed or race condition)
             elif inspector_run_result.get('status') == 'success':
                  final_inspector_results = inspector_run_result
        except json.JSONDecodeError as e:
             print(f"❌ Error decoding JSON from DB after answering questions for {record_id}: {e}")
             # Handle error - perhaps return error or partial data

        # Extract data for response structure
        cdt_classification = cdt_result.get("cdt_classification", {})
        topics_results = cdt_result.get("topics_results", {})
        icd_classification = icd_result.get("simplified", {})

        response_data = {
            "record_id": record_id,
            "processed_scenario": complete_data.get("processed_clean_data", ""),
            "cdt_classification": cdt_classification,
            "topics_results": topics_results,
            "icd_classification": icd_classification,
            "questioner_data": updated_questioner_data,
            "inspector_results": final_inspector_results
        }

        return {"status": "success", "data": response_data}

    except Exception as e:
        error_details = traceback.format_exc()
        print(f"❌ ERROR processing answers: {str(e)}")
        print(f"STACK TRACE: {error_details}")
        return {"status": "error", "message": str(e), "details": error_details}


# Endpoint to run inspectors directly (can use the refactored function)
@app.get("/api/run-inspectors/{record_id}")
async def trigger_inspectors(record_id: str):
    """Run both CDT and ICD inspectors for a given record."""
    try:
        # Use the refactored function
        inspector_run_result = await run_inspectors_for_scenario(record_id)

        # Get complete record data for response (similar to submit_question_answers)
        complete_data = db.get_complete_analysis(record_id)
        if not complete_data:
            return {"status": "error", "message": f"Failed to retrieve complete analysis for record ID: {record_id}"}

        # Parse JSON safely
        cdt_result = {}
        icd_result = {}
        questioner_data = {}
        final_inspector_results = {}
        try:
             cdt_result = json.loads(complete_data.get("cdt_result", "{}"))
             icd_result = json.loads(complete_data.get("icd_result", "{}"))
             questioner_data = json.loads(complete_data.get("questioner_data", "{}"))
             # Get inspector results from dedicated column first
             if complete_data.get('inspector_results'):
                 final_inspector_results = json.loads(complete_data['inspector_results'])
             elif inspector_run_result.get('status') == 'success': # Fallback
                  final_inspector_results = inspector_run_result
        except json.JSONDecodeError as e:
             print(f"❌ Error decoding JSON from DB on trigger_inspectors for {record_id}: {e}")
             # Handle error appropriately

        # Extract data for response structure
        cdt_classification = cdt_result.get("cdt_classification", {})
        topics_results = cdt_result.get("topics_results", {})
        icd_classification = icd_result.get("simplified", {})

        response_data = {
            "record_id": record_id,
            "processed_scenario": complete_data.get("processed_clean_data", ""),
            "cdt_classification": cdt_classification,
            "topics_results": topics_results,
            "icd_classification": icd_classification,
            "questioner_data": questioner_data,
            "inspector_results": final_inspector_results # From DB or the run result
        }

        # Check the status from the inspector run itself as well
        if inspector_run_result.get("status") != "success":
             print(f"⚠️ Inspector run triggered for {record_id} completed with status: {inspector_run_result.get('status')} - Message: {inspector_run_result.get('message')}")
             # The inspector_results in response_data might contain error details

        # Return success as the trigger endpoint worked, even if inspectors had issues internally
        return {"status": "success", "data": response_data}

    except Exception as e:
        error_details = traceback.format_exc()
        print(f"❌ ERROR triggering inspectors: {str(e)}")
        print(f"STACK TRACE: {error_details}")
        return {"status": "error", "message": str(e), "details": error_details}


# Existing run_inspectors function (Core logic - called by run_inspectors_for_scenario)
async def run_inspectors(record_id: str):
    """Core logic to run CDT and ICD inspectors in parallel for a given record."""
    print(f"\n*************************** RUNNING INSPECTORS (Core Logic) FOR RECORD {record_id} ***************************")
    inspector_results = {} # Initialize structure for results

    try:
        # Get the required data from the database
        analysis = db.get_complete_analysis(record_id)
        if not analysis:
            raise ValueError(f"No analysis found with ID: {record_id}")

        processed_scenario = analysis.get("processed_clean_data", "")
        questioner_data = {}
        cdt_data_from_db = {}
        icd_data_from_db = {}

        try:
             questioner_data = json.loads(analysis.get("questioner_data", "{}"))
             cdt_data_from_db = json.loads(analysis.get("cdt_result", "{}"))
             icd_data_from_db = json.loads(analysis.get("icd_result", "{}"))
        except json.JSONDecodeError as e:
             raise ValueError(f"Failed to parse stored JSON data for record {record_id}: {e}")

        # Check if we need to proceed with inspectors
        # Use 'has_answers' flag if available, otherwise assume answered if not 'has_questions'
        answered = questioner_data.get("has_answers", not questioner_data.get("has_questions", False))
        if questioner_data.get("has_questions", False) and not answered:
            print("⚠️ Questions exist but have not been answered yet - skipping inspectors")
            return {
                "status": "pending_answers",
                "message": "Questions need to be answered before running inspectors",
                "inspector_results": None # No results generated
            }

        # Format data for CDT inspector
        cdt_topic_analysis = {}
        if cdt_data_from_db and "topics_results" in cdt_data_from_db:
            topic_results = cdt_data_from_db["topics_results"]
            if "subtopic_data" in topic_results and isinstance(topic_results["subtopic_data"], dict):
                all_candidate_codes = []
                for subtopic_key, codes in topic_results["subtopic_data"].items():
                    formatted_codes = []
                    for code_entry in codes:
                        code = code_entry.get("code", "")
                        explanation = code_entry.get("explanation", "")
                        doubt = code_entry.get("doubt", "")
                        if code and code.lower() != 'none' and code != 'Unknown':
                            # Clean the code value if needed
                            if isinstance(code, str):
                                if " - " in code: code = code.split(" - ")[0].strip()
                            all_candidate_codes.append(code) # Add to candidate list

                        formatted_code = f"CODE: {code}\nEXPLANATION: {explanation}"
                        if doubt: formatted_code += f"\nDOUBT: {doubt}"
                        formatted_codes.append(formatted_code)

                    formatted_result = "\n\n".join(formatted_codes)
                    cdt_topic_analysis[subtopic_key] = {"name": subtopic_key, "result": formatted_result}

                # Add a special entry for all candidate codes
                if all_candidate_codes:
                    cdt_topic_analysis["_all_candidate_codes"] = {
                        "name": "All Candidate Codes",
                        "result": "CODES: " + ", ".join(list(set(all_candidate_codes))) # Use set for uniqueness
                    }

        # Format data for ICD inspector
        icd_topic_analysis = {}
        if icd_data_from_db and "simplified" in icd_data_from_db:
            simplified = icd_data_from_db["simplified"]
            if simplified and "error" not in simplified: # Check if ICD was successful
                icd_topic_analysis["1"] = {
                    "name": "Primary ICD Code",
                    "result": f"CODE: {simplified.get('code', '')}\nEXPLANATION: {simplified.get('explanation', '')}\nDOUBT: {simplified.get('doubt', '')}",
                    "parsed_result": simplified # Pass the dictionary directly
                }
            else:
                 print(f"⚠️ Skipping ICD inspection for {record_id} due to ICD classification error.")


        # Define async functions for parallel execution
        async def run_cdt_inspector_task():
            print("⏳ Running CDT Inspector...")
            try:
                return cdt_inspector.process(processed_scenario, cdt_topic_analysis, questioner_data)
            except Exception as e_cdt:
                print(f"❌ Error in CDT inspector: {str(e_cdt)}")
                return {"error": str(e_cdt), "codes": [], "rejected_codes": [], "explanation": f"Error occurred: {str(e_cdt)}"}

        async def run_icd_inspector_task():
            # Only run if we have valid data for it
            if not icd_topic_analysis:
                 return {"status": "skipped", "codes": [], "explanation": "Skipped due to previous ICD error"}
            print("⏳ Running ICD Inspector...")
            try:
                return icd_inspector.process(processed_scenario, icd_topic_analysis, questioner_data)
            except Exception as e_icd:
                print(f"❌ Error in ICD inspector: {str(e_icd)}")
                return {"error": str(e_icd), "codes": [], "explanation": f"Error occurred: {str(e_icd)}"}

        # Run both inspectors in parallel
        cdt_inspector_task = asyncio.create_task(run_cdt_inspector_task())
        icd_inspector_task = asyncio.create_task(run_icd_inspector_task())
        cdt_inspector_result, icd_inspector_result = await asyncio.gather(cdt_inspector_task, icd_inspector_task)

        # Log the results
        cdt_codes = cdt_inspector_result.get("codes", [])
        icd_codes = icd_inspector_result.get("codes", [])
        print(f"✅ CDT INSPECTOR COMPLETE - Found {len(cdt_codes)} validated codes for {record_id}")
        print(f"✅ ICD INSPECTOR COMPLETE - Found {len(icd_codes)} validated codes for {record_id}")

        # Combine results
        inspector_results = {
            "cdt": cdt_inspector_result,
            "icd": icd_inspector_result,
            "timestamp": str(datetime.datetime.now())
        }

        # Save inspector results to the dedicated column
        db.update_inspector_results(record_id, json.dumps(inspector_results))
        print(f"✅ Saved combined inspector results to database for record ID: {record_id}")

        # For backward compatibility, also update the existing fields if needed (can be removed later)
        # cdt_data_from_db["inspector_results"] = cdt_inspector_result
        # icd_data_from_db["inspector_results"] = icd_inspector_result
        # db.update_analysis_results(record_id, json.dumps(cdt_data_from_db), json.dumps(icd_data_from_db))

        return {"status": "success", "inspector_results": inspector_results}

    except Exception as e:
        print(f"❌ Error inside core run_inspectors for record {record_id}: {str(e)}")
        error_details = traceback.format_exc()
        # Structure the error response
        error_result = {
                "cdt": {"error": str(e), "codes": [], "rejected_codes": [], "explanation": f"Core Inspector Error: {str(e)}"},
                "icd": {"error": str(e), "codes": [], "explanation": f"Core Inspector Error: {str(e)}"},
                "timestamp": str(datetime.datetime.now())
            }
        # Try to save error state to DB
        try:
             db.update_inspector_results(record_id, json.dumps({"error": str(e), "details": error_details, **error_result}))
             print(f"⚠️ Saved error state for inspector results (core failure) for record ID: {record_id}")
        except Exception as db_e:
             print(f"❌ Failed to save inspector error state (core failure) to DB for {record_id}: {db_e}")

        return {"status": "error", "message": f"Core Inspector Error: {str(e)}", "details": error_details, "inspector_results": error_result}


# Endpoint for adding custom codes
@app.post("/api/add-custom-code")
async def add_custom_code(request: CustomCodeRequest):
    """Process and add a custom code for a given scenario."""
    try:
        print(f"\n*************************** ADDING CUSTOM CODE FOR RECORD {request.record_id} ***************************")
        print(f"Custom code: {request.code}")
        print(f"Scenario: {request.scenario}")
        
        # Run the custom code analysis
        analysis_result = Add_code_data(request.scenario, request.code)
        
        # Get the existing analysis from the database
        analysis = db.get_complete_analysis(request.record_id)
        if not analysis:
            return {
                "status": "error",
                "message": f"No analysis found with ID: {request.record_id}"
            }
            
        # Parse the analysis result to extract components
        explanation = ""
        doubt = "None"
        
        # Extract explanation and doubt from the analysis result
        if "Explanation:" in analysis_result:
            explanation = analysis_result.split("Explanation:")[1].strip()
            if "Doubt:" in explanation:
                parts = explanation.split("Doubt:")
                explanation = parts[0].strip()
                doubt = parts[1].strip()
        else:
            explanation = analysis_result
            
        # Check if the code is likely applicable based on the analysis result
        is_applicable = "Applicable? Yes" in analysis_result
        
        # Format the response in the expected structure
        code_data = {
            "code": request.code,
            "explanation": explanation,
            "doubt": doubt,
            "isApplicable": is_applicable
        }
        
        return {
            "status": "success",
            "message": "Custom code analysis completed",
            "data": {
                "code_data": code_data,
                "inspector_results": {
                    "cdt": {
                        "codes": [request.code] if is_applicable else [],
                        "rejected_codes": [] if is_applicable else [request.code],
                        "explanation": explanation
                    },
                    "icd": {
                        "codes": [],
                        "explanation": ""
                    }
                }
            }
        }
        
    except Exception as e:
        error_details = traceback.format_exc()
        print(f"❌ ERROR adding custom code: {str(e)}")
        print(f"STACK TRACE: {error_details}")
        return {"status": "error", "message": str(e), "details": error_details}


# Endpoint for storing code status (Manual user override)
@app.post("/api/store-code-status")
async def store_code_status(request: CodeStatusRequest):
    """Store the final status of selected and rejected codes based on user input."""
    try:
        print(f"\n*************************** STORING CODE STATUS FOR RECORD {request.record_id} ***************************")
        print(f"Selected CDT codes: {request.cdt_codes}")
        print(f"Selected ICD codes: {request.icd_codes}")
        print(f"Rejected CDT codes: {request.rejected_cdt_codes}")
        print(f"Rejected ICD codes: {request.rejected_icd_codes}") # Assuming frontend sends this

        # Get the existing analysis from the database
        analysis = db.get_complete_analysis(request.record_id)
        if not analysis:
            return {"status": "error", "message": f"No analysis found with ID: {request.record_id}"}

        # Get the inspector results or create new structure
        inspector_results = {}
        try:
             if analysis.get("inspector_results"):
                  inspector_results = json.loads(analysis["inspector_results"])
        except json.JSONDecodeError:
              print(f"Warning: Could not parse existing inspector results for {request.record_id} during status store. Overwriting.")
              inspector_results = {} # Start fresh if parsing failed

        # Ensure base structure exists
        if "cdt" not in inspector_results: inspector_results["cdt"] = {}
        if "icd" not in inspector_results: inspector_results["icd"] = {}

        # Update the inspector results with user selections
        inspector_results["cdt"]["codes"] = request.cdt_codes
        inspector_results["cdt"]["rejected_codes"] = request.rejected_cdt_codes
        
        inspector_results["icd"]["codes"] = request.icd_codes
        # Add rejected ICD if provided by request model
        inspector_results["icd"]["rejected_codes"] = request.rejected_icd_codes

        # Add a timestamp and source indicator
        inspector_results["timestamp"] = str(datetime.datetime.now())
        inspector_results["updated_by"] = "user_selection"

        # Update the database
        db.update_inspector_results(request.record_id, json.dumps(inspector_results))

        # Update the CDT and ICD results for backward compatibility (Optional - can remove later)
        # try:
        #     cdt_result = json.loads(analysis.get("cdt_result", "{}"))
        #     icd_result = json.loads(analysis.get("icd_result", "{}"))
        #     cdt_result["inspector_results"] = inspector_results["cdt"] # Store only CDT part
        #     icd_result["inspector_results"] = inspector_results["icd"] # Store only ICD part
        #     db.update_analysis_results(request.record_id, json.dumps(cdt_result), json.dumps(icd_result))
        # except Exception as legacy_e:
        #      print(f"Warning: Failed to update legacy CDT/ICD results for {request.record_id}: {legacy_e}")

        print(f"✅ Code status updated in the database")

        return {
            "status": "success",
            "message": "Code status updated successfully",
            "inspector_results": inspector_results # Return the final structure
        }

    except Exception as e:
        error_details = traceback.format_exc()
        print(f"❌ ERROR storing code status: {str(e)}")
        print(f"STACK TRACE: {error_details}")
        return {"status": "error", "message": str(e), "details": error_details}


# --- REWRITTEN BATCH ENDPOINT ---
@app.post("/api/analyze-batch")
async def analyze_batch(request: BatchScenarioRequest):
    """Process multiple dental scenarios concurrently across steps."""
    batch_start_time = time.time()
    num_scenarios = len(request.scenarios)
    print(f"\n*************************** PROCESSING BATCH OF {num_scenarios} SCENARIOS CONCURRENTLY ***************************")

    # Set a reasonable concurrency limit (adjust as needed based on resources/API limits)
    max_concurrent_tasks = 5 # Limit simultaneous calls to external APIs / heavy CPU tasks
    semaphore = asyncio.Semaphore(max_concurrent_tasks)

    # Dictionary to store results for each scenario by index
    results_dict = {i: {"original_scenario": s} for i, s in enumerate(request.scenarios)}

    async def process_single_scenario_pipeline(index: int, scenario: str):
        """Runs the full pipeline for one scenario, managing state in results_dict."""
        nonlocal results_dict
        step_start_time = time.time()
        print(f"Batch [{index+1}/{num_scenarios}] START")
        current_result = results_dict[index] # Work on the dictionary for this index

        try:
            # --- Step 1: Clean ---
            # Semaphore might not be strictly needed here unless cleaner uses external API heavily
            # async with semaphore:
            clean_result = await clean_scenario(scenario)
            current_result.update(clean_result)
            if clean_result["status"] == "error":
                print(f"Batch [{index+1}] FAIL (Clean)")
                current_result["final_status"] = "error"
                return # Stop processing this scenario

            processed_scenario = clean_result["processed_scenario"]

            # --- Step 2: Classify ---
            async with semaphore: # Classification uses external APIs
                 cdt_result, icd_result = await classify_scenario(processed_scenario)
            current_result["cdt_result"] = cdt_result
            current_result["icd_result"] = icd_result
            if cdt_result.get("status") == "error" or icd_result.get("status") == "error":
                print(f"Batch [{index+1}] FAIL (Classify)")
                current_result["final_status"] = "error"
                current_result["message"] = cdt_result.get("error") or icd_result.get("error", "Classification failed")
                current_result["details"] = cdt_result.get("details") or icd_result.get("details")
                return

            # --- Step 3: Activate Topics ---
            async with semaphore: # Topic activation uses external APIs
                topic_activation_result = await activate_topics_for_scenario(processed_scenario, cdt_result)
            current_result["topic_activation_result"] = topic_activation_result
            if topic_activation_result["status"] == "error":
                 print(f"Batch [{index+1}] FAIL (Topics)")
                 current_result["final_status"] = "error"
                 current_result["message"] = topic_activation_result.get("error")
                 current_result["details"] = topic_activation_result.get("details")
                 return

            # --- Step 4a: Save Initial Data ---
            # Pass the current state of the result dict for this scenario
            save_result = await save_initial_data(current_result)
            current_result.update(save_result) # Adds record_id, status, cdt_data, icd_data
            if save_result["status"] == "error":
                 print(f"Batch [{index+1}] FAIL (Save)")
                 current_result["final_status"] = "error"
                 # Message/details are already in save_result from the function
                 return

            record_id = save_result["record_id"]
            complete_cdt_data = save_result["cdt_data"] # Use the structured data returned
            complete_icd_data = save_result["icd_data"]

            # --- Step 4b: Generate Questions ---
            async with semaphore: # Questioner might call external API
                 question_gen_result = await generate_questions_for_scenario(
                     record_id, processed_scenario, complete_cdt_data, complete_icd_data
                 )
            current_result["questioner_result"] = question_gen_result["questioner_result"]
            current_result["should_run_inspectors_immediately"] = question_gen_result.get("should_run_inspectors_immediately", False)

            if question_gen_result["status"] == "error":
                 print(f"Batch [{index+1}] WARN (Questions failed: {question_gen_result.get('message')})")
                 current_result["questioner_error"] = question_gen_result.get("message")
                 # Continue processing, but inspectors won't run immediately if needed

            # --- Step 5: Run Inspectors (Conditionally and Immediately) ---
            inspector_run_result_data = {"status": "not_run"} # Default state
            if current_result.get("should_run_inspectors_immediately") and current_result.get("final_status") != "error":
                 print(f"Batch [{index+1}] Running Inspectors Immediately...")
                 async with semaphore: # Inspectors call external APIs
                     inspector_run_result_data = await run_inspectors_for_scenario(record_id)
                 current_result["inspector_run_result"] = inspector_run_result_data # Store the raw result from the run
                 if inspector_run_result_data.get("status") != "success":
                      print(f"Batch [{index+1}] WARN (Inspectors failed: {inspector_run_result_data.get('message')})")
                      # Error details might be within inspector_results structure inside inspector_run_result_data

            # Store the actual inspector results payload (or error state)
            current_result["inspector_results"] = inspector_run_result_data.get("inspector_results") if isinstance(inspector_run_result_data, dict) else inspector_run_result_data


            # --- Mark as Success (if no errors encountered during critical steps) ---
            if current_result.get("final_status") != "error":
                current_result["final_status"] = "success"
                print(f"Batch [{index+1}/{num_scenarios}] END OK ({time.time() - step_start_time:.2f}s)")
            else:
                 # Ensure final_status reflects the error if one occurred
                 print(f"Batch [{index+1}/{num_scenarios}] END FAIL ({time.time() - step_start_time:.2f}s)")


        except Exception as e:
            print(f"Batch [{index+1}] FAIL (Unhandled Exception: {str(e)})")
            error_details = traceback.format_exc()
            current_result.update({
                "final_status": "error",
                "message": f"Unhandled Batch Pipeline Error: {str(e)}",
                "details": error_details
            })
            # Ensure update is reflected
            results_dict[index] = current_result


    # Create and run tasks for each scenario using the pipeline function
    tasks = [process_single_scenario_pipeline(i, s) for i, s in enumerate(request.scenarios)]
    await asyncio.gather(*tasks)

    # Format the final response list from the results_dict
    final_batch_results = []
    for i in range(num_scenarios):
        result = results_dict[i]
        response_item = {
            "status": result.get("final_status", "error"), # Overall status for this scenario
            "original_scenario": result.get("original_scenario"),
            "record_id": result.get("record_id"),
            "message": result.get("message"), # Capture primary error messages if status is error
             "data": None
        }

        if response_item["status"] == "success":
             # Structure successful data similar to analyze_web response
             cdt_data = result.get("cdt_data", {}) # From save step
             icd_data = result.get("icd_data", {}) # From save step
             response_item["data"] = {
                 "record_id": result.get("record_id"),
                 "processed_scenario": result.get("processed_scenario"),
                 "cdt_classification": cdt_data.get("cdt_classification", {}),
                 "topics_results": cdt_data.get("topics_results", {}),
                 "icd_classification": icd_data.get("simplified", {}),
                 "questioner_data": result.get("questioner_result"), # Might contain error info if that step failed but others succeeded
                 "inspector_results": result.get("inspector_results") # May be empty/None if not run or failed
             }
        # Always include details if available, especially for errors
        if result.get("details"):
             response_item["details"] = result.get("details")
        # Include questioner error specifically if it occurred but didn't fail the whole process
        if result.get("questioner_error"):
             response_item["questioner_error"] = result.get("questioner_error")


        final_batch_results.append(response_item)


    total_batch_time = time.time() - batch_start_time
    print(f"\n*************************** BATCH PROCESSING COMPLETE ({total_batch_time:.2f} seconds) ***************************")

    return {
        "status": "success", # Batch endpoint itself succeeded in orchestrating tasks
        "batch_results": final_batch_results # Individual results indicate success/failure per scenario
    }


# Run the application
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")

    print("\n*************************** STARTING SERVER ***************************")
    print(f"🚀 SERVER RUNNING at {host}:{port}")
    # Consider disabling reload=True in production environments
    uvicorn.run("app:app", host=host, port=port, reload=True)