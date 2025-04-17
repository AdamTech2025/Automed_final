﻿from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import asyncio
from typing import Dict, Any, List
import json
import datetime
import time  # Import the time module

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
        if base_code[2:4] < "90":
            return "D5000-D5899"
        else:
            return "D5900-D5999"
    elif category_prefix == "D6":
        # Check if it's in the range D6000-D6199 or D6200-D6999
        if base_code[2:4] < "20":
            return "D6000-D6199"
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

# API endpoint to process user input
@app.post("/api/analyze")
async def analyze_web(request: ScenarioRequest):
    """Process the dental scenario through the data cleaner, CDT classifier, and topic activators."""
    start_time = time.time()
    try:
        # Step 1: Process the input through data_cleaner
        step_start_time = time.time()
        print("\n*************************** STEP 1: DATA CLEANING ***************************")
        print(f"🔍 INPUT SCENARIO: {request.scenario}")
        processed_result = cleaner.process(request.scenario)
        processed_scenario = processed_result["standardized_scenario"]
        print(f"✅ PROCESSED SCENARIO: {processed_scenario}")
        print(f"⏱️ Data Cleaning Time: {time.time() - step_start_time:.2f} seconds")
        
        # Step 2: Process the cleaned scenario with CDT and ICD classifiers in parallel
        step_start_time = time.time()
        print("\n*************************** STEP 2: PARALLEL CLASSIFICATION ***************************")
        print(f"⏳ RUNNING CDT & ICD CLASSIFICATION IN PARALLEL...")
        
        # Create async tasks for parallel execution
        async def run_cdt_classification():
            return cdt_classifier.process(processed_scenario)
            
        async def run_icd_classification():
            return icd_classifier.process(processed_scenario)
        
        # Run both classifications in parallel
        cdt_task = asyncio.create_task(run_cdt_classification())
        icd_task = asyncio.create_task(run_icd_classification())
        
        # Await both results
        cdt_result, icd_result = await asyncio.gather(cdt_task, icd_task)
        
        print(f"⏱️ Parallel Classification Time: {time.time() - step_start_time:.2f} seconds")
        
        # Log CDT results
        print(f"🏆 CDT CLASSIFICATION COMPLETE with {len(cdt_result.get('formatted_results', []))} code ranges")
        
        # Log ICD results
        if "error" in icd_result and icd_result["error"]:
            print(f"❌ ICD CLASSIFICATION ERROR: {icd_result['error']}")
        else:
            print(f"🏆 ICD CLASSIFICATION COMPLETE with {len(icd_result.get('categories', []))} categories")
            if icd_result.get("icd_codes"):
                print(f"📋 ICD CODES IDENTIFIED: {', '.join(icd_result.get('icd_codes', []))}")
        
        # Step 3: Activate topics in parallel based on code ranges
        step_start_time = time.time()
        print("\n*************************** STEP 3: TOPIC ACTIVATION ***************************")
        print(f"⚡ ACTIVATING TOPICS IN PARALLEL...")
        range_codes = cdt_result["range_codes_string"].split(",")
        
        # Process code ranges to get the standardized categories
        category_ranges = set()
        for range_code in range_codes:
            category = map_to_cdt_category(range_code.strip())
            if category:
                category_ranges.add(category)
        
        # Convert to comma-separated string for the registry
        category_ranges_str = ",".join(category_ranges)
        
        # Run all relevant topics in parallel
        topic_results = await topic_registry.activate_all(processed_scenario, category_ranges_str)
        
        # Make sure we have valid data structures
        activated_subtopics = topic_results.get('activated_subtopics', [])
        topic_result = topic_results.get('topic_result', [])
        print(f"🎯 TOPICS ACTIVATED: {activated_subtopics}")
        print(f"📋 SPECIFIC CODES IDENTIFIED: {len(topic_result)}")
        print(f"⏱️ Topic Activation Time: {time.time() - step_start_time:.2f} seconds")
        
        # Step 4: Process results for response
        step_start_time = time.time()
        print("\n*************************** STEP 4: PROCESSING RESULTS ***************************")
        
        # Process the CDT classification data for better structure
        formatted_cdt_results = []
        for result in cdt_result.get("formatted_results", []):
            formatted_result = {
                "code_range": result.get("code_range", ""),
                "explanation": result.get("explanation", ""),
                "doubt": result.get("doubt", "")
            }
            formatted_cdt_results.append(formatted_result)
        
        # Process topic_result to extract codes by subtopic for the response
        subtopic_data = {}
        for topic_item in topic_result:
            topic_name = topic_item.get("topic", "Unknown")
            if "codes" in topic_item:
                for subtopic_code in topic_item["codes"]:
                    subtopic_name = subtopic_code.get("topic", "Unknown Subtopic")
                    code_range = subtopic_code.get("code_range", "")
                    subtopic_key = f"{subtopic_name} ({code_range})"
                    
                    if "codes" in subtopic_code:
                        codes_list = []
                        for code_entry in subtopic_code["codes"]:
                            code = code_entry.get("code", "Unknown")
                            # Clean up code value
                            if isinstance(code, str):
                                if " - " in code:
                                    code = code.split(" - ")[0].strip()
                            
                            explanation = code_entry.get("explanation", "")
                            doubt = code_entry.get("doubt", "")
                            
                            codes_list.append({
                                "code": code,
                                "explanation": explanation,
                                "doubt": doubt
                            })
                        
                        if subtopic_key not in subtopic_data:
                            subtopic_data[subtopic_key] = []
                        subtopic_data[subtopic_key].extend(codes_list)
        
        # Remove codes arrays from topic_result to avoid duplication
        cleaned_topic_result = []
        for topic_item in topic_result:
            # Create a copy without the codes array
            cleaned_item = {
                "topic": topic_item.get("topic", "Unknown"),
                "code_range": topic_item.get("code_range", ""),
                "activated_subtopics": topic_item.get("activated_subtopics", [])
            }
            cleaned_topic_result.append(cleaned_item)
        
        # Format the topics data for response
        topics_data = {}
        for code_range in category_ranges:
            if code_range in CDT_TOPIC_MAPPING:
                topic_name = CDT_TOPIC_MAPPING[code_range]["name"]
                topics_data[code_range] = {
                    "name": topic_name,
                    "activated": topic_name in activated_subtopics
                }
        
        # Save data to database
        print("\n*************************** SAVING TO DATABASE ***************************")
        try:
            # Filter out activated_subtopics from topic_result for database
            db_topic_result = []
            for topic_item in cleaned_topic_result:
                # Create a copy without the activated_subtopics
                filtered_item = {
                    "topic": topic_item.get("topic", "Unknown"),
                    "code_range": topic_item.get("code_range", "")
                    # Removed activated_subtopics
                }
                db_topic_result.append(filtered_item)
            
            # Prepare the complete CDT result data with all components
            complete_cdt_data = {
                "cdt_classification": {
                    "CDT_classifier": formatted_cdt_results,
                },
                "topics_results": {
                    "topic_result": db_topic_result, 
                    "subtopic_data": subtopic_data
                }
            }
            
            # Prepare the complete ICD result data - ensuring all keys exist and have valid values
            complete_icd_data = {}
            
            # Check if icd_result exists and is not None
            if icd_result is not None:
                # Get primary category and topic result for simplified version
                primary_icd_code = ""
                primary_explanation = ""
                primary_doubt = ""
                
                # Extract from topics_results if available
                if "icd_topics_results" in icd_result and icd_result["icd_topics_results"]:
                    if "category_numbers_string" in icd_result and icd_result["category_numbers_string"]:
                        primary_category = icd_result["category_numbers_string"].split(",")[0]
                        if primary_category in icd_result["icd_topics_results"]:
                            topic_data = icd_result["icd_topics_results"][primary_category]
                            if "parsed_result" in topic_data:
                                parsed = topic_data["parsed_result"]
                                primary_icd_code = parsed.get("code", "")
                                primary_explanation = parsed.get("explanation", "")
                                primary_doubt = parsed.get("doubt", "")
                
                # If still no data, try categories
                if not primary_icd_code and "categories" in icd_result and icd_result["categories"]:
                    category_index = 0
                    if "icd_codes" in icd_result and len(icd_result["icd_codes"]) > category_index:
                        primary_icd_code = icd_result["icd_codes"][category_index]
                    if "explanations" in icd_result and len(icd_result["explanations"]) > category_index:
                        primary_explanation = icd_result["explanations"][category_index]
                    if "doubts" in icd_result and len(icd_result["doubts"]) > category_index:
                        primary_doubt = icd_result["doubts"][category_index]
                
                # Store both the full data and a simplified version
                complete_icd_data = {
                    "simplified": {
                        "code": primary_icd_code,
                        "explanation": primary_explanation,
                        "doubt": primary_doubt
                    }
                }
                
                print(f"⏳ Prepared ICD data for storage with primary code: {primary_icd_code}")
            else:
                print("⚠️ No ICD result data available to save")
                complete_icd_data = {"error": "No ICD data available"}
            
            # Check data sizes
            cdt_json = json.dumps(complete_cdt_data)
            icd_json = json.dumps(complete_icd_data)
            print(f"💾 CDT data size: {len(cdt_json)} bytes")
            print(f"💾 ICD data size: {len(icd_json)} bytes")
            
            # Prepare data for database storage
            db_data = {
                "user_question": request.scenario,  # Original user question
                "processed_clean_data": processed_scenario,  # Cleaned data
                "cdt_result": cdt_json,  # Complete CDT result data
                "icd_result": icd_json   # Complete ICD result data
            }
            
            # Save to database
            db_result = db.create_analysis_record(db_data)
            record_id = None
            if db_result:
                record_id = db_result[0]["id"]
                print(f"✅ Data saved to database successfully with ID: {record_id}")
                print(f"  - CDT data size: {len(db_data['cdt_result'])} bytes")
                print(f"  - ICD data size: {len(db_data['icd_result'])} bytes")
            else:
                print("❌ Failed to save data to database")
            
            # Step 5: Generate questions with the Questioner module
            print("\n*************************** STEP 5: QUESTIONER ANALYSIS ***************************")
            questioner_result = None
            if record_id:
                try:
                    # Format simplified data for the questioner
                    simplified_cdt_data = {
                        "code_ranges": cdt_result.get("range_codes_string", ""),
                        "activated_subtopics": activated_subtopics,
                        "subtopics": ", ".join(list(subtopic_data.keys())) if subtopic_data else "None",
                        "formatted_cdt_results": [
                            f"{res.get('code_range')}: {res.get('explanation')}" 
                            for res in formatted_cdt_results
                        ]
                    }
                    
                    # Format ICD data for questioner
                    primary_icd = complete_icd_data.get("simplified", {})
                    simplified_icd_data = {
                        "code": primary_icd.get("code", ""),
                        "explanation": primary_icd.get("explanation", ""),
                        "doubt": primary_icd.get("doubt", "")
                    }
                    
                    # Generate questions using the questioner module
                    print("⏳ Generating questions for the scenario...")
                    questioner_result = questioner.process(
                        processed_scenario, 
                        simplified_cdt_data, 
                        simplified_icd_data
                    )
                    
                    # Log the results
                    if questioner_result["has_questions"]:
                        print(f"✅ Generated {len(questioner_result['cdt_questions']['questions'])} CDT questions and {len(questioner_result['icd_questions']['questions'])} ICD questions")
                        
                        # Save questioner data to the database
                        questioner_json = json.dumps(questioner_result)
                        db.update_questioner_data(record_id, questioner_json)
                        print(f"✅ Saved questioner data to database for record ID: {record_id}")
                    else:
                        print("✅ No questions needed for this scenario")
                        
                        # Save empty questioner data to the database
                        db.update_questioner_data(record_id, json.dumps(questioner_result))
                        print(f"✅ Saved empty questioner data to database for record ID: {record_id}")
                        
                        # Since no questions are needed, proceed directly to inspectors
                        print("✅ Proceeding directly to inspector step...")
                        inspector_result = await run_inspectors(record_id)
                        print(f"✅ Inspector step complete without questions")
                    
                except Exception as e:
                    import traceback
                    error_details = traceback.format_exc()
                    print(f"❌ Error in questioner processing: {str(e)}")
                    print(f"STACK TRACE: {error_details}")
                    questioner_result = {
                        "cdt_questions": {"questions": [], "explanation": f"Error occurred: {str(e)}", "has_questions": False},
                        "icd_questions": {"questions": [], "explanation": f"Error occurred: {str(e)}", "has_questions": False},
                        "has_questions": False
                    }
            else:
                print("⚠️ Skipping questioner step - no record ID available")
                questioner_result = {
                    "cdt_questions": {"questions": [], "explanation": "No record ID", "has_questions": False},
                    "icd_questions": {"questions": [], "explanation": "No record ID", "has_questions": False},
                    "has_questions": False
                }
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"❌ Database error: {str(e)}")
            print(f"STACK TRACE: {error_details}")
            # Continue with API response even if database save fails
        
        # Step 6: Prepare final response
        print("\n*************************** STEP 6: PREPARING RESPONSE ***************************")
        
        # Extract ICD data with a more robust approach - using only code, explanation, and doubt
        simplified_icd_data = {
            "code": "",
            "explanation": "",
            "doubt": ""
        }
        
        # First, try to get data from icd_topics_results if available
        if icd_result and "icd_topics_results" in icd_result and icd_result["icd_topics_results"]:
            # Get the first category
            if "category_numbers_string" in icd_result and icd_result["category_numbers_string"]:
                categories = icd_result["category_numbers_string"].split(",")
                if categories and categories[0] in icd_result["icd_topics_results"]:
                    category_data = icd_result["icd_topics_results"][categories[0]]
                    if "parsed_result" in category_data:
                        parsed = category_data["parsed_result"]
                        if "code" in parsed:
                            simplified_icd_data["code"] = parsed["code"]
                        if "explanation" in parsed:
                            simplified_icd_data["explanation"] = parsed["explanation"]
                        if "doubt" in parsed:
                            simplified_icd_data["doubt"] = parsed["doubt"]
        
        # If no data found yet, try categories
        if not simplified_icd_data["code"] and "categories" in icd_result and icd_result["categories"]:
            category_index = 0
            simplified_icd_data["code"] = (
                icd_result["icd_codes"][category_index] if "icd_codes" in icd_result and len(icd_result["icd_codes"]) > category_index else ""
            )
            simplified_icd_data["explanation"] = (
                icd_result["explanations"][category_index] if "explanations" in icd_result and len(icd_result["explanations"]) > category_index else ""
            )
            simplified_icd_data["doubt"] = (
                icd_result["doubts"][category_index] if "doubts" in icd_result and len(icd_result["doubts"]) > category_index else ""
            )
        
        # Log what we're returning for debugging
        print(f"🏥 ICD DATA - CODE: {simplified_icd_data['code']}")
        print(f"🏥 ICD DATA - EXPLANATION: {simplified_icd_data['explanation'][:100]}...")
        
        # Get the most up-to-date inspector results from database
        inspector_results = {"cdt_inspector": {}, "icd_inspector": {}}
        if record_id:
            try:
                # Try to get the latest data from the database with inspector results
                latest_analysis = db.get_complete_analysis(record_id)
                if latest_analysis:
                    # Check if we have dedicated inspector_results column data
                    if 'inspector_results' in latest_analysis and latest_analysis['inspector_results']:
                        # Parse the inspector_results JSON
                        inspector_data = json.loads(latest_analysis['inspector_results'])
                        inspector_results = inspector_data
                        print(f"✅ Retrieved inspector results from dedicated column")
                    else:
                        # Fall back to the old method for backward compatibility
                        latest_cdt_data = json.loads(latest_analysis.get("cdt_result", "{}"))
                        latest_icd_data = json.loads(latest_analysis.get("icd_result", "{}"))
                        
                        # Extract inspector data
                        cdt_inspector = latest_cdt_data.get("inspector_results", {})
                        icd_inspector = latest_icd_data.get("inspector_results", {})
                        
                        # Format for the frontend
                        inspector_results = {
                            "cdt": {
                                "codes": cdt_inspector.get("codes", []),
                                "rejected_codes": cdt_inspector.get("rejected_codes", []),
                                "explanation": cdt_inspector.get("explanation", "")
                            },
                            "icd": {
                                "codes": icd_inspector.get("codes", []),
                                "explanation": icd_inspector.get("explanation", "")
                            }
                        }
                        print(f"✅ Retrieved inspector results from CDT/ICD data (legacy method)")
            except Exception as e:
                print(f"⚠️ Error retrieving inspector results: {str(e)}")
                inspector_results = {
                    "cdt": {"codes": [], "rejected_codes": [], "explanation": ""},
                    "icd": {"codes": [], "explanation": ""}
                }
        
        # Prepare a clean response that is JSON-serializable and properly structured
        response_data = {
            "record_id": record_id,
            "processed_scenario": processed_scenario,
            "cdt_classification": {
                "CDT_classifier": formatted_cdt_results,
                "range_codes_string": cdt_result.get("range_codes_string", "")
            },
            "topics_results": {
                "activated_subtopics": activated_subtopics,
                "topic_result": cleaned_topic_result,
                "subtopic_data": subtopic_data
            },
            "icd_classification": simplified_icd_data,
            "questioner_data": questioner_result,          
            "inspector_results": inspector_results
        }
        
        print("\n*************************** PROCESSING COMPLETE ***************************")
        
        total_time = time.time() - start_time
        print(f"⏱️ TOTAL analyze_web TIME: {total_time:.2f} seconds")
        
        return {
            "status": "success",
            "data": response_data
        }
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print("\n*************************** ERROR OCCURRED ***************************")
        print(f"❌ ERROR: {str(e)}")
        print(f"STACK TRACE: {error_details}")
        return {
            "status": "error",
            "message": str(e),
            "details": error_details
        }

