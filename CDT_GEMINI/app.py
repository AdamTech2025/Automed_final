﻿from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import uvicorn
import logging
import asyncio # Add asyncio import
import os # Add os import for getenv
from fastapi.middleware.cors import CORSMiddleware # Import CORS Middleware
from data_cleaner import DentalScenarioProcessor # Import the processor
from cdt_classifier import CDTClassifier       # Import CDT Classifier
from icd_classifier import ICDClassifier       # Import ICD Classifier
import json # Add json import
import traceback # Add traceback import
from typing import List, Dict, Any # Import List for request models
import datetime # Import datetime for timestamping

# Import Topic Activation components
from sub_topic_registry import SubtopicRegistry
# Import Questioner
from questioner import Questioner
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
# ICD Topics - Corrected Imports based on previous step
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

# Import Database class
from database import MedicalCodingDB

# Import Inspectors
from inspector import DentalInspector
from icd_inspector import ICDInspector

# Import Add Code functionality
from add_codes.add_code_data import Add_code_data

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Dental Scenario Analysis API",
    description="API for analyzing dental scenarios and suggesting CDT/ICD codes.",
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

# Initialize processors/classifiers
scenario_processor = DentalScenarioProcessor()
cdt_classifier = CDTClassifier()
icd_classifier = ICDClassifier()
questioner = Questioner() # Initialize Questioner
cdt_inspector = DentalInspector() # Initialize CDT Inspector
icd_inspector = ICDInspector() # Initialize ICD Inspector

# Initialize Topic Registry (Combined CDT & ICD)
topic_registry = SubtopicRegistry()

# Initialize Database Connection
db = MedicalCodingDB()

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

# --- ICD Topic Mapping and Registration (Corrected based on previous step) ---
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

class ScenarioInput(BaseModel):
    scenario: str

# --- Add Request Models from app.py.bak ---
class CustomCodeRequest(BaseModel):
    code: str
    scenario: str # Need the original scenario for Add_code_data
    record_id: str # Might be useful for context, though not used in bak logic

class CodeStatusRequest(BaseModel):
    record_id: str
    cdt_codes: List[str] = []
    icd_codes: List[str] = []
    rejected_cdt_codes: List[str] = []
    rejected_icd_codes: List[str] = []
# ------------------------------------------

# REMOVE the old response model
# class DetailedAnalysisOutput(BaseModel):
#     standardized_scenario: str
#     cdt_classification_results: dict 
#     icd_classification_results: dict 
#     cdt_topic_results: dict 
#     icd_topic_results: dict 

# REMOVE the old helper function (parsing is now done in SubtopicRegistry)
# def _parse_activation_result(result_text: str) -> dict: ... 

