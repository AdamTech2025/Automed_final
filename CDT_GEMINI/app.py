from fastapi import FastAPI, HTTPException, Depends, status, UploadFile, File
from pydantic import BaseModel, EmailStr
import uvicorn
import logging
import os
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from typing import Dict, Any, List, Optional
import json
from fastapi.responses import JSONResponse
from werkzeug.utils import secure_filename
import openai

# Import helper functions from extractor
from extractor import (
    extract_text_from_txt,
    extract_text_from_pdf,
    extract_text_from_image,
    extract_text_from_audio,
    allowed_file,
    check_char_limit,
    split_into_scenarios,
    UPLOAD_FOLDER,
    ALLOWED_EXTENSIONS,
    MAX_CHAR_LIMIT
)

# Import the data cleaner
from data_cleaner import DentalScenarioProcessor

# Import Classifiers
from cdt_classifier import CDTClassifier
from icd_classifier import ICDClassifier

# Import Authentication Router and Dependency
from auth.auth_routes import router as auth_router
from auth.auth_utils import get_current_user, require_admin_role

# Import Topic Activation components
from sub_topic_registry import SubtopicRegistry

# Import Database class
from database import MedicalCodingDB

# Import Questioner
from questioner import Questioner

# Import Inspectors
from inspector import DentalInspector
from icd_inspector import ICDInspector

# Import Subtopic Parser
from subtopic import dental_manager

# CDT Topics
from topics.diagnostics import diagnostic_service
from topics.preventive import preventive_service
from topics.restorative import restorative_service
from topics.endodontics import endodontic_service
from topics.periodontics import periodontic_service
from topics.prosthodonticsremovable import prosthodontics_service as prostho_remov_service # Alias needed
from topics.maxillofacialprosthetics import maxillofacial_service
from topics.implantservices import implant_service
from topics.prosthodonticsfixed import prosthodontics_service as prostho_fixed_service # Alias needed
from topics.oralandmaxillofacialsurgery import oral_surgery_service
from topics.orthodontics import orthodontic_service
from topics.adjunctivegeneralservices import adjunctive_general_services_service

# ICD Topics
from icdtopics.disordersofpulpandperiapicaltissues import disorders_of_pulp_and_periapical_tissues_service
from icdtopics.dentalencounters import dental_encounter_service
from icdtopics.disordersofteeth import disorders_of_teeth_service
from icdtopics.dentalcaries import dental_caries_service
from icdtopics.diseasesandconditionsoftheperiodontium import diseases_and_conditions_of_the_periodontium_service
from icdtopics.alveolarridgedisorders import alveolar_ridge_disorders_service
from icdtopics.findingsofbostteeth import findings_bost_teeth_service
from icdtopics.developmentdisordersofteethandjaws import development_disorders_service
from icdtopics.treatmentcomplications import treatment_complications_service
from icdtopics.inflammatoryconditionsofthmucosa import inflammatory_conditions_mucosa_service
from icdtopics.tmjdiseasesandconditions import tmj_diseases_conditions_service
from icdtopics.breathingspeechandsleepdisorders import breathing_sleep_disorders_service
from icdtopics.traumaandrelatedconditions import trauma_related_conditions_service
from icdtopics.oralneoplasms import oral_neoplasms_service
from icdtopics.pathologies import pathologies_service
from icdtopics.medicalfindingsrelatedtodentaltreatment import medical_findings_dental_treatment_service
from icdtopics.socialdeterminants import social_determinants_service
from icdtopics.symptomsanddisorderspertienttoorthodontiacases import symptoms_and_disorders_orthodontics_service

# Import Add Code functionality
from add_codes.add_code_data import Add_code_data

# Import Traceback for detailed error logging
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
logger = logging.getLogger("uvicorn.error") # USE UVICORN'S LOGGER

# Silence httpx INFO logs
logging.getLogger("httpx").setLevel(logging.WARNING)

app = FastAPI(
    title="Dental Scenario Analysis API - Step 1: Cleaning & Auth",
    description="API for cleaning dental scenarios, with authentication.",
    version="0.1.0"
)