@app.get("/")
def test():
    return {"message": "Dental Code Extractor API is running"}

# Endpoint for submitting answers to questions
@app.post("/api/answer-questions/{record_id}")
async def submit_question_answers(record_id: str, request: QuestionAnswersRequest):
    """Process the answers to questions and update the analysis."""
    try:
        print(f"\n*************************** PROCESSING ANSWERS FOR RECORD {record_id} ***************************")
        print(f"Received answers: {request.answers}")
        
        # Get the existing analysis from the database
        analysis = db.get_complete_analysis(record_id)
        if not analysis:
            return {
                "status": "error",
                "message": f"No analysis found with ID: {record_id}"
            }
        
        # Parse the answers JSON
        answers = json.loads(request.answers)
        
        # Update the questioner data with the answers
        questioner_data = json.loads(analysis.get("questioner_data", "{}"))
        if not questioner_data:
            return {
                "status": "error",
                "message": "No questioner data found for this analysis"
            }
        
        # Add the answers to the questioner data
        questioner_data["answers"] = answers
        questioner_data["answered"] = True
        questioner_data["has_answers"] = True
        
        # Update the database
        db.update_questioner_data(record_id, json.dumps(questioner_data))
        
        print(f"✅ Updated questioner data with answers for record ID: {record_id}")
        
        # Proceed to inspector step after answers are saved
        inspector_result = await run_inspectors(record_id)
        
        # Get the complete updated record data for response
        complete_data = db.get_complete_analysis(record_id)
        if not complete_data:
            return {
                "status": "error",
                "message": f"Failed to retrieve complete analysis for record ID: {record_id}"
            }
        
        # Parse all the necessary JSON data
        cdt_result = json.loads(complete_data.get("cdt_result", "{}"))
        icd_result = json.loads(complete_data.get("icd_result", "{}"))
        updated_questioner_data = json.loads(complete_data.get("questioner_data", "{}"))
        
        # Get inspector results with proper structure
        inspector_results = {}
        if 'inspector_results' in complete_data and complete_data['inspector_results']:
            inspector_results = json.loads(complete_data['inspector_results'])
        else:
            # Fallback to legacy method if needed
            cdt_inspector = cdt_result.get("inspector_results", {})
            icd_inspector = icd_result.get("inspector_results", {})
            
            inspector_results = {
                "cdt": {
                    "codes": cdt_inspector.get("codes", []),
                    "rejected_codes": cdt_inspector.get("rejected_codes", []),
                    "explanation": cdt_inspector.get("explanation", "")
                },
                "icd": {
                    "codes": icd_inspector.get("codes", []),
                    "explanation": icd_inspector.get("explanation", "")
                },
                "timestamp": str(datetime.datetime.now())
            }
        
        # Extract CDT classification data
        cdt_classification = cdt_result.get("cdt_classification", {})
        
        # Extract topics results data
        topics_results = cdt_result.get("topics_results", {})
        
        # Extract ICD classification data
        icd_classification = {}
        if "simplified" in icd_result:
            icd_classification = icd_result["simplified"]
        
        # Prepare the complete response data structure
        response_data = {
            "record_id": record_id,
            "processed_scenario": complete_data.get("processed_clean_data", ""),
            "cdt_classification": cdt_classification,
            "topics_results": topics_results,
            "icd_classification": icd_classification,
            "questioner_data": updated_questioner_data,
            "inspector_results": inspector_results
        }
        
        # Return the complete response data
        return {
            "status": "success",
            "data": response_data
        }
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"❌ ERROR: {str(e)}")
        print(f"STACK TRACE: {error_details}")
        return {
            "status": "error",
            "message": str(e),
            "details": error_details
        }

