from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import uvicorn
import logging
import asyncio # Add asyncio import
import os # Add os import for getenv
from fastapi.middleware.cors import CORSMiddleware # Import CORS Middleware
from data_cleaner import DentalScenarioProcessor # Import the processor
from cdt_classifier import CDTClassifier       # Import CDT Classifier
from icd_classifier import ICDClassifier       # Import ICD Classifier

# Import Topic Activation components (from backup reference)
from sub_topic_registry import SubtopicRegistry
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
from icdtopics.dentalencounters import dental_encounters_service
from icdtopics.dentalcaries import dental_caries_service
from icdtopics.disordersofteeth import teeth_disorders_service
from icdtopics.disordersofpulpandperiapicaltissues import pulp_periapical_service
from icdtopics.diseasesandconditionsoftheperiodontium import periodontium_diseases_service
from icdtopics.alveolarridgedisorders import alveolar_ridge_disorders_service
from icdtopics.findingsofbostteeth import lost_teeth_service # Corrected name? Assuming findingsoflostteeth
from icdtopics.developmentdisordersofteethandjaws import development_disorders_service
from icdtopics.treatmentcomplications import treatment_complications_service
from icdtopics.inflammatoryconditionsofthmucosa import inflammatory_mucosa_service # Corrected name? Assuming inflammatoryconditionsofthemucosa
from icdtopics.tmjdiseasesandconditions import tmj_disorders_service
from icdtopics.breathingspeechandsleepdisorders import breathing_sleep_disorders_service
from icdtopics.traumaandrelatedconditions import trauma_conditions_service
from icdtopics.oralneoplasms import oral_neoplasms_service
from icdtopics.pathologies import pathologies_service
from icdtopics.medicalfindingsrelatedtodentaltreatment import medical_findings_service
from icdtopics.socialdeterminants import social_determinants_service
from icdtopics.symptomsanddisorderspertienttoorthodontiacases import orthodontia_cases_service

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Dental Scenario Analysis API",
    description="API for analyzing dental scenarios and suggesting CDT/ICD codes.",
    version="0.1.0"
)

# Add CORS middleware (Using specific origins from backup)
origins = [
    "http://localhost:5173",
    "https://dentalcoder.vercel.app",
    "https://automed.adamtechnologies.in",
    "http://automed.adamtechnologies.in",
    os.getenv("FRONTEND_URL", "")  # Get from environment variable
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"], # Allows all headers
)

# Initialize processors/classifiers
scenario_processor = DentalScenarioProcessor()
cdt_classifier = CDTClassifier()
icd_classifier = ICDClassifier()

# Initialize Topic Registry (Combined CDT & ICD)
topic_registry = SubtopicRegistry()

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
    "6": "Alveolar Ridge Disorders", "7": "Findings of Lost Teeth",
    "8": "Developmental Disorders of Teeth and Jaws", "9": "Treatment Complications",
    "10": "Inflammatory Conditions of the Mucosa", "11": "TMJ Diseases and Conditions",
    "12": "Breathing, Speech, and Sleep Disorders", "13": "Trauma and Related Conditions",
    "14": "Oral Neoplasms", "15": "Pathologies", "16": "Medical Findings Related to Dental Treatment",
    "17": "Social Determinants", "18": "Symptoms and Disorders Pertinent to Orthodontia Cases"
}

