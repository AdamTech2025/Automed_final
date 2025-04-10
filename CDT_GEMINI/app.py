from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import time
import json
import uuid
import logging
import asyncio
import sys
import traceback
from pydantic import BaseModel

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import modules
from data_cleaner import process_scenario
from cdt_classifier import classify_cdt_categories
from icd_classifier import classify_icd_categories
from supabase import MedicalCodingDB
from inspector import analyze_dental_scenario
from icd_inspector import analyze_icd_scenario
from questioner import process_questioner

# Import CDT Topic Functions
from topics.diagnostics import activate_diagnostic
from topics.preventive import activate_preventive
from topics.restorative import activate_restorative
from topics.endodontics import activate_endodontic
from topics.periodontics import activate_periodontic
from topics.prosthodonticsremovable import activate_prosthodonticsremovable
from topics.maxillofacialprosthetics import activate_maxillofacial_prosthetics
from topics.implantservices import activate_implant_services
from topics.prosthodonticsfixed import activate_prosthodonticsfixed
from topics.oralandmaxillofacialsurgery import activate_oral_maxillofacial_surgery
from topics.orthodontics import activate_orthodontic
from topics.adjunctivegeneralservices import activate_adjunctive_general_services

# Initialize FastAPI app
app = FastAPI(title="Dental Code Extractor API")
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Track active analyses by ID
active_analyses = {}

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper function to map specific CDT codes to their broader category
def map_to_cdt_category(specific_code):
    """
    Maps a specific CDT code or range to its broader category.
    For example, "D0120-D0180" would map to "D0100-D0999".
    """
    # Extract the base code without the range
    if "-" in specific_code:
        base_code = specific_code.split("-")[0]
    else:
        base_code = specific_code
    
    # Get the first 4 characters (e.g., "D012" becomes "D01")
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

# CDT Topic and Subtopic Mappings
CDT_TOPICS = {
    "D0100-D0999": {
        "name": "Diagnostic",
        "function": activate_diagnostic,
    },
    "D1000-D1999": {
        "name": "Preventive",
        "function": activate_preventive,
    },
    "D2000-D2999": {
        "name": "Restorative",
        "function": activate_restorative,
    },
    "D3000-D3999": {
        "name": "Endodontics",
        "function": activate_endodontic,
    },
    "D4000-D4999": {
        "name": "Periodontics",
        "function": activate_periodontic,
    },
    "D5000-D5899": {
        "name": "Prosthodontics Removable",
        "function": activate_prosthodonticsremovable,
    },
    "D5900-D5999": {
        "name": "Maxillofacial Prosthetics",
        "function": activate_maxillofacial_prosthetics,
    },
    "D6000-D6199": {
        "name": "Implant Services",
        "function": activate_implant_services,
    },
    "D6200-D6999": {
        "name": "Prosthodontics Fixed",
        "function": activate_prosthodonticsfixed,
    },
    "D7000-D7999": {
        "name": "Oral and Maxillofacial Surgery",
        "function": activate_oral_maxillofacial_surgery,
    },
    "D8000-D8999": {
        "name": "Orthodontics",
        "function": activate_orthodontic,
    },
    "D9000-D9999": {
        "name": "Adjunctive General Services",
        "function": activate_adjunctive_general_services,
    },
}

class ScenarioRequest(BaseModel):
    scenario: str