# Endpoint to run inspectors directly
@app.get("/api/run-inspectors/{record_id}")
async def trigger_inspectors(record_id: str):
    """Run both CDT and ICD inspectors for a given record."""
    try:
        inspector_result = await run_inspectors(record_id)
        
        # Get complete record data for response
        complete_data = db.get_complete_analysis(record_id)
        if not complete_data:
            return {
                "status": "error",
                "message": f"Failed to retrieve complete analysis for record ID: {record_id}"
            }
        
        # Parse all the necessary JSON data
        cdt_result = json.loads(complete_data.get("cdt_result", "{}"))
        icd_result = json.loads(complete_data.get("icd_result", "{}"))
        questioner_data = json.loads(complete_data.get("questioner_data", "{}"))
        
        # Get inspector results with proper structure
        inspector_results = {}
        if 'inspector_results' in complete_data and complete_data['inspector_results']:
            inspector_results = json.loads(complete_data['inspector_results'])
            print(f"✅ Retrieved inspector results from dedicated column")
        else:
            # Fallback to legacy method if needed
            cdt_inspector = cdt_result.get("inspector_results", {})
            icd_inspector = icd_result.get("inspector_results", {})
            
            inspector_results = {
                "cdt": {
                    "codes": cdt_inspector.get("codes", []),
                    "rejected_codes": cdt_inspector.get("rejected_codes", []),
                    "explanation": cdt_inspector.get("explanation", "")
                },
                "icd": {
                    "codes": icd_inspector.get("codes", []),
                    "explanation": icd_inspector.get("explanation", "")
                },
                "timestamp": str(datetime.datetime.now())
            }
            print(f"✅ Retrieved inspector results from CDT/ICD data (legacy method)")
        
        # Extract CDT classification data
        cdt_classification = cdt_result.get("cdt_classification", {})
        
        # Extract topics results data
        topics_results = cdt_result.get("topics_results", {})
        
        # Extract ICD classification data
        icd_classification = {}
        if "simplified" in icd_result:
            icd_classification = icd_result["simplified"]
        
        # Prepare the complete response data structure
        response_data = {
            "record_id": record_id,
            "processed_scenario": complete_data.get("processed_clean_data", ""),
            "cdt_classification": cdt_classification,
            "topics_results": topics_results,
            "icd_classification": icd_classification,
            "questioner_data": questioner_data,
            "inspector_results": inspector_results
        }
        
        return {
            "status": "success",
            "data": response_data
        }
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"❌ ERROR: {str(e)}")
        print(f"STACK TRACE: {error_details}")
        return {
            "status": "error",
            "message": str(e),
            "details": error_details
        }