# Remove response_model from the endpoint definition
# @app.post(\"/api/analyze\", response_model=DetailedAnalysisOutput)
@app.post("/api/analyze")
async def analyze_scenario(payload: ScenarioInput):
    """
    Receives a dental scenario, cleans it, classifies CDT/ICD, 
    activates relevant CDT/ICD topics, saves to DB, and returns results.
    """
    logger.info(f"Received scenario for analysis: {payload.scenario[:75]}...")
    record_id = None # Initialize record_id for error handling

    try:
        # Step 1: Clean the scenario
        logger.info("*********🔍 step 1 :Cleaning Scenario:*********************")
        cleaned_data = scenario_processor.process(payload.scenario)
        cleaned_scenario_text = cleaned_data["standardized_scenario"]
        logger.info("Scenario cleaned successfully.")

        # Step 2: Run CDT & ICD Classifiers concurrently
        logger.info("*********🚀 step 2: Starting Concurrent CDT & ICD Classification:*********************")
        cdt_task = asyncio.to_thread(cdt_classifier.process, cleaned_scenario_text)
        icd_task = asyncio.to_thread(icd_classifier.process, cleaned_scenario_text)
        cdt_classification_results, icd_classification_results = await asyncio.gather(cdt_task, icd_task)
        logger.info("CDT & ICD classification completed.")

        # Step 3: Activate relevant CDT and ICD topics CONCURRENTLY
        logger.info("*********💡 step 3: Activating Topics Concurrently:*********************")
        
        tasks = []
        topic_keys = [] # To map results back
        cdt_topic_activation_results = [] # Store final CDT results
        icd_topic_details = None # Store final single ICD result
        cdt_code_ranges_to_activate = set()
        icd_category_to_activate = None

        # Determine which CDT topics to activate
        if cdt_classification_results and cdt_classification_results.get("range_codes_string"):
            cdt_range_codes_str = cdt_classification_results["range_codes_string"]
            for code_range in cdt_range_codes_str.split(','):
                code_range = code_range.strip()
                if code_range in CDT_TOPIC_MAPPING:
                    cdt_code_ranges_to_activate.add(code_range)
                    topic_info = CDT_TOPIC_MAPPING[code_range]
                    topic_keys.append({"type": "cdt", "key": code_range, "name": topic_info['name']}) 
                    tasks.append(asyncio.create_task(topic_info["func"](cleaned_scenario_text)))                 
                else:
                    logger.warning(f"CDT code range {code_range} from classifier not found in CDT_TOPIC_MAPPING.")
        else:
            logger.warning("Skipping CDT topic activation tasks due to missing/invalid classification.")

        # Determine which ICD topic to activate
        icd_category_number = icd_classification_results.get("category_number")
        if icd_category_number:
            icd_category_str = str(icd_category_number)
            if icd_category_str in ICD_TOPIC_MAPPING:
                icd_category_to_activate = icd_category_str
                topic_info = ICD_TOPIC_MAPPING[icd_category_str]
                if asyncio.iscoroutinefunction(topic_info["func"]):
                    topic_keys.append({"type": "icd", "key": icd_category_str, "name": topic_info['name']}) 
                    tasks.append(asyncio.create_task(topic_info["func"](cleaned_scenario_text)))
                else:
                    logger.warning(f"Function for ICD topic {topic_info['name']} is NOT async. Skipping.")
            else:
                 logger.warning(f"ICD category number {icd_category_str} not found in ICD_TOPIC_MAPPING.")
        else:
             logger.warning("Skipping ICD topic activation task due to missing/invalid classification.")

        # Run all topic activation tasks concurrently
        if tasks:
            logger.info(f"Running {len(tasks)} topic activation tasks concurrently...")
            # Use the SubtopicRegistry's activate_all method, passing the relevant keys
            # Combine CDT ranges and the single ICD key into one string for the registry
            keys_to_activate_str = ",".join(list(cdt_code_ranges_to_activate) + ([icd_category_to_activate] if icd_category_to_activate else []))
            logger.info(f"Keys passed to activate_all: {keys_to_activate_str}")
            
            # The registry now handles running and parsing
            registry_results = await topic_registry.activate_all(cleaned_scenario_text, keys_to_activate_str)
            logger.info("SubtopicRegistry activation completed.")
            
            # Separate the results
            all_topic_results = registry_results.get("topic_result", []) 
            cdt_topic_activation_results = [res for res in all_topic_results if res["code_range"] in cdt_code_ranges_to_activate] 
            icd_results_list = [res for res in all_topic_results if res["code_range"] == icd_category_to_activate] 
            
            if icd_results_list:
                icd_topic_details = icd_results_list[0] # Should only be one
                logger.info(f"Successfully processed ICD topic: {icd_topic_details.get('topic')}")
            else:
                 logger.warning(f"No result found for activated ICD category: {icd_category_to_activate}")
                 icd_topic_details = {"error": f"Activation result missing for ICD category {icd_category_to_activate}"}
            
            logger.info(f"Processed {len(cdt_topic_activation_results)} CDT topic results.")
                 
        else:
            logger.warning("No topic activation tasks were created.")
            cdt_topic_activation_results = [{"error": "No CDT topics activated."}]
            icd_topic_details = {"error": "No ICD topic activated."}

        # --- Step 4a: Save Initial Data to Database --- 
        logger.info("*********💾 step 4a: Saving Initial Data to DB:*********************")
        cdt_data_to_save = {
            "cdt_classification": cdt_classification_results, # Includes raw_data, formatted_results
            "topics_results": cdt_topic_activation_results # Includes subtopic details with raw_data
        }
        icd_data_to_save = {
            "icd_classification": icd_classification_results, # Includes raw_data, category_number etc.
            "topic_results": icd_topic_details # Includes topic details with raw_data
        }

        cdt_json = json.dumps(cdt_data_to_save)
        icd_json = json.dumps(icd_data_to_save)

        db_data = {
            "user_question": payload.scenario,
            "processed_clean_data": cleaned_scenario_text,
            "cdt_result": cdt_json,
            "icd_result": icd_json
        }

        db_result_list = db.create_analysis_record(db_data)
        if db_result_list and isinstance(db_result_list, list) and len(db_result_list) > 0 and "id" in db_result_list[0]:
            record_id = db_result_list[0]["id"]
            logger.info(f"Data saved successfully with Record ID: {record_id}")
        else:
            logger.error(f"Failed to save data to database or get valid ID. DB Response: {db_result_list}")
            # Consider raising an error or returning a specific error response
            raise HTTPException(status_code=500, detail="Failed to save analysis results to database.")

        # --- Step 5: Generate Questions --- 
        logger.info("*********❓ step 5: Generating Questions:*********************")
        questioner_data = {"has_questions": False, "status": "skipped"} # Default
        try:
            # Format data for Questioner (similar to app.py.bak)
            simplified_cdt_data = {
                "code_ranges": cdt_classification_results.get("range_codes_string", ""),
                "activated_topics": [topic.get('topic') for topic in cdt_topic_activation_results if not topic.get('error')],
                "formatted_cdt_results": [
                    f"{res.get('code_range')}: {res.get('explanation')}"
                    for res in cdt_classification_results.get('formatted_results', [])
                ]
            }
            # Extract simplified ICD info
            simplified_icd_data = {
                "code": icd_classification_results.get("icd_code", ""), # Assuming 'icd_code' key exists
                "explanation": icd_classification_results.get("explanation", ""),
                "doubt": icd_classification_results.get("doubt", ""),
                "category": ICD_CATEGORY_NAMES.get(str(icd_classification_results.get("category_number")))
            }
            # Ensure ICD data passed is not just the error structure
            if "error" in simplified_icd_data:
                 simplified_icd_data = {"code": "", "explanation": f"ICD Error: {simplified_icd_data['error']}", "doubt": "", "category": "Error"}

            questioner_result = questioner.process(
                cleaned_scenario_text,
                simplified_cdt_data,
                simplified_icd_data
            )
            questioner_data = questioner_result # Store the full result

            # Save questioner data to the database
            questioner_json = json.dumps(questioner_result)
            db.update_questioner_data(record_id, questioner_json)
            logger.info(f"Questioner data saved to DB for record ID: {record_id}. Has Questions: {questioner_result.get('has_questions', False)}")

        except Exception as q_err:
            logger.error(f"Error during question generation for {record_id}: {q_err}", exc_info=True)
            questioner_data["error"] = f"Questioner Error: {str(q_err)}"
            questioner_data["status"] = "error"
            # Attempt to save error state to DB
            try:
                db.update_questioner_data(record_id, json.dumps(questioner_data))
                logger.warning(f"Saved questioner error state to DB for record ID: {record_id}")
            except Exception as db_q_err:
                logger.error(f"Failed to save questioner error state to DB for {record_id}: {db_q_err}")

        # --- Step 6: Run Inspectors (Conditionally) ---
        logger.info("*********🕵️ step 6: Running Inspectors (Conditionally):*********************")
        inspector_results = {"cdt": {}, "icd": {}, "status": "not_run"} # Default state
        should_run_inspectors = not questioner_data.get("has_questions", True) # Run if no questions

        if should_run_inspectors:
            logger.info(f"No questions generated for {record_id}, running inspectors immediately.")
            try:
                # Format data for CDT inspector (mimicking app.py.bak)
                cdt_topic_analysis_for_inspector = {}
                # Use the data we prepared for saving (cdt_data_to_save)
                cdt_topics_results = cdt_data_to_save.get("topics_results", [])
                all_candidate_codes = []
                for topic_res in cdt_topics_results:
                    if not topic_res.get('error'):
                        codes_list = topic_res.get('codes', [])
                        if codes_list: # Assuming 'codes' now contains the detailed list including raw_data
                            formatted_codes = []
                            subtopic_key = f"{topic_res.get('topic', 'Unknown')} ({topic_res.get('code_range', '')})"
                            for code_entry in codes_list:
                                code = code_entry.get("code", "")
                                explanation = code_entry.get("explanation", "")
                                doubt = code_entry.get("doubt", "")
                                if code and code.lower() != 'none':
                                    all_candidate_codes.append(code) # Add to candidate list
                                formatted_code = f"CODE: {code}\nEXPLANATION: {explanation}"
                                if doubt: formatted_code += f"\nDOUBT: {doubt}"
                                formatted_codes.append(formatted_code)
                            # Store formatted result string for the subtopic
                            cdt_topic_analysis_for_inspector[subtopic_key] = {"name": subtopic_key, "result": "\n\n".join(formatted_codes)}
                # Add all candidate codes summary
                if all_candidate_codes:
                    cdt_topic_analysis_for_inspector["_all_candidate_codes"] = {
                        "name": "All Candidate Codes",
                        "result": "CODES: " + ", ".join(list(set(all_candidate_codes)))
                    }

                # Format data for ICD inspector (mimicking app.py.bak)
                icd_topic_analysis_for_inspector = {}
                # Use the data we prepared for saving (icd_data_to_save)
                icd_topic_result_detail = icd_data_to_save.get("topic_results")
                icd_classification_detail = icd_data_to_save.get("icd_classification")
                if icd_topic_result_detail and not icd_topic_result_detail.get('error') and icd_classification_detail:
                    category_num = icd_classification_detail.get('category_number')
                    if category_num:
                        category_key = str(category_num)
                        simplified = { # Reconstruct simplified structure for inspector
                            "code": icd_topic_result_detail.get('codes', [{}])[0].get('code', ''),
                            "explanation": icd_topic_result_detail.get('codes', [{}])[0].get('explanation', ''),
                            "doubt": icd_topic_result_detail.get('codes', [{}])[0].get('doubt', '')
                        }
                        icd_topic_analysis_for_inspector[category_key] = {
                            "name": ICD_CATEGORY_NAMES.get(category_key, "Unknown ICD Topic"),
                            "result": icd_topic_result_detail.get('raw_data', "No raw data"), # Pass raw data if available
                            "parsed_result": simplified
                        }
                    else:
                        logger.warning(f"ICD category number missing in classification data for inspector.")
                elif icd_classification_detail and icd_classification_detail.get('error'):
                    logger.warning(f"Skipping ICD inspection for {record_id} due to ICD classification error: {icd_classification_detail.get('error')}")
                else:
                     logger.warning(f"Could not format ICD data for inspector for record {record_id}.")

                # Define async inspector tasks
                cdt_inspector_task = asyncio.to_thread(
                    cdt_inspector.process, 
                    cleaned_scenario_text, 
                    cdt_topic_analysis_for_inspector, # Pass formatted CDT data
                    questioner_data
                )
                icd_inspector_task = asyncio.to_thread(
                    icd_inspector.process, 
                    cleaned_scenario_text, 
                    icd_topic_analysis_for_inspector, # Pass formatted ICD data
                    questioner_data
                )

                # Run concurrently
                cdt_inspector_result, icd_inspector_result = await asyncio.gather(
                    cdt_inspector_task, icd_inspector_task
                )
                logger.info(f"CDT Inspector Result: {cdt_inspector_result.get('codes')}")
                logger.info(f"ICD Inspector Result: {icd_inspector_result.get('codes')}")

                # Combine and save results
                inspector_results = {
                    "cdt": cdt_inspector_result,
                    "icd": icd_inspector_result,
                    "status": "completed" # Mark as completed
                }
                db.update_inspector_results(record_id, json.dumps(inspector_results))
                logger.info(f"Inspector results saved to DB for record ID: {record_id}")

            except Exception as insp_err:
                logger.error(f"Error during inspector processing for {record_id}: {insp_err}", exc_info=True)
                inspector_results["error"] = f"Inspector Error: {str(insp_err)}"
                inspector_results["status"] = "error"
                # Attempt to save error state
                try:
                    db.update_inspector_results(record_id, json.dumps(inspector_results))
                    logger.warning(f"Saved inspector error state to DB for record ID: {record_id}")
                except Exception as db_insp_err:
                    logger.error(f"Failed to save inspector error state to DB for {record_id}: {db_insp_err}")
        else:
            logger.info(f"Skipping immediate inspector run for {record_id} as questions were generated.")

        # --- Construct the final response --- 
        logger.info("*********🔧 step 7: Constructing Final Response:*********************")

        # CDT Classifier Results
        cdt_classifier_response = {
            "raw_data": cdt_classification_results.get('raw_data'),
            "formatted_results": cdt_classification_results.get('formatted_results')
        }
        
        # CDT Topic Summary
        cdt_topic_summary = [
            {"topic": item.get('topic'), "code_range": item.get('code_range')} 
            for item in cdt_topic_activation_results if not item.get('error')
        ]
        
        # CDT Subtopic Details (Includes raw_data within 'codes' list)
        cdt_subtopic_details = cdt_topic_activation_results

        # ICD Classifier Results
        icd_classifier_response = icd_classification_results # Use the original full result
        
        # ICD Topic Details (Includes raw_data within 'codes' list)
        icd_topic_response = icd_topic_details

        # Final response structure
        final_response = {
            "record_id": record_id, # Include the record ID
            "scenario": cleaned_scenario_text,
            "CDT_classifier": cdt_classifier_response,
            "CDT_topic": cdt_topic_summary,
            "CDT_subtopic": cdt_subtopic_details,
            "ICD_classifier": icd_classifier_response,
            "ICD_topic_result": icd_topic_response,
            "questioner_data": questioner_data, # Add questioner results
            "inspector_results": inspector_results # Add inspector results
        }

        logger.info("Response construction complete.")
        return final_response

    except Exception as e:
        logger.error(f"Error during scenario processing: {e}", exc_info=True)
        # Return error in a consistent structure if possible
        return {
            "error": f"Internal server error: {str(e)}",
            "record_id": record_id, # Return record_id even if error occurred after saving
            "details": traceback.format_exc() if 'traceback' in locals() else "Traceback not available"
        }