# Add simple implementation for routes
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Render the home page."""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "results": None,
        "has_questions": False,
        "cdt_questions": None,
        "icd_questions": None
    })

@app.post("/api/analyze")
async def analyze_web(request: ScenarioRequest):
    """Process the dental scenario and return results."""
    try:
        # Step 1: Create a record ID
        record_id = str(uuid.uuid4())
        print("=== STARTING DENTAL SCENARIO ANALYSIS ===")
        print(f"Input scenario: {request.scenario}")
        print(f"Generated record ID: {record_id}")
        
        # Step 2: Clean the data using data_cleaner
        print("\n=== CLEANING DATA ===")
        start_time = time.time()
        processed_result = process_scenario(request.scenario)
        processed_scenario = processed_result["standardized_scenario"]
        
        # Step 3: Store in database
        print("\n=== STORING IN DATABASE ===")
        db = MedicalCodingDB()
        
        # First record with just user input
        initial_record = db.create_analysis_record({
            "user_question": request.scenario,
            "processed_clean_data": "",
            "cdt_result": "{}",
            "icd_result": "{}",
            "questioner_data": "{}"
        })
        print("Initial record created in database")
        
        # Update with processed data
        db.update_processed_scenario(initial_record[0]["id"], processed_scenario)
        print("Database updated with cleaned data")
        
        # Step 4: Analyze CDT Codes
        cdt_result = classify_cdt_categories(processed_scenario)
        
        # Format CDT classifier results as structured JSON for the database
        # Use the new format for database storage
        cdt_classifier_json = {
            "formatted_results": cdt_result.get("formatted_results", []),
            "range_codes_string": cdt_result.get('range_codes_string', '')
        }
        
        # Step 5: Activate CDT Topics
        range_codes = cdt_result["range_codes_string"].split(",")
        topics_results = {}
        
        # Keep track of already processed categories to avoid duplicates
        processed_categories = set()
        
        # Process each identified code range
        for range_code in range_codes:
            clean_range = range_code.strip()
            
            # Map the specific range to its broader category
            category_range = map_to_cdt_category(clean_range)
            
            # Skip if we've already processed this category
            if category_range in processed_categories:
                print(f"Skipping already processed category: {category_range} for specific code {clean_range}")
                continue
                
            if category_range and category_range in CDT_TOPICS:
                # Add to processed categories
                processed_categories.add(category_range)
                
                topic_info = CDT_TOPICS[category_range]
                topic_name = topic_info["name"]
                
                # Continue with topic activation as in the original code
                try:
                    # Pass the processed scenario directly to the topic function
                    # Make sure we handle errors and empty responses
                    try:
                        activation_result = topic_info["function"](processed_scenario)
                        if not activation_result:
                            print(f"  Warning: Empty result from {topic_name}")
                            activation_result = {
                                "code_range": clean_range,
                                "subtopic": topic_name,
                                "codes": [f"No specific codes identified for {topic_name}"]
                            }
                    except Exception as topic_error:
                        print(f"  Error in {topic_name}: {str(topic_error)}")
                        activation_result = {
                            "code_range": clean_range,
                            "subtopic": topic_name,
                            "error": str(topic_error),
                            "codes": [f"Error processing {topic_name}"]
                        }
                    
                    # End of inner try-except
                    # Store the results
                    topics_results[clean_range] = {
                        "name": topic_name,
                        "result": activation_result
                    }
                
                    # Print the activation result
                    print(f"  Result: {json.dumps(activation_result, indent=2)}")
                
                    # Display specific codes if available
                    if isinstance(activation_result, dict) and 'codes' in activation_result:
                        print("  Specific Codes:")
                        for code in activation_result['codes']:
                            print(f"  - {code}")
                            
                    # Display activated subtopics if available
                    if isinstance(activation_result, dict) and 'activated_subtopics' in activation_result:
                        print("  Activated Subtopics:")
                        for subtopic in activation_result['activated_subtopics']:
                            print(f"  - {subtopic}")
                except Exception as e:
                    print(f"Error activating {topic_name}: {str(e)}")
                    topics_results[clean_range] = {
                        "name": topic_name,
                        "result": {"error": str(e)}
                    }
            else:
                print(f"Warning: No topic function found for range code {clean_range} (mapped to {category_range})")
        
        # Step 6: Generate questions if needed (before inspector)
        print("\n=== STEP 6: QUESTIONER - GENERATING QUESTIONS IF NEEDED ===")
        questioner_result = process_questioner(processed_scenario, 
                                              cdt_analysis=topics_results, 
                                              icd_analysis=classify_icd_categories(processed_scenario))
        
        has_questions = questioner_result.get('has_questions', False)
        
        # If there are questions, we need to handle them
        if has_questions:
            print(f"Questions identified: {questioner_result.get('cdt_questions', {}).get('questions', [])} | {questioner_result.get('icd_questions', {}).get('questions', [])}")
            
            # For web interface, we would normally show a form with questions
            # Since we're building API functionality, we'll store the questions
            # and return them in the response
            
            # Store questioner data in the database
            questioner_json = json.dumps(questioner_result, default=str)
            db.update_questioner_data(initial_record[0]["id"], questioner_json)
            print(f"Questioner data saved to database for ID: {initial_record[0]['id']}")
            
            # For now, we'll continue without answers (in production, you'd wait for user input)
            print("Questions need to be answered before proceeding to inspection stage")
        else:
            print("No questions needed, proceeding to inspection stage")
            # Store empty questioner data
            db.update_questioner_data(initial_record[0]["id"], json.dumps({"has_questions": False}))
        
        # Step 7: Final validation with inspectors (after questioner)
        print("\n=== STEP 7: INSPECTOR - VALIDATING CODES ===")
        inspector_cdt_results = analyze_dental_scenario(processed_scenario, 
                                                       topics_results, 
                                                       questioner_data=questioner_result if has_questions else None)
        
        inspector_icd_results = analyze_icd_scenario(processed_scenario, 
                                                    classify_icd_categories(processed_scenario).get("icd_topics_results", {}), 
                                                    questioner_data=questioner_result if has_questions else None)
        
        # Save results to database
        # Format and combine CDT results
        combined_cdt_results = {
            "cdt_classifier": cdt_classifier_json,
            "topics": topics_results,
            "inspector_results": inspector_cdt_results,
            "subtopics_data": {},  # Initialize empty subtopics container
        }

        # Loop through topics results to extract subtopic data
        for range_code, topic_data in topics_results.items():
            topic_name = topic_data.get("name", "Unknown")
            activation_result = topic_data.get("result", {})
            
            # Extract subtopic info if available
            if isinstance(activation_result, dict) and 'activated_subtopics' in activation_result:
                subtopics = activation_result.get('activated_subtopics', [])
                codes = activation_result.get('codes', [])
                
                # Process each code to extract code, explanation, and doubt
                formatted_codes = []
                for code_text in codes:
                    # Extract code, explanation, and doubt using regex
                    import re
                    code_match = re.search(r'CODE: (.*?)(?=\n|$)', code_text)
                    explanation_match = re.search(r'EXPLANATION: (.*?)(?=\n|$)', code_text)
                    doubt_match = re.search(r'DOUBT: (.*?)(?=\n|$)', code_text)
                    
                    formatted_code = {
                        "code": code_match.group(1).strip() if code_match else "",
                        "explanation": explanation_match.group(1).strip() if explanation_match else "",
                        "doubt": doubt_match.group(1).strip() if doubt_match else ""
                    }
                    formatted_codes.append(formatted_code)
                
                # Add to subtopics data
                combined_cdt_results["subtopics_data"][range_code] = {
                    "topic_name": topic_name,
                    "activated_subtopics": subtopics,
                    "specific_codes": formatted_codes
                }

        # Format ICD results to include inspector results
        icd_result = classify_icd_categories(processed_scenario)
        icd_result["inspector_results"] = inspector_icd_results
        
        # Convert to JSON string for database
        combined_cdt_json = json.dumps(combined_cdt_results, default=str)
        combined_icd_json = json.dumps(icd_result, default=str)
        
        # Save results to database
        db.update_analysis_results(initial_record[0]["id"], combined_cdt_json, combined_icd_json)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        print(f"\nTotal processing time: {round(processing_time, 2)} seconds")
        print("=== ANALYSIS COMPLETE ===")
        
        # Return JSON response
        return {
            "status": "success",
            "data": {
                "record_id": record_id,
                # "cdt_result": cdt_classifier_json,
                # "topics_results": topics_results,
                "subtopics_data": combined_cdt_results["subtopics_data"],
                "inspector_results": inspector_cdt_results,
                # "icd_data": icd_result,
                # "questioner_result": questioner_result,
                # "has_questions": has_questions,
                "cdt_questions": questioner_result.get('cdt_questions', {}).get('questions', []),
                "icd_questions": questioner_result.get('icd_questions', {}).get('questions', []),
                "processing_time": round(processing_time, 2)
            }
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

# Endpoint to check analysis status (for AJAX polling)
@app.get("/status/{analysis_id}", response_class=JSONResponse)
async def get_analysis_status(analysis_id: str):
    """Get the status of an ongoing analysis."""
    if analysis_id in active_analyses:
        return active_analyses[analysis_id]
    return {"status": "not_found"}

def analyze_dental_scenario_cli(scenario):
    """Process a dental scenario, clean data, and store in database with terminal output."""
    try:
        # STEP 1: CLEAN AND SAVE DATA
        print("🔍 === STEP 1: CLEAN AND SAVE DATA === 🔍")
        print(f"Input: {scenario}")
        
        # Basic validation
        if not scenario or not scenario.strip():
            print("Error: Empty scenario provided")
            return
        
        # Create record ID for tracking
        record_id = str(uuid.uuid4())
        print(f"Generated record ID: {record_id}")
        
        # Initialize database connection
        db = MedicalCodingDB()
        
        # Save initial record
        db.create_analysis_record(
            record_id=record_id,
            user_question=scenario,
            processed_clean_data="",
            cdt_result="{}",
            icd_result="{}"
        )
        print("Initial record created in database")
        
        # Process scenario using data_cleaner
        print("\n🧼 === CLEANING DATA === 🧼")
        start_time = time.time()
        processed_result = process_scenario(scenario)
        processed_scenario = processed_result["standardized_scenario"]
        print(f"Cleaned data: {processed_scenario}")
        
        # Update database with processed scenario
        db.update_processed_scenario(record_id, processed_scenario)
        print("Database updated with cleaned data ✅")
        
        # STEP 2: IDENTIFY CDT CODE RANGES
        print("\n🦷 === STEP 2: IDENTIFY CDT CODE RANGES === 🦷")
        cdt_result = classify_cdt_categories(processed_scenario)
        print(f"🦷 CDT Range Codes: {cdt_result.get('range_codes_string', '')} 🦷")
        
        # Print each code range with explanation using the new format
        print("\n🦷 CDT classifier results (NEW FORMAT): 🦷")
        for item in cdt_result.get("formatted_results", []):
            print(f"{{")
            print(f"code_range: {item['code_range']},")
            print(f"explanation: {item['explanation']},")
            print(f"doubt: {item['doubt']}")
            print(f"}},")
        
        # Format CDT classifier results as structured JSON for the database
        # Use the new format for database storage
        cdt_classifier_json = {
            "formatted_results": cdt_result.get("formatted_results", []),
            "range_codes_string": cdt_result.get('range_codes_string', '')
        }
        
        # Display the JSON structure
        print("\n🦷 CDT classifier results JSON: 🦷")
        print(json.dumps(cdt_classifier_json, indent=2, default=str))
        
        # STEP 3: ACTIVATE CDT TOPICS BASED ON CODE RANGES
        print("\n🦷 === STEP 3: ACTIVATE CDT TOPICS === 🦷")
        # Get the relevant code ranges identified in step 2
        range_codes = cdt_result["range_codes_string"].split(",")
        topics_results = {}
        
        # Keep track of already processed categories to avoid duplicates
        processed_categories = set()
        
        # Process each identified code range
        for range_code in range_codes:
            clean_range = range_code.strip()
            
            # Map the specific range to its broader category
            category_range = map_to_cdt_category(clean_range)
            
            # Skip if we've already processed this category
            if category_range in processed_categories:
                print(f"🦷 Skipping already processed category: {category_range} for specific code {clean_range} 🦷")
                continue
                
            if category_range and category_range in CDT_TOPICS:
                # Add to processed categories
                processed_categories.add(category_range)
                
                topic_info = CDT_TOPICS[category_range]
                topic_name = topic_info["name"]
                
                print(f"🦷 Activating topic: {topic_name} ({category_range}) for specific code {clean_range} 🦷")
                
                try:
                    # Pass the processed scenario directly to the topic function
                    # Make sure we handle errors and empty responses
                    try:
                        activation_result = topic_info["function"](processed_scenario)
                        if not activation_result:
                            print(f"  Warning: Empty result from {topic_name}")
                            activation_result = {
                                "code_range": clean_range,
                                "subtopic": topic_name,
                                "codes": [f"No specific codes identified for {topic_name}"]
                            }
                    except Exception as topic_error:
                        print(f"  Error in {topic_name}: {str(topic_error)}")
                        activation_result = {
                            "code_range": clean_range,
                            "subtopic": topic_name,
                            "error": str(topic_error),
                            "codes": [f"Error processing {topic_name}"]
                        }
                    
                    # End of inner try-except
                    # Store the results
                    topics_results[clean_range] = {
                        "name": topic_name,
                        "result": activation_result
                    }
                
                    # Print the activation result
                    print(f"  🦷 Result: {json.dumps(activation_result, indent=2)} 🦷")
                
                    # Display specific codes if available
                    if isinstance(activation_result, dict) and 'codes' in activation_result:
                        print("  🦷 Specific Codes: 🦷")
                        for code in activation_result['codes']:
                            print(f"  - {code}")
                            
                    # Display activated subtopics if available
                    if isinstance(activation_result, dict) and 'activated_subtopics' in activation_result:
                        print("  🦷 Activated Subtopics: 🦷")
                        for subtopic in activation_result['activated_subtopics']:
                            print(f"  - {subtopic}")
                except Exception as e:
                    print(f"Error activating {topic_name}: {str(e)}")
                    topics_results[clean_range] = {
                        "name": topic_name,
                        "result": {"error": str(e)}
                    }
            else:
                print(f"Warning: No topic function found for range code {clean_range} (mapped to {category_range})")
        
        # Display the topics results JSON
        print("\n🦷 Topic activation results JSON: 🦷")
        print(json.dumps(topics_results, indent=2, default=str))
        
        # Combine CDT classifier and topics results into a single JSON structure
        combined_cdt_results = {
            "cdt_classifier": cdt_classifier_json,
            "topics": topics_results,
            "inspector_results": {},  # Placeholder for inspector results
            "subtopics_data": {},  # Initialize empty subtopics container
        }
        
        # Loop through topics results to extract subtopic data
        for range_code, topic_data in topics_results.items():
            topic_name = topic_data.get("name", "Unknown")
            activation_result = topic_data.get("result", {})
            
            # Extract subtopic info if available
            if isinstance(activation_result, dict) and 'activated_subtopics' in activation_result:
                subtopics = activation_result.get('activated_subtopics', [])
                codes = activation_result.get('codes', [])
                
                # Process each code to extract code, explanation, and doubt
                formatted_codes = []
                for code_text in codes:
                    # Extract code, explanation, and doubt using regex
                    import re
                    code_match = re.search(r'CODE: (.*?)(?=\n|$)', code_text)
                    explanation_match = re.search(r'EXPLANATION: (.*?)(?=\n|$)', code_text)
                    doubt_match = re.search(r'DOUBT: (.*?)(?=\n|$)', code_text)
                    
                    formatted_code = {
                        "code": code_match.group(1).strip() if code_match else "",
                        "explanation": explanation_match.group(1).strip() if explanation_match else "",
                        "doubt": doubt_match.group(1).strip() if doubt_match else ""
                    }
                    formatted_codes.append(formatted_code)
                
                # Add to subtopics data
                combined_cdt_results["subtopics_data"][range_code] = {
                    "topic_name": topic_name,
                    "activated_subtopics": subtopics,
                    "specific_codes": formatted_codes
                }
        
        # STEP 4: QUESTIONER - CHECK IF ANY QUESTIONS ARE NEEDED
        print("\n❓ === STEP 4: QUESTIONER - CHECKING FOR NEEDED QUESTIONS === ❓")
        questioner_result = process_questioner(processed_scenario, 
                                              cdt_analysis=combined_cdt_results, 
                                              icd_analysis=classify_icd_categories(processed_scenario))
        
        has_questions = questioner_result.get('has_questions', False)
        
        if has_questions:
            print("Questions needed before final coding:")
            
            # Display CDT questions if any
            cdt_questions = questioner_result.get('cdt_questions', {}).get('questions', [])
            if cdt_questions:
                print("\n🦷 CDT Questions: 🦷")
                for i, question in enumerate(cdt_questions, 1):
                    print(f"{i}. {question}")
                print(f"Explanation: {questioner_result.get('cdt_questions', {}).get('explanation', '')}")
            
            # Display ICD questions if any
            icd_questions = questioner_result.get('icd_questions', {}).get('questions', [])
            if icd_questions:
                print("\n🏥 ICD Questions: 🏥")
                for i, question in enumerate(icd_questions, 1):
                    print(f"{i}. {question}")
                print(f"Explanation: {questioner_result.get('icd_questions', {}).get('explanation', '')}")
            
            # In CLI mode, prompt for answers
            print("\nPlease answer these questions to continue with analysis:")
            answers = {}
            
            # Get answers for CDT questions
            for question in cdt_questions:
                answer = input(f"CDT Q: {question}\nA: ")
                answers[question] = answer
            
            # Get answers for ICD questions
            for question in icd_questions:
                answer = input(f"ICD Q: {question}\nA: ")
                answers[question] = answer
            
            # Update the scenario with the answers
            updated_scenario = processed_scenario + "\n\nAdditional information provided:\n"
            for question, answer in answers.items():
                updated_scenario += f"Q: {question}\nA: {answer}\n"
            
            # Update the database with the updated scenario
            db.update_processed_scenario(record_id, updated_scenario)
            
            # Update questioner data with answers
            questioner_result["answers"] = answers
            questioner_result["has_answers"] = True
            questioner_result["updated_scenario"] = updated_scenario
            
            # Save questioner data to the database
            db.update_questioner_data(record_id, json.dumps(questioner_result))
            
            # Use the updated scenario for inspection
            processed_scenario = updated_scenario
            print(f"\nScenario updated with answers: {updated_scenario}")
        else:
            print("No questions needed, proceeding to inspection stage")
            # Store empty questioner data
            db.update_questioner_data(record_id, json.dumps({"has_questions": False}))
        
        # STEP 5: IDENTIFY ICD CATEGORIES & CODES
        print("\n🏥 === STEP 5: IDENTIFY ICD CATEGORIES & CODES === 🏥")
        icd_result = classify_icd_categories(processed_scenario)
        print(f"🏥 ICD Categories: {icd_result.get('category_numbers_string', '')} 🏥")
        
        # Print each category with explanation
        for i, category in enumerate(icd_result["categories"]):
            print(f"\n🏥 Category {i+1}: {category} 🏥")
            print(f"Codes:")
            for code in icd_result["code_lists"][i]:
                print(f"  - {code}")
            print(f"Explanation: {icd_result['explanations'][i]}")
            if icd_result['doubts'][i]:
                print(f"Doubt: {icd_result['doubts'][i]}")
        
        # Get the ICD topic results
        icd_topics_results = icd_result.get("icd_topics_results", {})
        
        # Display the ICD topics results
        print("\n🏥 ICD Topics Results: 🏥")
        for category_num, topic_data in icd_topics_results.items():
            category_name = topic_data.get("name", "Unknown")
            print(f"🏥 Category {category_num}: {category_name} 🏥")
            print(f"Result: {topic_data.get('result', 'No result')}")
            
            # Print the parsed result if available
            parsed_result = topic_data.get("parsed_result", {})
            if parsed_result:
                print(f"  Code: {parsed_result.get('code', 'No code')}")
                print(f"  Explanation: {parsed_result.get('explanation', 'No explanation')}")
                print(f"  Doubt: {parsed_result.get('doubt', 'No doubt')}")
        
        # STEP 6: INVOKE INSPECTOR TO VALIDATE CDT CODES (with questioner data if available)
        print("\n🔍 === STEP 6: VALIDATE CDT CODES WITH INSPECTOR === 🔍")
        inspector_cdt_results = analyze_dental_scenario(processed_scenario, 
                                                      topics_results, 
                                                      questioner_data=questioner_result if has_questions else None)
        
        # Format and display results
        print("\n🦷 Inspector CDT validation results: 🦷")
        print(f"🦷 Validated CDT codes: {inspector_cdt_results.get('codes', [])} 🦷")
        print(f"🦷 Explanation: {inspector_cdt_results.get('explanation', 'No explanation provided')} 🦷")
        
        # STEP 7: INVOKE ICD INSPECTOR TO VALIDATE ICD CODES (with questioner data if available)
        print("\n🔍 === STEP 7: VALIDATE ICD CODES WITH INSPECTOR === 🔍")
        inspector_icd_results = analyze_icd_scenario(processed_scenario, 
                                                   icd_topics_results, 
                                                   questioner_data=questioner_result if has_questions else None)
        
        # Format and display results
        print("\n🏥 Inspector ICD validation results: 🏥")
        print(f"🏥 Validated ICD codes: {inspector_icd_results.get('codes', [])} 🏥")
        print(f"🏥 Explanation: {inspector_icd_results.get('explanation', 'No explanation provided')} 🏥")
        
        # STEP 8: SAVE RESULTS TO DATABASE
        print("\n💾 === STEP 8: SAVE FINAL RESULTS TO DATABASE === 💾")
        # Save CDT results with comprehensive structure
        combined_cdt_results = {
            "cdt_classifier": cdt_classifier_json,
            "topics": topics_results,
            "inspector_results": inspector_cdt_results,
            "subtopics_data": {},  # Initialize empty subtopics container
        }

        # Loop through topics results to extract subtopic data
        for range_code, topic_data in topics_results.items():
            topic_name = topic_data.get("name", "Unknown")
            activation_result = topic_data.get("result", {})
            
            # Extract subtopic info if available
            if isinstance(activation_result, dict) and 'activated_subtopics' in activation_result:
                subtopics = activation_result.get('activated_subtopics', [])
                codes = activation_result.get('codes', [])
                
                # Process each code to extract code, explanation, and doubt
                formatted_codes = []
                for code_text in codes:
                    # Extract code, explanation, and doubt using regex
                    import re
                    code_match = re.search(r'CODE: (.*?)(?=\n|$)', code_text)
                    explanation_match = re.search(r'EXPLANATION: (.*?)(?=\n|$)', code_text)
                    doubt_match = re.search(r'DOUBT: (.*?)(?=\n|$)', code_text)
                    
                    formatted_code = {
                        "code": code_match.group(1).strip() if code_match else "",
                        "explanation": explanation_match.group(1).strip() if explanation_match else "",
                        "doubt": doubt_match.group(1).strip() if doubt_match else ""
                    }
                    formatted_codes.append(formatted_code)
                
                # Add to subtopics data
                combined_cdt_results["subtopics_data"][range_code] = {
                    "topic_name": topic_name,
                    "activated_subtopics": subtopics,
                    "specific_codes": formatted_codes
                }

        # Format ICD results to include inspector results
        combined_icd_data = icd_result  # Use the already obtained icd_result
        combined_icd_data["inspector_results"] = inspector_icd_results

        # Convert to JSON string
        combined_cdt_json = json.dumps(combined_cdt_results, default=str)
        combined_icd_json = json.dumps(combined_icd_data, default=str)

        # Explain what's being stored
        print("\n📋 === CDT DATA STRUCTURE BEING SAVED === 📋")
        print("The cdt_result field in the database will contain a JSON object with the following structure:")
        print("- cdt_classifier: Contains the output from classify_cdt_categories function")
        print("  |- formatted_results: Array of code ranges with explanations and doubts")
        print("  |- range_codes_string: Comma-separated string of code ranges")
        print("- topics: Contains the results from topic activation functions")
        print("  |- [code_range]: Information about each activated CDT topic")
        print("     |- name: Topic name (e.g., 'Diagnostic', 'Preventive')")
        print("     |- result: Detailed result from topic activation function")
        print("- subtopics_data: Information about activated subtopics")
        print("  |- [code_range]: Information about subtopics for each code range")
        print("     |- topic_name: Name of the parent topic")
        print("     |- activated_subtopics: List of activated subtopics")
        print("     |- specific_codes: List of specific codes with explanations")
        print("- inspector_results: Output from analyze_dental_scenario function")
        print("  |- codes: Final validated CDT codes")
        print("  |- explanation: Explanation for the code selection")

        print("\n📋 === ICD DATA STRUCTURE BEING SAVED === 📋")
        print("The icd_result field in the database will contain a JSON object with the following structure:")
        print("- categories: List of ICD categories identified")
        print("- code_lists: List of ICD codes for each category")
        print("- explanations: Explanations for each ICD category")
        print("- doubts: Any doubts or uncertainties for each category")
        print("- category_numbers_string: Comma-separated string of category numbers")
        print("- icd_topics_results: Results from ICD topic activation")
        print("- inspector_results: Output from analyze_icd_scenario function")
        print("  |- codes: Final validated ICD codes")
        print("  |- explanation: Explanation for the code selection")

        # Save CDT results
        db.update_analysis_results(record_id, combined_cdt_json, combined_icd_json)
        print(f"Combined CDT and ICD results saved to database for ID: {record_id} ✅")
        print(f"Data in 'cdt_result' field includes classifier, topics, subtopics, and inspector results.")
        
        # Calculate processing time
        processing_time = time.time() - start_time
        print(f"\n⏱️ Total processing time: {round(processing_time, 2)} seconds ⏱️")
        print("=== ANALYSIS COMPLETE ===")
        
    except Exception as e:
        print(f"Error in analysis: {str(e)}")

def get_record_from_database(record_id, close_connection=True):
    """
    Retrieve a record from the database by ID
    Returns a dictionary with all record data or None if not found
    
    Parameters:
    record_id -- The ID of the record to retrieve
    close_connection -- Whether to close the connection after retrieving the record (default: True)
    """
    try:
        db = MedicalCodingDB()
        
        # Get basic record info using the correct column names
        query = """
        SELECT 
            id, 
            user_question,
            processed_clean_data, 
            cdt_result,
            icd_result,
            questioner_data,
            created_at
        FROM dental_report 
        WHERE id = ?
        """
        db.cursor.execute(query, (record_id,))
        row = db.cursor.fetchone()
        
        if not row:
            return None
        
        # Create a dict with the record data
        record = {
            "id": row[0],
            "user_question": row[1],
            "processed_scenario": row[2],  # processed_clean_data in DB
            "cdt_json": row[3],           # cdt_result in DB
            "icd_json": row[4],           # icd_result in DB
            "questioner_json": row[5],    # questioner_data in DB
            "created_at": row[6]
        }
        
        return record
    except Exception as e:
        logger.error(f"Error retrieving record from database: {e}")
        return None
    finally:
        if close_connection:
            db.close_connection()

@app.get("/view-record/{record_id}", response_class=HTMLResponse)
async def view_record(request: Request, record_id: str):
    """View the details of a stored analysis record."""
    try:
        # Get record from the database
        record = get_record_from_database(record_id)
        
        if not record:
            return templates.TemplateResponse(
                "record_view.html",
                {
                    "request": request,
                    "record_id": record_id,
                    "error": "Record not found",
                    "error_details": f"No record with ID {record_id} exists in the database."
                }
            )
        
        # Parse JSON data
        template_data = {
            "request": request,
            "record_id": record_id,
            "processed_scenario": record.get("processed_scenario", "Not available"),
            "error": None
        }
        
        # Format CDT data
        try:
            if "cdt_json" in record and record["cdt_json"]:
                cdt_json = json.loads(record["cdt_json"])
                template_data["formatted_cdt_json"] = json.dumps(cdt_json, indent=2)
                
                # Extract CDT classifier data
                if "cdt_classifier" in cdt_json:
                    template_data["cdt_classifier"] = cdt_json["cdt_classifier"]
                
                # Extract subtopics data
                if "subtopics_data" in cdt_json:
                    template_data["subtopics_data"] = cdt_json["subtopics_data"]
                
                # Extract inspector results
                if "inspector_results" in cdt_json:
                    template_data["inspector_results"] = cdt_json["inspector_results"]
            else:
                template_data["formatted_cdt_json"] = "{}"
        except Exception as e:
            logger.error(f"Error parsing CDT JSON data: {e}")
            template_data["formatted_cdt_json"] = f"Error parsing data: {str(e)}"
        
        # Format ICD data
        try:
            icd_data = {}
            if "icd_json" in record and record["icd_json"]:
                icd_json = json.loads(record["icd_json"])
                template_data["formatted_icd_json"] = json.dumps(icd_json, indent=2)
                
                # Extract ICD data
                if "categories" in icd_json:
                    icd_data["categories"] = icd_json["categories"]
                
                if "code_lists" in icd_json:
                    icd_data["code_lists"] = icd_json["code_lists"]
                
                if "explanations" in icd_json:
                    icd_data["explanations"] = icd_json["explanations"]
                
                if "doubts" in icd_json:
                    icd_data["doubts"] = icd_json["doubts"]
                
                if "icd_topics_results" in icd_json:
                    icd_data["icd_topics_results"] = icd_json["icd_topics_results"]
                
                if "inspector_results" in icd_json:
                    icd_data["inspector_results"] = icd_json["inspector_results"]
            else:
                template_data["formatted_icd_json"] = "{}"
            
            template_data["icd_data"] = icd_data
        except Exception as e:
            logger.error(f"Error parsing ICD JSON data: {e}")
            template_data["formatted_icd_json"] = f"Error parsing data: {str(e)}"
            template_data["icd_data"] = {}
        
        # Format questioner data
        try:
            if "questioner_json" in record and record["questioner_json"]:
                questioner_json = json.loads(record["questioner_json"])
                template_data["formatted_questioner_json"] = json.dumps(questioner_json, indent=2)
            else:
                template_data["formatted_questioner_json"] = "{}"
        except Exception as e:
            logger.error(f"Error parsing questioner JSON data: {e}")
            template_data["formatted_questioner_json"] = f"Error parsing data: {str(e)}"
        
        # Render the template with data
        return templates.TemplateResponse("record_view.html", template_data)
    
    except Exception as e:
        logger.error(f"Error viewing record: {e}")
        return templates.TemplateResponse(
            "record_view.html",
            {
                "request": request,
                "record_id": record_id,
                "error": "Error retrieving record",
                "error_details": str(e),
                "processing_complete": True  # Mark as complete for error state
            }
        )

def display_database_record(record_id):
    """
    CLI function to display database record content
    """
    print(f"Attempting to retrieve record: {record_id}")  # Debug statement
    
    try:
        record = get_record_from_database(record_id)
        if not record:
            print(f"No record found with ID: {record_id}")
            return
        
        print(f"\n{'='*80}")
        print(f"RECORD ID: {record_id}")
        print(f"{'='*80}")
        
        if "processed_scenario" in record:
            print(f"\nPROCESSED SCENARIO:")
            print(f"{'-'*80}")
            print(record["processed_scenario"])
        
        # Display CDT data
        if "cdt_json" in record and record["cdt_json"]:
            print(f"\nCDT DATA:")
            print(f"{'-'*80}")
            
            try:
                cdt_json = json.loads(record["cdt_json"])
                
                # Display CDT Classifier
                if "cdt_classifier" in cdt_json:
                    print("\nCDT CLASSIFIER RESULTS:")
                    classifier = cdt_json["cdt_classifier"]
                    if "range_codes_string" in classifier:
                        print(f"Range Codes: {classifier['range_codes_string']}")
                    
                    if "formatted_results" in classifier:
                        print("\nFormatted Results:")
                        for result in classifier["formatted_results"]:
                            print(f"  - Code Range: {result.get('code_range', 'N/A')}")
                            print(f"    Explanation: {result.get('explanation', 'N/A')}")
                            if "doubt" in result and result["doubt"]:
                                print(f"    Doubt: {result['doubt']}")
                            print()
                
                # Display activated topics
                if "subtopics_data" in cdt_json:
                    print("\nACTIVATED TOPICS AND SUBTOPICS:")
                    for code_range, data in cdt_json["subtopics_data"].items():
                        print(f"  - {data.get('topic_name', 'Unknown Topic')} ({code_range})")
                        
                        if "activated_subtopics" in data and data["activated_subtopics"]:
                            print("    Activated Subtopics:")
                            for subtopic in data["activated_subtopics"]:
                                print(f"      * {subtopic}")
                        
                        if "specific_codes" in data and data["specific_codes"]:
                            print("    Specific Codes:")
                            print(f"      {', '.join(data['specific_codes'])}")
                        
                        print()
                
                # Display inspector results
                if "inspector_results" in cdt_json:
                    print("\nINSPECTOR RESULTS:")
                    inspector = cdt_json["inspector_results"]
                    if "codes" in inspector and inspector["codes"]:
                        print(f"  Validated CDT Codes: {', '.join(inspector['codes'])}")
                    
                    if "explanation" in inspector:
                        print(f"  Explanation: {inspector['explanation']}")
                    
                    print()
            except json.JSONDecodeError:
                print("  [Error parsing CDT JSON data]")
        
        # Display ICD data
        if "icd_json" in record and record["icd_json"]:
            print(f"\nICD DATA:")
            print(f"{'-'*80}")
            
            try:
                icd_json = json.loads(record["icd_json"])
                
                # Display ICD Categories
                if "categories" in icd_json:
                    print("\nICD CATEGORIES:")
                    for i, category in enumerate(icd_json["categories"]):
                        print(f"  - {category}")
                        
                        # Display codes for this category
                        if "code_lists" in icd_json and i < len(icd_json["code_lists"]):
                            codes = icd_json["code_lists"][i]
                            if codes:
                                print(f"    Codes: {', '.join(codes)}")
                        
                        # Display explanation for this category
                        if "explanations" in icd_json and i < len(icd_json["explanations"]):
                            explanation = icd_json["explanations"][i]
                            print(f"    Explanation: {explanation}")
                        
                        # Display doubt for this category
                        if "doubts" in icd_json and i < len(icd_json["doubts"]) and icd_json["doubts"][i]:
                            doubt = icd_json["doubts"][i]
                            print(f"    Doubt: {doubt}")
                        
                        print()
                
                # Display ICD inspector results
                if "inspector_results" in icd_json:
                    print("\nICD INSPECTOR RESULTS:")
                    inspector = icd_json["inspector_results"]
                    if "codes" in inspector and inspector["codes"]:
                        print(f"  Validated ICD Codes: {', '.join(inspector['codes'])}")
                    
                    if "explanation" in inspector:
                        print(f"  Explanation: {inspector['explanation']}")
                    
                    print()
            except json.JSONDecodeError:
                print("  [Error parsing ICD JSON data]")
        
        # Display Questioner data
        if "questioner_json" in record and record["questioner_json"]:
            print(f"\nQUESTIONER DATA:")
            print(f"{'-'*80}")
            
            try:
                questioner_json = json.loads(record["questioner_json"])
                print(json.dumps(questioner_json, indent=2))
            except json.JSONDecodeError:
                print("  [Error parsing Questioner JSON data]")
        
        print(f"\n{'='*80}\n")
    
    except Exception as e:
        print(f"Error displaying record: {e}")

# Add a new endpoint for answering questions
@app.post("/answer-questions/{record_id}", response_class=HTMLResponse)
async def answer_questions(request: Request, record_id: str):
    """Process the answers to questions and continue with analysis."""
    try:
        print(f"=== PROCESSING ANSWERS FOR ID: {record_id} ===")
        
        # Get the form data
        form_data = await request.form()
        answers_json = form_data.get("answers", "{}")
        
        try:
            # Parse the answers JSON
            answers = json.loads(answers_json)
        except json.JSONDecodeError:
            # Fallback to traditional form processing if JSON parsing fails
            answers = {}
            # Process CDT questions from traditional form fields
            for key in form_data.keys():
                if key.startswith("cdt_") or key.startswith("icd_"):
                    answers[key] = form_data[key]
        
        # Create a new database connection
        db = MedicalCodingDB()
        
        # Get the record from the database - don't close the connection
        record = get_record_from_database(record_id, close_connection=False)
        
        if not record:
            return templates.TemplateResponse("index.html", {
                "request": request,
                "error": "Record not found",
                "error_details": f"No record found with ID: {record_id}"
            })
        
        # Get the processed scenario
        processed_scenario = record.get("processed_scenario", "")
        
        # Get the questioner data
        questioner_json = record.get("questioner_json", "{}")
        questioner_data = json.loads(questioner_json) if questioner_json else {}
        
        # Update the scenario with the answers
        updated_scenario = processed_scenario + "\n\nAdditional information provided:\n"
        for question, answer in answers.items():
            updated_scenario += f"Q: {question}\nA: {answer}\n"
        
        # Update the record with the updated scenario
        try:
            db.update_processed_scenario(record_id, updated_scenario)
            print(f"Updated processed scenario for {record_id}")
        except Exception as e:
            print(f"❌ Error updating processed scenario: {str(e)}")
            # Try to reconnect and retry
            db.connect()
            db.update_processed_scenario(record_id, updated_scenario)
            print(f"Second attempt: Updated processed scenario for {record_id}")
        
        # Update the questioner data with the answers
        questioner_data["answers"] = answers
        questioner_data["has_answers"] = True
        questioner_data["updated_scenario"] = updated_scenario
        
        # Save the updated questioner data
        try:
            db.update_questioner_data(record_id, json.dumps(questioner_data))
            print(f"Updated questioner data for {record_id}")
        except Exception as e:
            print(f"❌ Error updating questioner data: {str(e)}")
            # Try to reconnect and retry
            db.connect()
            db.update_questioner_data(record_id, json.dumps(questioner_data))
            print(f"Second attempt: Updated questioner data for {record_id}")
        
        # Parse CDT and ICD results from the database
        cdt_json = record.get("cdt_json", "{}")
        icd_json = record.get("icd_json", "{}")
        
        cdt_result = json.loads(cdt_json) if cdt_json else {}
        icd_result = json.loads(icd_json) if icd_json else {}
        
        # Get topics_results from CDT result
        topics_results = cdt_result.get("topics", {})
        
        # Run the inspectors with the updated scenario and questioner data
        inspector_cdt_results = analyze_dental_scenario(updated_scenario, 
                                                       topics_results, 
                                                       questioner_data=questioner_data)
        
        inspector_icd_results = analyze_icd_scenario(updated_scenario, 
                                                   icd_result.get("icd_topics_results", {}), 
                                                    questioner_data=questioner_data)

        # Update CDT results
        cdt_result["inspector_results"] = inspector_cdt_results
        
        # Update ICD result with inspector results
        icd_result["inspector_results"] = inspector_icd_results
        
        # Save to database
        try:
            db.update_analysis_results(record_id, json.dumps(cdt_result), json.dumps(icd_result))
            print(f"Updated analysis results for {record_id}")
        except Exception as e:
            print(f"❌ Error updating analysis results: {str(e)}")
            # Try to reconnect and retry
            db.connect()
            db.update_analysis_results(record_id, json.dumps(cdt_result), json.dumps(icd_result))
            print(f"Second attempt: Updated analysis results for {record_id}")
        
        # Format data for template
        cdt_classifier_json = cdt_result.get("cdt_classifier", {})
        subtopics_data = cdt_result.get("subtopics_data", {})
        
        # Close database connection
        db.close_connection()
        
        # Return the results
        return templates.TemplateResponse("index.html", {
            "request": request,
            "scenario": record.get("user_question", ""),
            "processed_scenario": updated_scenario,
            "cdt_result": cdt_classifier_json,
            "topics_results": topics_results,
            "subtopics_data": subtopics_data,
            "inspector_results": inspector_cdt_results,
            "icd_data": icd_result,
            "questioner_result": questioner_data,
            "has_questions": False,  # Questions have been answered
            "results": {
                "record_id": record_id
            },
            "processing_complete": True  # Flag to indicate processing is complete
        })
        
    except Exception as e:
        traceback.print_exc()
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": "An error occurred while processing answers",
            "error_details": str(e),
            "processing_complete": True  # Still mark as complete even with error
        })

# CLI command handling
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "view-record" and len(sys.argv) == 3:
        record_id = sys.argv[2]
        display_database_record(record_id)
    else:
        import uvicorn
        uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)