async def run_inspectors(record_id: str):
    """Run both CDT and ICD inspectors in parallel for a given record."""
    print(f"\n*************************** RUNNING INSPECTORS FOR RECORD {record_id} ***************************")
    
    # Get the required data from the database
    analysis = db.get_complete_analysis(record_id)
    if not analysis:
        raise ValueError(f"No analysis found with ID: {record_id}")
    
    processed_scenario = analysis.get("processed_clean_data", "")
    cdt_result = json.loads(analysis.get("cdt_result", "{}"))
    icd_result = json.loads(analysis.get("icd_result", "{}"))
    questioner_data = json.loads(analysis.get("questioner_data", "{}"))
    
    # Check if we need to proceed with inspectors
    if questioner_data.get("has_questions", False) and not questioner_data.get("has_answers", False):
        print("⚠️ Questions exist but have not been answered yet - skipping inspectors")
        return {
            "status": "pending_answers",
            "message": "Questions need to be answered before running inspectors",
            "cdt_inspector": None,
            "icd_inspector": None
        }
    
    # Format data for CDT inspector - proper dictionary format expected
    cdt_topic_analysis = {}
    if cdt_result and "topics_results" in cdt_result:
        topic_results = cdt_result["topics_results"]
        # Format topic data for inspector
        if "topic_result" in topic_results and isinstance(topic_results["topic_result"], list):
            for topic in topic_results["topic_result"]:
                topic_name = topic.get("topic", "Unknown")
                code_range = topic.get("code_range", "")
                if code_range:
                    cdt_topic_analysis[code_range] = {
                        "name": topic_name,
                        "result": code_range
                    }
        
        # Add subtopic data - this is the key part that needs improvement
        if "subtopic_data" in topic_results and isinstance(topic_results["subtopic_data"], dict):
            for subtopic_key, codes in topic_results["subtopic_data"].items():
                # Format the codes list for better readability by the inspector
                formatted_codes = []
                for code_entry in codes:
                    code = code_entry.get("code", "")
                    explanation = code_entry.get("explanation", "")
                    doubt = code_entry.get("doubt", "")
                    
                    formatted_code = f"CODE: {code}\nEXPLANATION: {explanation}"
                    if doubt:
                        formatted_code += f"\nDOUBT: {doubt}"
                    
                    formatted_codes.append(formatted_code)
                
                formatted_result = "\n\n".join(formatted_codes)
                
                if subtopic_key not in cdt_topic_analysis:
                    cdt_topic_analysis[subtopic_key] = {
                        "name": subtopic_key,
                        "result": formatted_result
                    }
                else:
                    # Append to existing result
                    existing_result = cdt_topic_analysis[subtopic_key].get("result", "")
                    cdt_topic_analysis[subtopic_key]["result"] = f"{existing_result}\n\n{formatted_result}"
            
            # Add a special entry for all candidate codes for easier extraction
            all_candidate_codes = []
            for subtopic_key, codes in topic_results["subtopic_data"].items():
                for code_entry in codes:
                    code = code_entry.get("code", "")
                    if code and code.lower() != 'none' and code != 'Unknown':
                        # Clean the code value if needed
                        if isinstance(code, str):
                            if " - " in code:
                                code = code.split(" - ")[0].strip()
                        all_candidate_codes.append(code)
            
            if all_candidate_codes:
                cdt_topic_analysis["_all_candidate_codes"] = {
                    "name": "All Candidate Codes",
                    "result": "CODES: " + ", ".join(all_candidate_codes)
                }
    
    # Format data for ICD inspector
    icd_topic_analysis = {}
    if icd_result and "simplified" in icd_result:
        simplified = icd_result["simplified"]
        icd_topic_analysis["1"] = {
            "name": "Primary ICD Code",
            "result": f"CODE: {simplified.get('code', '')}\nEXPLANATION: {simplified.get('explanation', '')}\nDOUBT: {simplified.get('doubt', '')}",
            "parsed_result": {
                "code": simplified.get("code", ""),
                "explanation": simplified.get("explanation", ""),
                "doubt": simplified.get("doubt", "")
            }
        }
    
    # Define async functions for parallel execution
    async def run_cdt_inspector():
        print("⏳ Running CDT Inspector...")
        try:
            return cdt_inspector.process(processed_scenario, cdt_topic_analysis, questioner_data)
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"❌ Error in CDT inspector: {str(e)}")
            print(f"STACK TRACE: {error_details}")
            return {
                "error": str(e),
                "codes": [],
                "rejected_codes": [],
                "explanation": f"Error occurred: {str(e)}"
            }
        
    async def run_icd_inspector():
        print("⏳ Running ICD Inspector...")
        try:
            return icd_inspector.process(processed_scenario, icd_topic_analysis, questioner_data)
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"❌ Error in ICD inspector: {str(e)}")
            print(f"STACK TRACE: {error_details}")
            return {
                "error": str(e),
                "codes": [],
                "explanation": f"Error occurred: {str(e)}"
            }
    
    # Run both inspectors in parallel
    cdt_inspector_task = asyncio.create_task(run_cdt_inspector())
    icd_inspector_task = asyncio.create_task(run_icd_inspector())
    
    # Await both results
    cdt_inspector_result, icd_inspector_result = await asyncio.gather(cdt_inspector_task, icd_inspector_task)
    
    # Log the results
    cdt_codes = cdt_inspector_result.get("codes", [])
    icd_codes = icd_inspector_result.get("codes", [])
    
    print(f"✅ CDT INSPECTOR COMPLETE - Found {len(cdt_codes)} validated codes")
    print(f"✅ ICD INSPECTOR COMPLETE - Found {len(icd_codes)} validated codes")
    
    # Save inspector results to the database
    inspector_results = {
        "cdt": cdt_inspector_result,
        "icd": icd_inspector_result,
        "timestamp": str(datetime.datetime.now())
    }
    
    # Save to the dedicated inspector_results column
    try:
        # Save the inspector results to the dedicated column
        db.update_inspector_results(record_id, json.dumps(inspector_results))
        print(f"✅ Saved inspector results to database for record ID: {record_id}")
        
        # For backward compatibility, also update the existing fields
        # This can be removed later when all code is migrated to use the dedicated column
        cdt_data = json.loads(analysis.get("cdt_result", "{}"))
        cdt_data["inspector_results"] = cdt_inspector_result
        
        icd_data = json.loads(analysis.get("icd_result", "{}"))
        icd_data["inspector_results"] = icd_inspector_result
        
        db.update_analysis_results(
            record_id, 
            json.dumps(cdt_data), 
            json.dumps(icd_data)
        )
    except Exception as e:
        print(f"❌ Error saving inspector results: {str(e)}")
    
    return {
        "status": "success",
        "inspector_results": inspector_results
    }

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
        
        # Parse the existing CDT result data
        cdt_result = json.loads(analysis.get("cdt_result", "{}"))
        
        # Add the custom code analysis to the inspector results
        if "inspector_results" not in cdt_result:
            cdt_result["inspector_results"] = {}
        
        # Check if the code is likely applicable based on the analysis result
        is_applicable = "Applicable? Yes" in analysis_result
        
        # Update the inspector results
        inspector = cdt_result["inspector_results"]
        if is_applicable:
            if "codes" not in inspector:
                inspector["codes"] = []
            
            # Only add the code if it's not already in the list
            if request.code not in inspector["codes"]:
                inspector["codes"].append(request.code)
                
                # Update the explanation
                if "explanation" not in inspector:
                    inspector["explanation"] = ""
                inspector["explanation"] += f"\n\nCustom Code {request.code}: {analysis_result}"
        else:
            if "rejected_codes" not in inspector:
                inspector["rejected_codes"] = []
            
            # Only add the code if it's not already in the list
            if request.code not in inspector["rejected_codes"]:
                inspector["rejected_codes"].append(request.code)
                
                # Update the explanation
                if "explanation" not in inspector:
                    inspector["explanation"] = ""
                inspector["explanation"] += f"\n\nRejected Custom Code {request.code}: {analysis_result}"
        
        # Update the database
        db.update_analysis_results(
            request.record_id,
            json.dumps(cdt_result),
            analysis.get("icd_result", "{}")
        )
        
        print(f"✅ Custom code analysis completed and saved to database")
        
        # Get the updated record
        updated_analysis = db.get_complete_analysis(request.record_id)
        if not updated_analysis:
            return {
                "status": "error",
                "message": "Failed to retrieve updated analysis"
            }
        
        # Return the updated inspector results
        inspector_results = {}
        if "inspector_results" in updated_analysis and updated_analysis["inspector_results"]:
            inspector_results = json.loads(updated_analysis["inspector_results"])
        else:
            # Fallback to the inspector results from the cdt_result
            cdt_data = json.loads(updated_analysis.get("cdt_result", "{}"))
            icd_data = json.loads(updated_analysis.get("icd_result", "{}"))
            
            cdt_inspector = cdt_data.get("inspector_results", {})
            icd_inspector = icd_data.get("inspector_results", {})
            
            inspector_results = {
                "cdt": {
                    "codes": cdt_inspector.get("codes", []),
                    "rejected_codes": cdt_inspector.get("rejected_codes", []),
                    "explanation": cdt_inspector.get("explanation", "")
                },
                "icd": {
                    "codes": icd_inspector.get("codes", []),
                    "explanation": icd_inspector.get("explanation", "")
                },
                "timestamp": str(datetime.datetime.now())
            }
        
        return {
            "status": "success",
            "message": "Custom code analysis completed",
            "analysis": analysis_result,
            "is_applicable": is_applicable,
            "inspector_results": inspector_results
        }
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"❌ ERROR: {str(e)}")
        print(f"STACK TRACE: {error_details}")
        return {
            "status": "error",
            "message": str(e),
            "details": error_details
        }