# Add CORS middleware
origins = [
    "http://localhost:5173",
    "https://dentalcoder.vercel.app",
    "https://automed.adamtechnologies.in",
    "http://automed.adamtechnologies.in",
    os.getenv("FRONTEND_URL", "")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Authentication Routes
app.include_router(auth_router)

# Initialize processors
scenario_processor = DentalScenarioProcessor()
cdt_classifier = CDTClassifier()       # Initialize CDT Classifier
icd_classifier = ICDClassifier()       # Initialize ICD Classifier

# Initialize Topic Registry (Combined CDT & ICD)
topic_registry = SubtopicRegistry()

# Initialize Database Connection
db = MedicalCodingDB()

# Initialize Questioner & Inspectors
questioner = Questioner()
cdt_inspector = DentalInspector()
icd_inspector = ICDInspector()

# --- CDT Topic Mapping and Registration ---
CDT_TOPIC_MAPPING = {
    "D0100-D0999": {"func": diagnostic_service.activate_diagnostic, "name": "Diagnostic"},
    "D1000-D1999": {"func": preventive_service.activate_preventive, "name": "Preventive"},
    "D2000-D2999": {"func": restorative_service.activate_restorative, "name": "Restorative"},
    "D3000-D3999": {"func": endodontic_service.activate_endodontic, "name": "Endodontics"},
    "D4000-D4999": {"func": periodontic_service.activate_periodontic, "name": "Periodontics"},
    "D5000-D5899": {"func": prostho_remov_service.activate_prosthodontics_removable, "name": "Prosthodontics Removable"},
    "D5900-D5999": {"func": maxillofacial_service.activate_maxillofacial_prosthetics, "name": "Maxillofacial Prosthetics"},
    "D6000-D6199": {"func": implant_service.activate_implant_services, "name": "Implant Services"},
    "D6200-D6999": {"func": prostho_fixed_service.activate_prosthodontics_fixed, "name": "Prosthodontics Fixed"},
    "D7000-D7999": {"func": oral_surgery_service.activate_oral_maxillofacial_surgery, "name": "Oral and Maxillofacial Surgery"},
    "D8000-D8999": {"func": orthodontic_service.activate_orthodontic, "name": "Orthodontics"},
    "D9000-D9999": {"func": adjunctive_general_services_service.activate_adjunctive_general_services, "name": "Adjunctive General Services"}
}
for code_range, topic_info in CDT_TOPIC_MAPPING.items():
    topic_registry.register(code_range, topic_info["func"], topic_info["name"])

# --- ICD Topic Mapping and Registration ---
ICD_CATEGORY_NAMES = {
    "1": "Dental Encounters", "2": "Dental Caries", "3": "Disorders of Teeth",
    "4": "Disorders of Pulp and Periapical Tissues", "5": "Diseases and Conditions of the Periodontium",
    "6": "Alveolar Ridge Disorders", "7": "Findings of BOST Teeth",
    "8": "Developmental Disorders of Teeth and Jaws", "9": "Treatment Complications",
    "10": "Inflammatory Conditions of the Mucosa", "11": "TMJ Diseases and Conditions",
    "12": "Breathing, Speech, and Sleep Disorders", "13": "Trauma and Related Conditions",
    "14": "Oral Neoplasms", "15": "Pathologies", "16": "Medical Findings Related to Dental Treatment",
    "17": "Social Determinants", "18": "Symptoms and Disorders Pertinent to Orthodontic Cases"
}

ICD_TOPIC_MAPPING = {
    "1": {"func": dental_encounter_service.activate_dental_encounter, "name": ICD_CATEGORY_NAMES["1"]},
    "2": {"func": dental_caries_service.activate_dental_caries, "name": ICD_CATEGORY_NAMES["2"]},
    "3": {"func": disorders_of_teeth_service.activate_disorders_of_teeth, "name": ICD_CATEGORY_NAMES["3"]},
    "4": {"func": disorders_of_pulp_and_periapical_tissues_service.activate_disorders_of_pulp_and_periapical_tissues, "name": ICD_CATEGORY_NAMES["4"]},
    "5": {"func": diseases_and_conditions_of_the_periodontium_service.activate_diseases_and_conditions_of_the_periodontium, "name": ICD_CATEGORY_NAMES["5"]},
    "6": {"func": alveolar_ridge_disorders_service.activate_alveolar_ridge_disorders, "name": ICD_CATEGORY_NAMES["6"]},
    "7": {"func": findings_bost_teeth_service.activate_findings_of_bost_teeth, "name": ICD_CATEGORY_NAMES["7"]},
    "8": {"func": development_disorders_service.activate_development_disorders_of_teeth_and_jaws, "name": ICD_CATEGORY_NAMES["8"]},
    "9": {"func": treatment_complications_service.activate_treatment_complications, "name": ICD_CATEGORY_NAMES["9"]},
    "10": {"func": inflammatory_conditions_mucosa_service.activate_inflammatory_conditions_of_the_mucosa, "name": ICD_CATEGORY_NAMES["10"]},
    "11": {"func": tmj_diseases_conditions_service.activate_tmj_diseases_and_conditions, "name": ICD_CATEGORY_NAMES["11"]},
    "12": {"func": breathing_sleep_disorders_service.activate_breathing_sleep_disorders, "name": ICD_CATEGORY_NAMES["12"]},
    "13": {"func": trauma_related_conditions_service.activate_trauma_and_related_conditions, "name": ICD_CATEGORY_NAMES["13"]},
    "14": {"func": oral_neoplasms_service.activate_oral_neoplasms, "name": ICD_CATEGORY_NAMES["14"]},
    "15": {"func": pathologies_service.activate_pathologies, "name": ICD_CATEGORY_NAMES["15"]},
    "16": {"func": medical_findings_dental_treatment_service.activate_medical_findings_related_to_dental_treatment, "name": ICD_CATEGORY_NAMES["16"]},
    "17": {"func": social_determinants_service.activate_social_determinants, "name": ICD_CATEGORY_NAMES["17"]},
    "18": {"func": symptoms_and_disorders_orthodontics_service.activate_symptoms_and_disorders_pertinent_to_orthodontic_cases, "name": ICD_CATEGORY_NAMES["18"]}
}

# Register ICD topics using category number as the key
for category_num, topic_info in ICD_TOPIC_MAPPING.items():
    topic_registry.register(category_num, topic_info["func"], topic_info["name"])

# --- Request Models ---
class ScenarioInput(BaseModel):
    scenario: str

class CleanedScenarioOutput(BaseModel):
    original_scenario: str
    cleaned_scenario: str
    standardized_scenario: str
    details: dict

class AnalysisStep2Output(BaseModel):
    original_scenario: str
    cleaned_scenario: str 
    standardized_scenario: str
    cdt_classification_results: Dict[str, Any]
    icd_classification_results: Dict[str, Any]

class AnalysisStep3Output(AnalysisStep2Output):
    cdt_topic_activation_results: List[Dict[str, Any]]
    icd_topic_activation_results: Dict[str, Any] 

class AnalysisStep4Output(AnalysisStep3Output):
    record_id: str

class AnalysisStep6Output(AnalysisStep4Output):
    questioner_data: Dict[str, Any]
    inspector_results: Dict[str, Any]

# Request models from app.txt
class CustomCodeRequest(BaseModel):
    code: str
    scenario: str # Need the original scenario for Add_code_data
    record_id: str # Might be useful for context

class CodeStatusRequest(BaseModel):
    record_id: str
    cdt_codes: List[str] = []
    icd_codes: List[str] = []
    rejected_cdt_codes: List[str] = []
    rejected_icd_codes: List[str] = []

# --- User Activity Response Model ---
class UserDetails(BaseModel):
    id: str
    name: str
    email: EmailStr
    phone: Optional[str]
    is_email_verified: bool
    created_at: Optional[str] # Assuming it comes as string from DB
    role: str # Add role

class AnalysisSummary(BaseModel):
    id: str
    user_question: Optional[str]
    created_at: Optional[str]

class UserActivityResponse(BaseModel):
    user_details: UserDetails
    analysis_count: int
    analyses: List[AnalysisSummary]

# --- Admin Response Models ---
class AdminUserSummary(UserDetails): # Inherits fields from UserDetails
    analysis_count: int

class AllUsersActivityResponse(BaseModel):
    users: List[AdminUserSummary]

# --- End Request Models ---

# File upload response model
class FileUploadResponse(BaseModel):
    message: str
    filename: str
    scenarios: List[str]

@app.post("/api/upload", response_model=FileUploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """
    Handles file upload, extracts text, splits into scenarios using AI,
    and returns the scenarios as JSON.
    """
    logging.info("Received request to /upload endpoint.")
    
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")

    if not allowed_file(file.filename):
        raise HTTPException(
            status_code=400, 
            detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    # Create upload folder if it doesn't exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    extracted_text = None

    try:
        # Save uploaded file
        logging.info(f"Saving uploaded file: {filename} to {file_path}")
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        file_type = filename.rsplit('.', 1)[1].lower()

        # --- Text Extraction ---
        logging.info(f"Starting text extraction for file type: {file_type}")
        if file_type == 'txt':
            extracted_text = extract_text_from_txt(file_path)
        elif file_type == 'pdf':
            extracted_text = extract_text_from_pdf(file_path)
        elif file_type in ['png', 'jpg', 'jpeg']:
            extracted_text = extract_text_from_image(file_path)
        elif file_type in ['mp3', 'wav']:
            extracted_text = extract_text_from_audio(file_path)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type for processing")

        # --- Character Limit Check ---
        check_char_limit(extracted_text or "")

        # --- AI Scenario Splitting ---
        logging.info("Calling AI scenario splitting function...")
        scenarios = split_into_scenarios(extracted_text)

        logging.info(f"Successfully processed file {filename}. Returning {len(scenarios)} scenarios.")
        
        return FileUploadResponse(
            message='File successfully processed.',
            filename=filename,
            scenarios=scenarios
        )

    except ValueError as ve:
        logging.error(f"Configuration or Value Error during processing: {ve}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(ve))
    
    except (IOError, ConnectionError) as file_err:
        logging.error(f"File Processing or Connection Error: {file_err}", exc_info=True)
        err_msg = f'Error communicating with external API: {str(file_err)}' if isinstance(file_err, ConnectionError) else f'Error processing file: {str(file_err)}'
        raise HTTPException(status_code=500, detail=err_msg)
    
    except openai.OpenAIError as oai_err:
        logging.error(f"OpenAI API Error: {oai_err}", exc_info=True)
        raise HTTPException(status_code=502, detail=f'An API error occurred with OpenAI: {str(oai_err)}')
    
    except Exception as e:
        logging.error(f"Unexpected server error during upload processing: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail='An unexpected server error occurred.')

    finally:
        # --- Cleanup ---
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                logging.info(f"Temporary file removed: {file_path}")
            except Exception as e_rem:
                logging.error(f"Error removing temporary file {file_path}: {e_rem}", exc_info=True)

@app.post("/api/analyze", response_model=AnalysisStep6Output)
async def analyze_scenario_endpoint(
    payload: ScenarioInput,
    current_user: dict = Depends(get_current_user) # Inject user data dependency
):
    """
    Receives a dental scenario, cleans it, classifies CDT/ICD, 
    activates topics, saves to DB, generates questions, runs inspectors (conditionally),
    and returns full results. Requires authentication.
    """
    logger.info(f"Received scenario for full analysis from user {current_user.get('id')}: {payload.scenario[:75]}...")
    record_id = None
    questioner_data = {} # Initialize for scope
    inspector_results = {} # Initialize for scope
    try:
        # Step 1: Clean the scenario
        logger.info(f"*********🔍 Step 1: Cleaning Scenario:*********************")
        cleaned_data = scenario_processor.process(payload.scenario)
        cleaned_scenario_text = cleaned_data.get("standardized_scenario", "")
        if not cleaned_scenario_text:
            logger.error("Scenario cleaning failed or produced empty result.")
            raise HTTPException(status_code=500, detail="Failed to clean scenario.")
        logger.info(f"Scenario cleaned successfully.")

        # Step 2: Run CDT & ICD Classifiers concurrently
        logger.info(f"*********🚀 Step 2: Starting Concurrent CDT & ICD Classification:*********************")
        cdt_task = asyncio.to_thread(cdt_classifier.process, cleaned_scenario_text)
        icd_task = asyncio.to_thread(icd_classifier.process, cleaned_scenario_text)
        
        # Await results from both classifiers
        cdt_results, icd_results = await asyncio.gather(cdt_task, icd_task)
        logger.info(f"CDT & ICD classification completed.")
        logger.debug(f"CDT Raw Results: {cdt_results}")
        logger.debug(f"ICD Raw Results: {icd_results}")

        # Step 3: Activate relevant CDT and ICD topics CONCURRENTLY
        logger.info(f"*********💡 Step 3: Activating Topics Concurrently:*********************")
        
        cdt_topic_activation_results = [] # Store final CDT results
        icd_topic_details = {} # Store final single ICD result (or error)
        cdt_code_ranges_to_activate = set()
        icd_category_to_activate = None

        # Determine which CDT topics to activate
        if cdt_results and isinstance(cdt_results, dict) and cdt_results.get("range_codes_string"):
            cdt_range_codes_str = cdt_results["range_codes_string"]
            logger.info(f"Classifier identified CDT ranges: {cdt_range_codes_str}")
            for code_range in cdt_range_codes_str.split(','):
                code_range = code_range.strip()
                if code_range in CDT_TOPIC_MAPPING:
                    cdt_code_ranges_to_activate.add(code_range)
                else:
                    logger.warning(f"CDT code range '{code_range}' from classifier not found in CDT_TOPIC_MAPPING.")
        else:
            logger.warning(f"Skipping CDT topic activation tasks due to missing/invalid classification result: {cdt_results}")

        # Determine which ICD topic to activate
        icd_category_number = None # Initialize
        if icd_results and isinstance(icd_results, dict):
            icd_category_number = icd_results.get("category_number")
            
        # Corrected logic block for determining icd_category_to_activate
        if icd_category_number:
            icd_category_str = str(icd_category_number)
            if icd_category_str in ICD_TOPIC_MAPPING:
                icd_category_to_activate = icd_category_str
            else:
                logger.warning(f"ICD category number '{icd_category_str}' not found in ICD_TOPIC_MAPPING.")
        elif icd_results: # Check if icd_results exists but number is missing
             logger.warning(f"ICD category number missing in classification result: {icd_results}")
        else: # Case where icd_results itself is invalid or missing
             logger.warning(f"Skipping ICD topic activation task due to missing/invalid classification result: {icd_results}")

        # Create activation tasks
        tasks_to_gather = []

        # CDT Task
        if cdt_code_ranges_to_activate:
            cdt_ranges_str = ",".join(sorted(list(cdt_code_ranges_to_activate)))
            logger.info(f"Creating activation task for CDT ranges: {cdt_ranges_str}")
            # Assuming activate_all returns a coroutine
            cdt_task = topic_registry.activate_all(cleaned_scenario_text, cdt_ranges_str)
            tasks_to_gather.append(cdt_task)
        else:
            async def _dummy_cdt_task(): return []
            tasks_to_gather.append(_dummy_cdt_task()) # Add the coroutine

        # ICD Task
        if icd_category_to_activate:
            logger.info(f"Creating activation task for ICD category: {icd_category_to_activate}")
            # Assuming activate_all returns a coroutine
            icd_task = topic_registry.activate_all(cleaned_scenario_text, icd_category_to_activate)
            tasks_to_gather.append(icd_task)
        else:
            async def _dummy_icd_task(): return []
            tasks_to_gather.append(_dummy_icd_task()) # Add the coroutine

        # Run activations concurrently using asyncio.gather
        logger.info(f"Starting parallel activation of CDT and ICD topics")
        # Gather all tasks in the list
        results = await asyncio.gather(*tasks_to_gather)
        logger.info(f"Finished gathering topic activation results.")

        # Unpack results carefully based on what was added
        cdt_registry_results = []
        icd_registry_results = [] # Should be list containing one dict or empty list

        result_index = 0
        if cdt_code_ranges_to_activate:
            cdt_registry_results = results[result_index]
            result_index += 1
        else:
            # Skip the dummy CDT result (which is [])
            result_index += 1

        if icd_category_to_activate:
            # The result from activate_all should be a list (even if one item)
            icd_registry_results = results[result_index]
            result_index += 1
        else:
            # Skip the dummy ICD result (which is [])
            result_index +=1

        # Process CDT results (already a list from activate_all or dummy)
        cdt_topic_activation_results = cdt_registry_results if isinstance(cdt_registry_results, list) else []
        logger.info(f"Processed {len(cdt_topic_activation_results)} CDT topic results.")
        logger.debug(f"CDT Activation Results: {cdt_topic_activation_results}")

        # Process ICD results (should be a list with 0 or 1 item from activate_all or dummy)
        icd_topic_details = {} # Reset for clarity
        if isinstance(icd_registry_results, list) and icd_registry_results:
            # If activate_all returned a list with the result
            icd_topic_details = icd_registry_results[0]
            logger.info(f"Successfully processed ICD topic: {icd_topic_details.get('topic')}")
        elif icd_category_to_activate: # Log warning only if we expected a result but got none
            logger.warning(f"No result found for activated ICD category: {icd_category_to_activate}. Registry result: {icd_registry_results}")
            icd_topic_details = {"error": f"Activation result missing for ICD category {icd_category_to_activate}", "topic": "Error", "code_range": icd_category_to_activate}
        else:
            # If no category was activated, keep icd_topic_details as an empty dict
            logger.info("No ICD category was activated.")
        logger.debug(f"ICD Activation Result: {icd_topic_details}")

        # --- Step 4: Save Initial Data to Database --- 
        logger.info(f"*********💾 Step 4: Saving Initial Data to DB:*********************")
        
        # Prepare the full topic activation results for saving
        # CDT: Use the direct list of results from activate_all
        cdt_data_to_save = cdt_topic_activation_results
        
        # ICD: Use the direct result dictionary from activate_all processing
        icd_data_to_save = icd_topic_details

        # Convert to JSON strings
        # Use default=str to handle potential non-serializable types like datetime if they exist
        cdt_json = json.dumps(cdt_data_to_save, default=str)
        icd_json = json.dumps(icd_data_to_save, default=str)

        db_data = {
            "user_question": payload.scenario,
            "processed_clean_data": cleaned_scenario_text,
            "cdt_result": cdt_json, # Store JSON string of the full list
            "icd_result": icd_json, # Store JSON string of the full dict
            # user_id will be passed separately
        }

        # Save to DB and get record_id
        db_result_list = db.create_analysis_record(db_data, user_id=current_user.get('id'))
        
        if db_result_list and isinstance(db_result_list, list) and len(db_result_list) > 0 and "id" in db_result_list[0]:
            record_id = db_result_list[0]["id"]
            logger.info(f"Data saved successfully with Record ID: {record_id}")
        else:
            logger.error(f"Failed to save data to database or get valid ID. DB Response: {db_result_list}")
            raise HTTPException(status_code=500, detail="Failed to save analysis results to database.")

        # --- Step 5: Generate Questions --- 
        logger.info(f"*********❓ Step 5: Generating Questions:*********************")
        questioner_data = {"has_questions": False, "status": "skipped"} # Default
        try:
            # Format data for Questioner (using actual results)
            # Note: Ensure cdt_results and icd_results are dictionaries as expected
            simplified_cdt_data = {
                "code_ranges": cdt_results.get("range_codes_string", "") if isinstance(cdt_results, dict) else "",
                "activated_topics": [topic.get('topic') for topic in cdt_topic_activation_results if topic.get("error") is None],
                "formatted_cdt_results": cdt_results.get('formatted_results', []) if isinstance(cdt_results, dict) else []
            }
            simplified_icd_data = {
                "code": icd_results.get("icd_code", "") if isinstance(icd_results, dict) else "",
                "explanation": icd_results.get("explanation", "") if isinstance(icd_results, dict) else "",
                "doubt": icd_results.get("doubt", "") if isinstance(icd_results, dict) else "",
                "category": ICD_CATEGORY_NAMES.get(str(icd_results.get("category_number"))) if isinstance(icd_results, dict) and icd_results.get("category_number") else None
            }
            # Prevent passing error structure as data
            if simplified_icd_data.get("error"):
                 simplified_icd_data = {"code": "", "explanation": f"ICD Error: {simplified_icd_data['error']}", "doubt": "", "category": "Error"}

            # Run Questioner (assuming synchronous for now, wrap if needed)
            # If questioner.process is async, use: await questioner.process(...)
            questioner_result = questioner.process(
                cleaned_scenario_text,
                simplified_cdt_data,
                simplified_icd_data
            )
            questioner_data = questioner_result # Store the full result

            # Save questioner data to the database
            questioner_json = json.dumps(questioner_result, default=str)
            db.update_questioner_data(record_id, questioner_json)
            logger.info(f"Questioner data saved to DB for record ID: {record_id}. Has Questions: {questioner_result.get('has_questions', False)}")

        except Exception as q_err:
            logger.error(f"Error during question generation for {record_id}: {q_err}", exc_info=True)
            questioner_data["error"] = f"Questioner Error: {str(q_err)}"
            questioner_data["status"] = "error"
            # Attempt to save error state to DB
            try:
                db.update_questioner_data(record_id, json.dumps(questioner_data, default=str))
                logger.warning(f"Saved questioner error state to DB for record ID: {record_id}")
            except Exception as db_q_err:
                logger.error(f"Failed to save questioner error state to DB for {record_id}: {db_q_err}")

        # --- Step 6: Run Inspectors (Conditionally) ---
        logger.info(f"*********🕵️ Step 6: Running Inspectors (Conditionally):*********************")
        inspector_results = {"cdt": {}, "icd": {}, "status": "not_run"} # Default state
        # Run inspectors only if the questioner didn't generate questions
        should_run_inspectors = not questioner_data.get("has_questions", True) 

        if should_run_inspectors:
            logger.info(f"No questions generated for {record_id}, running inspectors immediately.")
            try:
                # Pass the full activation results to inspectors
                cdt_inspector_input = cdt_topic_activation_results
                icd_inspector_input = icd_topic_details # This is the single dictionary
                
                # Define async inspector tasks using asyncio.to_thread
                cdt_inspector_task = asyncio.to_thread(
                    cdt_inspector.process, 
                    cleaned_scenario_text, 
                    cdt_inspector_input, 
                    questioner_data
                )
                icd_inspector_task = asyncio.to_thread(
                    icd_inspector.process, 
                    cleaned_scenario_text, 
                    icd_inspector_input, 
                    questioner_data
                )

                # Run concurrently
                cdt_inspector_result, icd_inspector_result = await asyncio.gather(
                    cdt_inspector_task, icd_inspector_task
                )
                logger.info(f"CDT Inspector Result Codes: {cdt_inspector_result.get('codes')}")
                logger.info(f"ICD Inspector Result Codes: {icd_inspector_result.get('codes')}")

                # Combine and save results
                inspector_results = {
                    "cdt": cdt_inspector_result,
                    "icd": icd_inspector_result,
                    "status": "completed" # Mark as completed
                }
                db.update_inspector_results(record_id, json.dumps(inspector_results, default=str))
                logger.info(f"Inspector results saved to DB for record ID: {record_id}")

            except Exception as insp_err:
                logger.error(f"Error during inspector processing for {record_id}: {insp_err}", exc_info=True)
                inspector_results["error"] = f"Inspector Error: {str(insp_err)}"
                inspector_results["status"] = "error"
                # Attempt to save error state
                try:
                    db.update_inspector_results(record_id, json.dumps(inspector_results, default=str))
                    logger.warning(f"Saved inspector error state to DB for record ID: {record_id}")
                except Exception as db_insp_err:
                    logger.error(f"Failed to save inspector error state to DB for {record_id}: {db_insp_err}")
        else:
            logger.info(f"Skipping immediate inspector run for {record_id} as questions were generated.")

        # --- Step 7: Construct Final Response --- 
        logger.info(f"*********🔧 Step 7: Constructing Final Response:*********************")
        
        # Apply final formatting/parsing to CDT topic results using dental_manager
        # This adds the 'parsed_result' field based on the original 'raw_result'
        logger.info(f"Formatting CDT subtopic results...")
        formatted_cdt_subtopic_results = cdt_topic_activation_results # Default to original
        try:
            # Ensure cdt_topic_activation_results is a list of dicts before passing
            if isinstance(cdt_topic_activation_results, list):
                 # This function now ADDS 'parsed_result' instead of replacing 'raw_result'
                 formatted_cdt_subtopic_results = dental_manager.transform_json_list(cdt_topic_activation_results)
            else:
                logger.warning("CDT topic activation results are not a list, skipping subtopic formatting.")
        except Exception as fmt_err:
             logger.error(f"Error formatting CDT subtopic results: {fmt_err}", exc_info=True)
             # On error, we still use the unformatted results

        # Prepare the final response including Questioner and Inspector results
        response_data = AnalysisStep6Output(
            record_id=record_id,
            original_scenario=payload.scenario,
            cleaned_scenario=cleaned_data.get("cleaned_scenario", "Cleaning failed"),
            standardized_scenario=cleaned_scenario_text,
            cdt_classification_results=cdt_results, 
            icd_classification_results=icd_results,
            cdt_topic_activation_results=formatted_cdt_subtopic_results, # Use the potentially formatted results
            icd_topic_activation_results=icd_topic_details,
            questioner_data=questioner_data,      # Add questioner results
            inspector_results=inspector_results   # Add inspector results
        )
        return response_data

    except HTTPException as http_exc: # Re-raise HTTP exceptions
        raise http_exc
    except Exception as e:
        logger.error(f"Error during scenario analysis (clean & classify & activate): {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error during analysis: {str(e)}")

# --- Add Custom Code Endpoint --- 
@app.post("/api/add-custom-code")
async def add_custom_code(
    request: CustomCodeRequest,
    current_user: dict = Depends(get_current_user) # Inject user data dependency
):
    """Process and add a custom code for a given scenario, associated with the user."""
    try:
        logger.info(f"--- Adding Custom Code for Record {request.record_id} by User {current_user.get('id')} --- ")
        logger.info(f"Custom code: {request.code}")
        
        # Run the custom code analysis 
        # Assuming Add_code_data is synchronous; wrap if async
        analysis_result = Add_code_data(request.scenario, request.code)
        logger.info(f"Add_code_data result: {analysis_result}")

        # Save analysis to the separate dental_code_analysis table
        try:
            db.add_code_analysis(
                scenario=request.scenario,
                cdt_codes=request.code,
                response=analysis_result, # Store the full response
                user_id=current_user.get('id')
            )
            logger.info(f"Custom code analysis saved to dental_code_analysis table.")
        except Exception as db_err:
            logger.error(f"Failed to save custom code analysis to DB: {db_err}", exc_info=True)
            # Depending on requirements, might raise HTTPException here

        # Parse the result (adjust parsing logic if Add_code_data format changes)
        explanation = ""
        doubt = "None"
        is_applicable = False # Default
        if isinstance(analysis_result, str):
            if "Explanation:" in analysis_result:
                explanation = analysis_result.split("Explanation:")[1].strip()
                if "Doubt:" in explanation:
                    parts = explanation.split("Doubt:")
                    explanation = parts[0].strip()
                    doubt = parts[1].strip()
            else:
                explanation = analysis_result # Assume entire result is explanation
            is_applicable = "applicable? yes" in analysis_result.lower()
        else:
            explanation = "Invalid analysis result format received."
        
        # Format response (mimicking inspector structure for consistency)
        code_data = {
            "code": request.code,
            "explanation": explanation,
            "doubt": doubt,
            "isApplicable": is_applicable
        }
        inspector_like_results = {
            "cdt": {
                "codes": [request.code] if is_applicable else [],
                "rejected_codes": [] if is_applicable else [request.code],
                "explanation": explanation
            },
            "icd": { # Assuming custom codes are CDT only
                "codes": [], "rejected_codes": [], "explanation": "N/A"
            }
        }
        
        return {
            "status": "success",
            "message": "Custom code analysis completed",
            "data": {"code_data": code_data, "inspector_results": inspector_like_results}
        }
        
    except Exception as e:
        error_details = traceback.format_exc()
        logger.error(f"❌ ERROR adding custom code for Record {request.record_id}: {str(e)}")
        logger.error(f"STACK TRACE: {error_details}")
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        if isinstance(e, HTTPException) and e.status_code == 401:
            status_code = e.status_code
        raise HTTPException(status_code=status_code, detail=str(e))

# --- Add Store Code Status Endpoint --- 
@app.post("/api/store-code-status")
async def store_code_status(
    request: CodeStatusRequest,
    current_user: dict = Depends(get_current_user) # Inject user data dependency
):
    """Store the final status of selected and rejected codes based on user input."""
    try:
        user_id = current_user.get('id') # Extract user ID
        logger.info(f"--- Storing Code Status for Record {request.record_id} by User {user_id} --- ")
        logger.info(f"Accepted CDT: {request.cdt_codes}")
        logger.info(f"Rejected CDT: {request.rejected_cdt_codes}")
        logger.info(f"Accepted ICD: {request.icd_codes}")
        logger.info(f"Rejected ICD: {request.rejected_icd_codes}")
        
        # Save selections to the dedicated table
        saved_selection = db.save_code_selections(
            record_id=request.record_id,
            accepted_cdt=request.cdt_codes,
            rejected_cdt=request.rejected_cdt_codes,
            accepted_icd=request.icd_codes,
            rejected_icd=request.rejected_icd_codes,
            user_id=user_id
        )

        if not saved_selection:
            logger.error(f"Failed to save code selections for record ID: {request.record_id}")
            raise HTTPException(status_code=500, detail="Failed to save code selections to database.")

        logger.info(f"Code status updated in the database for {request.record_id}")
        return {
            "status": "success",
            "message": "Code status updated successfully",
            "saved_selection": saved_selection
        }
        
    except Exception as e:
        error_details = traceback.format_exc()
        logger.error(f"❌ ERROR storing code status for Record {request.record_id}: {str(e)}")
        logger.error(f"STACK TRACE: {error_details}")
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        if isinstance(e, HTTPException) and e.status_code == 401:
            status_code = e.status_code
        raise HTTPException(status_code=status_code, detail=str(e))

# --- User Activity Endpoint ---
@app.get("/api/user/activity", response_model=UserActivityResponse)
async def get_user_activity(
    current_user: dict = Depends(get_current_user) # Inject user data dependency
):
    """Retrieve user details and their analysis history."""
    user_id = current_user.get('id') # Get user ID from the dependency result
    logger.info(f"Fetching activity for user ID: {user_id} (Role: {current_user.get('role')})")
    try:
        # Fetch user details
        user_details_data = db.get_user_details_by_id(user_id)
        if not user_details_data:
            logger.warning(f"User not found for activity request: {user_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        # Fetch user analyses
        user_analyses_data = db.get_user_analyses(user_id)
        
        # Prepare response
        user_details = UserDetails(**user_details_data)
        analysis_summaries = [AnalysisSummary(**analysis) for analysis in user_analyses_data]
        
        response = UserActivityResponse(
            user_details=user_details,
            analysis_count=len(analysis_summaries),
            analyses=analysis_summaries
        )
        
        logger.info(f"Successfully retrieved activity for user ID: {user_id} ({len(analysis_summaries)} analyses)")
        return response

    except HTTPException as http_exc: # Re-raise HTTP exceptions
        raise http_exc
    except Exception as e:
        error_details = traceback.format_exc()
        logger.error(f"❌ ERROR fetching user activity for User {user_id}: {str(e)}")
        logger.error(f"STACK TRACE: {error_details}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve user activity")

# --- Admin Endpoint --- 
@app.get("/api/admin/all-users", response_model=AllUsersActivityResponse)
async def get_all_user_activity(
    admin_user: dict = Depends(require_admin_role) # Use REAL admin check dependency
):
    """(Admin) Retrieve details and analysis count for all users."""
    admin_user_id = admin_user.get('id') # Get admin user ID
    logger.info(f"Admin request received from {admin_user_id} (Role: {admin_user.get('role')}) to fetch all user activity.")
    try:
        # Fetch all user details
        all_users_data = db.get_all_users_details()
        if not all_users_data:
             logger.info("No users found to report.")
             return AllUsersActivityResponse(users=[])
             
        # Fetch all analysis summaries (includes user_id)
        all_analyses_data = db.get_user_analyses() # Call with no user_id
        
        # Create a map of user_id -> analysis_count
        analysis_counts = {}
        for analysis in all_analyses_data:
            uid = analysis.get('user_id')
            if uid:
                analysis_counts[uid] = analysis_counts.get(uid, 0) + 1
                
        # Prepare response list
        admin_user_summaries = []
        for user_data in all_users_data:
            user_id = user_data.get('id')
            user_summary = AdminUserSummary(
                **user_data, # Pass all fields from UserDetails
                analysis_count=analysis_counts.get(user_id, 0)
            )
            admin_user_summaries.append(user_summary)

        response = AllUsersActivityResponse(users=admin_user_summaries)
        logger.info(f"Successfully retrieved activity summary for {len(admin_user_summaries)} users.")
        return response

    except Exception as e:
        error_details = traceback.format_exc()
        logger.error(f"❌ ERROR fetching all user activity: {str(e)}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve all user activity")

# Add a root endpoint for basic checks
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Dental Scenario Analysis API"}

# --- Application Runner ---
if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8001
    logger.info(f"Starting Uvicorn server for Cleaning & Auth API on {host}:{port}")
    uvicorn.run("app:app", host=host, port=port, reload=True)