# Add a root endpoint for basic checks
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Dental Scenario Analysis API"}

# --- Add Custom Code Endpoint (from app.py.bak) ---
@app.post("/api/add-custom-code")
async def add_custom_code(request: CustomCodeRequest):
    """Process and add a custom code for a given scenario."""
    try:
        logger.info(f"--- Adding Custom Code for Record {request.record_id} ---")
        logger.info(f"Custom code: {request.code}")
        # logger.info(f"Scenario: {request.scenario[:75]}...")
        
        # Run the custom code analysis - Assuming Add_code_data is synchronous
        # If it becomes async, use await asyncio.to_thread(Add_code_data, ...)
        analysis_result = Add_code_data(request.scenario, request.code)
        logger.info(f"Add_code_data result: {analysis_result}")
        
        # Parse the analysis result to extract components (similar to app.py.bak)
        explanation = ""
        doubt = "None"
        
        # Basic parsing logic - adjust if Add_code_data format is different
        if "Explanation:" in analysis_result:
            explanation = analysis_result.split("Explanation:")[1].strip()
            if "Doubt:" in explanation:
                parts = explanation.split("Doubt:")
                explanation = parts[0].strip()
                doubt = parts[1].strip()
        else:
            explanation = analysis_result # Assume entire result is explanation if keyword missing
        
        # Check if the code is likely applicable based on the analysis result
        # Using a case-insensitive check for robustness
        is_applicable = "applicable? yes" in analysis_result.lower()
        
        # Format the response in the expected structure
        code_data = {
            "code": request.code,
            "explanation": explanation,
            "doubt": doubt,
            "isApplicable": is_applicable
        }
        
        # Mimic the inspector structure for frontend consistency
        inspector_like_results = {
            "cdt": {
                "codes": [request.code] if is_applicable else [],
                "rejected_codes": [] if is_applicable else [request.code],
                "explanation": explanation
            },
            "icd": { # Assuming custom codes are CDT only
                "codes": [],
                "rejected_codes": [],
                "explanation": "N/A for custom CDT code analysis."
            }
        }
        
        return {
            "status": "success",
            "message": "Custom code analysis completed",
            "data": {
                "code_data": code_data,
                "inspector_results": inspector_like_results 
            }
        }
        
    except Exception as e:
        error_details = traceback.format_exc()
        logger.error(f"❌ ERROR adding custom code: {str(e)}")
        logger.error(f"STACK TRACE: {error_details}")
        return {"status": "error", "message": str(e), "details": error_details}