# Endpoint for storing code status
@app.post("/api/store-code-status")
async def store_code_status(request: CodeStatusRequest):
    """Store the final status of selected and rejected codes."""
    try:
        print(f"\n*************************** STORING CODE STATUS FOR RECORD {request.record_id} ***************************")
        print(f"Selected CDT codes: {request.cdt_codes}")
        print(f"Selected ICD codes: {request.icd_codes}")
        print(f"Rejected CDT codes: {request.rejected_cdt_codes}")
        print(f"Rejected ICD codes: {request.rejected_icd_codes}")
        
        # Get the existing analysis from the database
        analysis = db.get_complete_analysis(request.record_id)
        if not analysis:
            return {
                "status": "error",
                "message": f"No analysis found with ID: {request.record_id}"
            }
        
        # Get the inspector results
        inspector_results = {}
        if "inspector_results" in analysis and analysis["inspector_results"]:
            inspector_results = json.loads(analysis["inspector_results"])
        else:
            # Create new inspector_results structure
            inspector_results = {
                "cdt": {
                    "codes": [],
                    "rejected_codes": [],
                    "explanation": "User-selected codes"
                },
                "icd": {
                    "codes": [],
                    "rejected_codes": [],
                    "explanation": "User-selected codes"
                },
                "timestamp": str(datetime.datetime.now())
            }
        
        # Update the inspector results with user selections
        if "cdt" in inspector_results:
            inspector_results["cdt"]["codes"] = request.cdt_codes
            inspector_results["cdt"]["rejected_codes"] = request.rejected_cdt_codes
        
        if "icd" in inspector_results:
            inspector_results["icd"]["codes"] = request.icd_codes
            inspector_results["icd"]["rejected_codes"] = request.rejected_icd_codes
        
        # Add a timestamp to indicate it was updated
        inspector_results["updated_timestamp"] = str(datetime.datetime.now())
        inspector_results["updated_by"] = "user"
        
        # Update the database
        db.update_inspector_results(request.record_id, json.dumps(inspector_results))
        
        # Also update the CDT and ICD results for backward compatibility
        cdt_result = json.loads(analysis.get("cdt_result", "{}"))
        icd_result = json.loads(analysis.get("icd_result", "{}"))
        
        # Update the inspector_results in the CDT data
        cdt_inspector = {
            "codes": request.cdt_codes,
            "rejected_codes": request.rejected_cdt_codes,
            "explanation": "User-selected codes"
        }
        cdt_result["inspector_results"] = cdt_inspector
        
        # Update the inspector_results in the ICD data
        icd_inspector = {
            "codes": request.icd_codes,
            "rejected_codes": request.rejected_icd_codes,
            "explanation": "User-selected codes"
        }
        icd_result["inspector_results"] = icd_inspector
        
        # Update the database with the modified data
        db.update_analysis_results(
            request.record_id,
            json.dumps(cdt_result),
            json.dumps(icd_result)
        )
        
        print(f"✅ Code status updated in the database")
        
        return {
            "status": "success",
            "message": "Code status updated successfully",
            "inspector_results": inspector_results
        }
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"❌ ERROR: {str(e)}")
        print(f"STACK TRACE: {error_details}")
        return {
            "status": "error",
            "message": str(e),
            "details": error_details
        }