ICD_TOPIC_MAPPING = {
    "1": {"func": dental_encounters_service.activate_dental_encounters, "name": ICD_CATEGORY_NAMES["1"]},
    "2": {"func": dental_caries_service.activate_dental_caries, "name": ICD_CATEGORY_NAMES["2"]},
    "3": {"func": teeth_disorders_service.activate_disorders_of_teeth, "name": ICD_CATEGORY_NAMES["3"]},
    "4": {"func": pulp_periapical_service.activate_pulp_periapical_disorders, "name": ICD_CATEGORY_NAMES["4"]},
    "5": {"func": periodontium_diseases_service.activate_periodontium_disorders, "name": ICD_CATEGORY_NAMES["5"]},
    "6": {"func": alveolar_ridge_disorders_service.activate_alveolar_ridge_disorders, "name": ICD_CATEGORY_NAMES["6"]},
    "7": {"func": lost_teeth_service.activate_lost_teeth, "name": ICD_CATEGORY_NAMES["7"]},
    "8": {"func": development_disorders_service.activate_development_disorders, "name": ICD_CATEGORY_NAMES["8"]},
    "9": {"func": treatment_complications_service.activate_treatment_complications, "name": ICD_CATEGORY_NAMES["9"]},
    "10": {"func": inflammatory_mucosa_service.activate_inflammatory_mucosa, "name": ICD_CATEGORY_NAMES["10"]},
    "11": {"func": tmj_disorders_service.activate_tmj_disorders, "name": ICD_CATEGORY_NAMES["11"]},
    "12": {"func": breathing_sleep_disorders_service.activate_breathing_sleep_disorders, "name": ICD_CATEGORY_NAMES["12"]},
    "13": {"func": trauma_conditions_service.activate_trauma_conditions, "name": ICD_CATEGORY_NAMES["13"]},
    "14": {"func": oral_neoplasms_service.activate_oral_neoplasms, "name": ICD_CATEGORY_NAMES["14"]},
    "15": {"func": pathologies_service.activate_pathologies, "name": ICD_CATEGORY_NAMES["15"]},
    "16": {"func": medical_findings_service.activate_medical_findings, "name": ICD_CATEGORY_NAMES["16"]},
    "17": {"func": social_determinants_service.activate_social_determinants, "name": ICD_CATEGORY_NAMES["17"]},
    "18": {"func": orthodontia_cases_service.activate_orthodontia_cases, "name": ICD_CATEGORY_NAMES["18"]}
}

# Register ICD topics using category number as the key
for category_num, topic_info in ICD_TOPIC_MAPPING.items():
    topic_registry.register(category_num, topic_info["func"], topic_info["name"])

class ScenarioInput(BaseModel):
    scenario: str

# Use a more detailed output model similar to the reference structure
class DetailedAnalysisOutput(BaseModel):
    standardized_scenario: str
    cdt_classification_results: dict # Original CDT classification results
    icd_classification_results: dict # Original ICD classification results
    cdt_topic_results: dict # Processed CDT topics/subtopics
    icd_topic_results: dict # Processed (simplified) ICD topic result

# Helper function to parse activation results (similar to reference)
def _parse_activation_result(result_text: str) -> dict:
    parsed = {"code": None, "explanation": None, "doubt": None}
    if not isinstance(result_text, str):
        return parsed
        
    current_key = None
    current_value = ""

    for line in result_text.split('\n'): # Handle escaped newlines if present
        line = line.strip()
        if not line: continue

        # More robust key detection
        if line.upper().startswith("CODE:"):
            if current_key: # Save previous key-value
                 parsed[current_key] = current_value.strip()
            current_key = "code"
            current_value = line.split(":", 1)[1].strip().strip('*')
        elif line.upper().startswith("EXPLANATION:"):
            if current_key: # Save previous key-value
                 parsed[current_key] = current_value.strip()
            current_key = "explanation"
            current_value = line.split(":", 1)[1].strip().strip('*')
        elif line.upper().startswith("DOUBT:"):
            if current_key: # Save previous key-value
                 parsed[current_key] = current_value.strip()
            current_key = "doubt"
            current_value = line.split(":", 1)[1].strip().strip('*')
        elif current_key: # Append to current value if a key is active
            current_value += " " + line # Add space for multi-line values
            
    if current_key: # Save the last key-value pair
        parsed[current_key] = current_value.strip()

    # Clean up potential "none" strings
    for key in parsed:
        if isinstance(parsed[key], str) and parsed[key].lower() == 'none':
            parsed[key] = None
            
    return parsed