# --- Add Store Code Status Endpoint (from app.py.bak) ---
@app.post("/api/store-code-status")
async def store_code_status(request: CodeStatusRequest):
    """Store the final status of selected and rejected codes based on user input."""
    try:
        logger.info(f"--- Storing Code Status for Record {request.record_id} ---")
        logger.info(f"Selected CDT: {request.cdt_codes}")
        logger.info(f"Rejected CDT: {request.rejected_cdt_codes}")
        logger.info(f"Selected ICD: {request.icd_codes}")
        logger.info(f"Rejected ICD: {request.rejected_icd_codes}")
        
        # Call the new function to save selections to the dedicated table
        saved_selection = db.save_code_selections(
            record_id=request.record_id,
            accepted_cdt=request.cdt_codes,
            rejected_cdt=request.rejected_cdt_codes,
            accepted_icd=request.icd_codes,
            rejected_icd=request.rejected_icd_codes
        )

        if not saved_selection:
            logger.error(f"Failed to save code selections for record ID: {request.record_id}")
            raise HTTPException(status_code=500, detail="Failed to save code selections to database.")

        logger.info(f"Code status updated in the database for {request.record_id}")
        
        return {
            "status": "success",
            "message": "Code status updated successfully",
            "saved_selection": saved_selection # Return the data saved to the new table
        }
        
    except Exception as e:
        error_details = traceback.format_exc()
        logger.error(f"❌ ERROR storing code status: {str(e)}")
        logger.error(f"STACK TRACE: {error_details}")
        return {"status": "error", "message": str(e), "details": error_details}

# --- Application Runner ---
if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8000
    logger.info(f"Starting Uvicorn server on {host}:{port}")
    # Note: reload=True is great for development but should be False in production
    uvicorn.run("app:app", host=host, port=port, reload=True)