# API endpoint to process multiple scenarios in batch
@app.post("/api/analyze-batch")
async def analyze_batch(request: BatchScenarioRequest):
    """Process multiple dental scenarios in parallel."""
    try:
        print(f"\n*************************** PROCESSING BATCH OF {len(request.scenarios)} SCENARIOS ***************************")
        
        # Limit the maximum number of concurrent operations
        max_concurrent = min(3, len(request.scenarios))
        
        # Create a semaphore to limit concurrency
        semaphore = asyncio.Semaphore(max_concurrent)
        
        # Define a function to process a single scenario with rate limiting
        async def process_scenario(scenario, index):
            try:
                # Acquire semaphore to limit concurrent processing
                async with semaphore:
                    print(f"Processing scenario {index+1}/{len(request.scenarios)}")
                    
                    # Create a single scenario request
                    single_request = ScenarioRequest(scenario=scenario)
                    
                    # Set a timeout to prevent hanging
                    timeout = 180  # 180 seconds (3 minutes) timeout per scenario
                    try:
                        # Process using the existing analyze_web function with a timeout
                        result = await asyncio.wait_for(
                            analyze_web(single_request), 
                            timeout=timeout
                        )
                        return result
                    except asyncio.TimeoutError:
                        print(f"Timeout processing scenario {index+1} after {timeout} seconds")
                        return {
                            "status": "error",
                            "message": f"Processing timed out after {timeout} seconds. The scenario may be too complex or the system is under heavy load."
                        }
            except Exception as e:
                # Handle rate limit errors specifically
                if "rate limit" in str(e).lower() or "quota" in str(e).lower() or "429" in str(e):
                    print(f"Rate limit exceeded for scenario {index+1}")
                    return {
                        "status": "error",
                        "message": "API rate limit exceeded. Please try again in a few moments or process fewer scenarios at once."
                    }
                print(f"Error processing scenario {index+1}: {str(e)}")
                return {
                    "status": "error",
                    "message": str(e)
                }
        
        # Create tasks for processing each scenario with controlled concurrency
        tasks = []
        for i, scenario in enumerate(request.scenarios):
            task = asyncio.create_task(process_scenario(scenario, i))
            tasks.append(task)
        
        # Wait for all tasks to complete
        results = await asyncio.gather(*tasks)
        
        # Return all results
        return {
            "status": "success",
            "batch_results": results
        }
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"❌ BATCH PROCESSING ERROR: {str(e)}")
        print(f"STACK TRACE: {error_details}")
        return {
            "status": "error",
            "message": str(e),
            "details": error_details
        }

# Run the application
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
        
    print("\n*************************** STARTING SERVER ***************************")
    print(f"🚀 SERVER RUNNING at {host}:{port}")
    uvicorn.run("app:app", host=host, port=port, reload=True)