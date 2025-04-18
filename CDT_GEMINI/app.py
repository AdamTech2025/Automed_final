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

# Import Topic Activation components
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
    activates relevant CDT/ICD topics, and returns results in the requested format.
    """
    logger.info(f"Received scenario for analysis: {payload.scenario[:75]}...")

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

        # --- Construct the final response --- 
        logger.info("*********🔧 step 4: Constructing Final Response:*********************")

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
            "scenario": cleaned_scenario_text,
            "CDT_classifier": cdt_classifier_response,
            "CDT_topic": cdt_topic_summary,
            "CDT_subtopic": cdt_subtopic_details,
            "ICD_classifier": icd_classifier_response,
            "ICD_topic_result": icd_topic_response
        }

        logger.info("Response construction complete.")
        return final_response

    except Exception as e:
        logger.error(f"Error during scenario processing: {e}", exc_info=True)
        # Return error in a consistent structure if possible
        return {
            "error": f"Internal server error: {str(e)}",
            "details": traceback.format_exc() if 'traceback' in locals() else "Traceback not available"
        }

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