@app.post("/api/analyze", response_model=DetailedAnalysisOutput) # Use updated model
async def analyze_scenario(payload: ScenarioInput):
    """
    Receives a dental scenario, cleans it, classifies CDT/ICD, 
    activates relevant CDT/ICD topics, and returns results.
    """
    logger.info(f"Received scenario for analysis: {payload.scenario[:75]}...")

    try:
        # Step 1: Clean the scenario using DentalScenarioProcessor
        logger.info("*********🔍 step 1 :Cleaning Scenario:*********************")
        cleaned_data = scenario_processor.process(payload.scenario)
        logger.info("Scenario cleaned successfully.")
        cleaned_scenario_text = cleaned_data["standardized_scenario"]

        # Step 2: Run CDT Classifier and Initial ICD Classifier concurrently
        logger.info("*********🚀 step 2: Starting Concurrent CDT & Initial ICD Classification:*********************")
        cdt_task = asyncio.to_thread(cdt_classifier.process, cleaned_scenario_text)
        icd_initial_task = asyncio.to_thread(icd_classifier.process, cleaned_scenario_text) # Initial ICD classification

        cdt_classification_results, icd_classification_results = await asyncio.gather(cdt_task, icd_initial_task)

        logger.info("CDT & Initial ICD classification completed.")

        # --- Step 3: Activate relevant CDT and ICD topics CONCURRENTLY --- 
        logger.info("*********💡 step 3: Activating Topics Concurrently:*********************")
        
        tasks = []
        topic_keys = [] # To map results back

        # Prepare CDT topic activation tasks
        if cdt_classification_results and cdt_classification_results.get("range_codes_string"):
            cdt_range_codes_str = cdt_classification_results["range_codes_string"]
            # Split the ranges and find corresponding functions
            for code_range in cdt_range_codes_str.split(','):
                code_range = code_range.strip()
                if code_range in CDT_TOPIC_MAPPING:
                    topic_info = CDT_TOPIC_MAPPING[code_range]
                    logger.info(f"Creating task for CDT Topic: {topic_info['name']}")
                    tasks.append(asyncio.create_task(topic_info["func"](cleaned_scenario_text)))
                    topic_keys.append({"type": "cdt", "key": code_range, "name": topic_info['name']})
                else:
                    logger.warning(f"CDT code range {code_range} from classifier not found in CDT_TOPIC_MAPPING.")
        else:
            logger.warning("Skipping CDT topic activation tasks due to missing/invalid classification.")

        # Prepare ICD topic activation task
        icd_category_number = icd_classification_results.get("category_number")
        if icd_category_number:
            icd_category_str = str(icd_category_number)
            if icd_category_str in ICD_TOPIC_MAPPING:
                topic_info = ICD_TOPIC_MAPPING[icd_category_str]
                logger.info(f"Creating task for ICD Topic: {topic_info['name']}")
                tasks.append(asyncio.create_task(topic_info["func"](cleaned_scenario_text)))
                topic_keys.append({"type": "icd", "key": icd_category_str, "name": topic_info['name']})
            else:
                 logger.warning(f"ICD category number {icd_category_str} not found in ICD_TOPIC_MAPPING.")
        else:
             logger.warning("Skipping ICD topic activation task due to missing/invalid classification.")

        # Run all topic activation tasks concurrently
        cdt_topic_results = {} # Initialize final structures
        processed_icd_topic_results = {}
        
        if tasks:
            logger.info(f"Running {len(tasks)} topic activation tasks concurrently...")
            topic_results_raw = await asyncio.gather(*tasks, return_exceptions=True)
            logger.info("Concurrent topic activation completed.")

            # Process the results
            cdt_topic_list_for_response = [] # Store individual topic results for CDT
            for i, result in enumerate(topic_results_raw):
                key_info = topic_keys[i]
                topic_type = key_info["type"]
                topic_key = key_info["key"]
                topic_name = key_info["name"]

                if isinstance(result, Exception):
                    logger.error(f"Error activating topic {topic_name} ({topic_key}): {result}")
                    error_result = {"error": f"Activation failed for {topic_name}: {str(result)}"}
                    if topic_type == "cdt":
                        # Add error entry specific to this topic
                        cdt_topic_list_for_response.append({
                            "topic": topic_name,
                            "code_range": topic_key,
                            **error_result
                        })
                    elif topic_type == "icd":
                        processed_icd_topic_results = error_result
                elif isinstance(result, dict):
                    logger.info(f"Successfully activated topic: {topic_name}")
                    if topic_type == "cdt":
                        # Add the structured result from the topic activation function
                        result['topic'] = topic_name # Ensure topic name is present
                        cdt_topic_list_for_response.append(result)
                    elif topic_type == "icd":
                        # For ICD, we want the simplified structure
                        # The ICD topic activation function should ideally return the standard dict 
                        # with explanation, doubt, code_range, activated_subtopics, codes.
                        # We parse the *subtopic* result here for the final format.
                        icd_subtopic_codes = result.get("codes", [])
                        parsed_icd_code = None
                        parsed_icd_explanation = None
                        parsed_icd_doubt = None
                        
                        if icd_subtopic_codes and isinstance(icd_subtopic_codes, list) and icd_subtopic_codes[0]:
                            # Assuming the first code entry from the subtopic activation holds the primary code
                            # This relies on the ICD subtopic functions returning a parseable structure
                            first_code_entry = icd_subtopic_codes[0]
                            if isinstance(first_code_entry, dict): # Check if it's a dict
                                raw_text_to_parse = first_code_entry.get('result', '') or first_code_entry.get('raw_text', '')
                                if raw_text_to_parse:
                                    parsed_data = _parse_activation_result(raw_text_to_parse) # Use helper from app.py
                                    parsed_icd_code = parsed_data.get('code')
                                    parsed_icd_explanation = parsed_data.get('explanation')
                                    parsed_icd_doubt = parsed_data.get('doubt')
                                elif 'code' in first_code_entry: # Fallback if already parsed
                                    parsed_icd_code = first_code_entry.get('code')
                                    parsed_icd_explanation = first_code_entry.get('explanation')
                                    parsed_icd_doubt = first_code_entry.get('doubt')
                                else:
                                     logger.warning(f"Could not parse ICD subtopic result for {topic_name}. Raw subtopic result: {first_code_entry}")
                            else:
                                logger.warning(f"Unexpected format for ICD subtopic code entry: {first_code_entry}")
                        else:
                             logger.warning(f"No valid codes found in ICD topic result for {topic_name}. Raw topic result: {result}")
                             
                        processed_icd_topic_results = {
                            "category": topic_name,
                            "code": parsed_icd_code,
                            "explanation": parsed_icd_explanation,
                            "doubt": parsed_icd_doubt,
                            "raw_topic_result": result # Keep raw topic result for debug if needed
                        }
                        logger.info(f"Processed ICD Topic Result: Code={processed_icd_topic_results.get('code')}")
                else:
                    logger.warning(f"Unexpected result type for topic {topic_name}: {type(result)}")
                    error_result = {"error": f"Unexpected result type for {topic_name}: {type(result)}"}
                    if topic_type == "cdt":
                         cdt_topic_list_for_response.append({
                            "topic": topic_name,
                            "code_range": topic_key,
                            **error_result
                        })
                    elif topic_type == "icd":
                        processed_icd_topic_results = error_result

            # Structure the final CDT results (mimics the old raw_cdt_topic_results structure somewhat)
            # Combine activated subtopics from all successful CDT results
            all_activated_cdt_subtopics = set()
            for res in cdt_topic_list_for_response:
                if isinstance(res, dict) and not res.get("error"):
                    all_activated_cdt_subtopics.update(res.get("activated_subtopics", []))
            
            cdt_topic_results = {
                "topic_result": cdt_topic_list_for_response, # List of results from each activated CDT topic
                "activated_subtopics": sorted(list(all_activated_cdt_subtopics)) # Consolidated list
            }

        else:
            logger.warning("No topic activation tasks were created.")
            cdt_topic_results = {"error": "No CDT topics activated."}
            processed_icd_topic_results = {"error": "No ICD topic activated."}
        
        # --- End of Concurrent Activation --- 

        # Placeholder for subsequent analysis steps (e.g., Questioner, Inspector)

        # Return using the new detailed model structure
        return DetailedAnalysisOutput(
            standardized_scenario=cleaned_scenario_text,
            cdt_classification_results=cdt_classification_results, # Pass original classification
            icd_classification_results=icd_classification_results, # Pass original classification
            cdt_topic_results=cdt_topic_results, # Pass the structured CDT topic results
            icd_topic_results=processed_icd_topic_results # Pass the processed ICD topic result
        )

    except Exception as e:
        logger.error(f"Error during scenario processing: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Add a root endpoint for basic checks
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Dental Scenario Analysis API"}

# --- Application Runner ---
if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8000
    logger.info(f"Starting Uvicorn server on {host}:{port}")
    # Note: reload=True is great for development but should be False in production
    uvicorn.run("app:app", host=host, port=port, reload=True)
