from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import time
import json
import logging
import sys
import traceback
from pydantic import BaseModel
from typing import List, Optional
import re
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
inspector_logger = logging.getLogger("inspector_data_flow")

# Add this function to help debug data sources
def log_inspector_data_source(data_type, data, source_description, is_initial_analysis=True):
    """Log detailed information about data being sent to the inspector."""
    inspector_logger.info(f"{'='*80}")
    inspector_logger.info(f"INSPECTOR DATA FLOW - {'INITIAL ANALYSIS' if is_initial_analysis else 'QUESTION ANSWERS'}")
    inspector_logger.info(f"{'='*80}")
    inspector_logger.info(f"Data Type: {data_type}")
    inspector_logger.info(f"Source: {source_description}")
    
    # Log data structure and size
    if isinstance(data, dict):
        inspector_logger.info(f"Structure: Dictionary with {len(data)} keys")
        inspector_logger.info(f"Keys: {list(data.keys())}")
        
        # Sample a few values for inspection
        if data and len(data) > 0:
            sample_key = next(iter(data))
            inspector_logger.info(f"Sample data for key '{sample_key}':")
            sample_value = data[sample_key]
            if isinstance(sample_value, dict):
                inspector_logger.info(f"  - Type: {type(sample_value).__name__}")
                inspector_logger.info(f"  - Keys: {list(sample_value.keys())}")
            else:
                inspector_logger.info(f"  - Value: {str(sample_value)[:100]}...")
    elif data is None:
        inspector_logger.info("Structure: None")
    else:
        inspector_logger.info(f"Structure: {type(data).__name__}")
        inspector_logger.info(f"Value: {str(data)[:100]}...")
    
    inspector_logger.info(f"{'='*80}")

# Import modules
from data_cleaner import process_scenario
from cdt_classifier import classify_cdt_categories
from icd_classifier import classify_icd_categories
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

from database1 import MedicalCodingDB

db = MedicalCodingDB()
# Initialize FastAPI app
app = FastAPI(title="Dental Code Extractor API")

# Track active analyses by ID
active_analyses = {}

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
    expose_headers=["*"],
    max_age=86400,  # 24 hours
)




# Utility function to transform topics to a simplified structure for DB storage
def transform_topics_for_db(topics_data):
    """
    Transform the complex topics structure into a simplified format for database storage.
    
    Args:
        topics_data (dict): Original topics data structure
        
    Returns:
        dict: Simplified topics structure with clean format
    """
    transformed_topics = {}
    
    for range_code, topic_data in topics_data.items():
        topic_name = topic_data.get("name", "Unknown")
        activation_result = topic_data.get("result", {})
        
        # Extract key information from the activation result
        explanation = activation_result.get("explanation", "")
        doubt = activation_result.get("doubt", "")
        activated_subtopics = activation_result.get("activated_subtopics", [])
        
        # Extract code range - handle case where it contains explanation text
        code_range = activation_result.get("code_range", "")
        if "\nCODE RANGE:" in code_range:
            # It's a complex block, extract just the code range part
            import re
            code_match = re.search(r'\nCODE RANGE:\s*(.*?)(?:\n|$)', code_range)
            if code_match:
                code_range = code_match.group(1).strip()
            else:
                # Fallback to the full text if no match
                code_range = code_range
        
        # Create a simplified structure for the topic
        transformed_topics[range_code] = {
            "name": topic_name,
            "result": {
                "EXPLANATION": explanation,
                "DOUBT": doubt,
                "CODE": code_range
            },
            "activated_subtopics": activated_subtopics
        }
    
    return transformed_topics

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

class CodeStatusRequest(BaseModel):
    accepted: List[str]
    denied: List[str]
    record_id: str

class CodeDataRequest(BaseModel):
    scenario: str
    cdt_codes: Optional[str] = None
    code: Optional[str] = None
    record_id: Optional[str] = None

# API routes begin here
@app.post("/api/analyze")
async def analyze_web(request: ScenarioRequest):
    """Process the dental scenario and return results."""
    try:
        # Step 1: Create a record ID
        print("=== STARTING DENTAL SCENARIO ANALYSIS ===")
        print(f"Input scenario: {request.scenario}")
        
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
        
        # Get the database-generated record ID
        record_id = initial_record[0]["id"]
        print(f"Initial record created in database with ID: {record_id}")
        
        # Update with processed data
        db.update_processed_scenario(record_id, processed_scenario)
        print("Database updated with cleaned data")
        
        # Step 4: Analyze CDT Codes
        cdt_result = classify_cdt_categories(processed_scenario)
        
        # Print the CDT classifier result for debugging
        print("\n=== CDT CLASSIFIER RESULT ===")
        print(f"Keys in cdt_result: {cdt_result.keys()}")
        
        # Format CDT classifier results as structured JSON for the database
        cdt_classifier_json = {
            "formatted_results": [],
            "range_codes_string": cdt_result.get('range_codes_string', '')
        }
        
        # Process the formatted_results directly if available
        if 'formatted_results' in cdt_result:
            cdt_classifier_json["formatted_results"] = cdt_result['formatted_results']
            print(f"Using formatted_results directly from classifier with {len(cdt_result['formatted_results'])} results")
        # Fallback for old format processing (keeping this for backward compatibility)
        elif 'code_ranges' in cdt_result and 'explanations' in cdt_result and 'doubts' in cdt_result:
            # Make sure the lengths match
            min_length = min(len(cdt_result['code_ranges']), len(cdt_result['explanations']), len(cdt_result['doubts']))
            
            print(f"Processing {min_length} CDT code ranges with explanations and doubts")
            
            # Process each code range with its explanation and doubt
            for i in range(min_length):
                code_range_data = cdt_result['code_ranges'][i]
                code_range = code_range_data.get('code_range', '').strip()
                
                # Extract just the code part if it contains a name
                if " - " in code_range:
                    code_range = code_range.split(" - ")[0].strip()
                    
                # Remove any brackets
                code_range = code_range.replace("[", "").replace("]", "").replace("\"", "").strip()
                
                # Create formatted result
                formatted_result = {
                    "code_range": code_range,
                    "explanation": cdt_result['explanations'][i].strip() if i < len(cdt_result['explanations']) else "",
                    "doubt": cdt_result['doubts'][i].strip() if i < len(cdt_result['doubts']) else ""
                }
                cdt_classifier_json["formatted_results"].append(formatted_result)
                
                print(f"Processed code range: {code_range} with explanation and doubt")
        elif 'range_codes' in cdt_result:
            # Just include the code ranges without explanations/doubts
            range_codes = cdt_result.get('range_codes', [])
            print(f"No explanations/doubts found. Using {len(range_codes)} range codes")
            
            for code in range_codes:
                cdt_classifier_json["formatted_results"].append({
                    "code_range": code,
                    "explanation": "",
                    "doubt": ""
                })
        else:
            print("WARNING: Could not find formatted_results or code_ranges in CDT classifier result")
            print(f"Available fields: {list(cdt_result.keys())}")
            
            # Try to extract directly from the result text if available
            result_text = cdt_result.get('text', '')
            if result_text:
                # Use regex to extract code ranges, explanations, and doubts
                sections = re.split(r'CODE_RANGE:', result_text)
                
                for section in sections[1:]:  # Skip first empty section
                    lines = section.strip().split('\n')
                    if not lines:
                        continue
                        
                    # First line is the code range
                    code_range = lines[0].strip()
                    if " - " in code_range:
                        code_range = code_range.split(" - ")[0].strip()
                    code_range = code_range.replace("[", "").replace("]", "").replace("\"", "").strip()
                    
                    # Extract explanation and doubt
                    explanation = ""
                    doubt = ""
                    current_section = None
                    
                    for line in lines[1:]:
                        line = line.strip()
                        if not line:
                            continue
                            
                        if line == "EXPLANATION:":
                            current_section = "explanation"
                        elif line == "DOUBT:":
                            current_section = "doubt"
                        elif current_section == "explanation":
                            if explanation:
                                explanation += " " + line
                            else:
                                explanation = line
                        elif current_section == "doubt":
                            if doubt:
                                doubt += " " + line
                            else:
                                doubt = line
                    
                    cdt_classifier_json["formatted_results"].append({
                        "code_range": code_range,
                        "explanation": explanation,
                        "doubt": doubt
                    })

        print(f"Formatted CDT classifier JSON with {len(cdt_classifier_json['formatted_results'])} results")
        print(json.dumps(cdt_classifier_json, indent=2))
        
        # Step 5: Activate CDT Topics
        # Get the range codes string from the classifier result directly
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
                                "explanation": "",
                                "doubt": "",
                                "subtopic": topic_name,
                                "activated_subtopics": [],
                                "codes": [f"No specific codes identified for {topic_name}"]
                            }
                        # If activation_result doesn't have explanation or doubt fields, ensure they're present 
                        if isinstance(activation_result, dict) and 'code_range' in activation_result:
                            if 'explanation' not in activation_result:
                                activation_result['explanation'] = ""
                            if 'doubt' not in activation_result:
                                activation_result['doubt'] = ""
                    except Exception as topic_error:
                        print(f"  Error in {topic_name}: {str(topic_error)}")
                        activation_result = {
                            "code_range": clean_range,
                            "explanation": "",
                            "doubt": f"Error processing: {str(topic_error)}",
                            "subtopic": topic_name,
                            "activated_subtopics": [],
                            "codes": [f"Error processing {topic_name}"]
                        }
                    
                    # Ensure the result has a consistent structure
                    if isinstance(activation_result, dict) and 'code_range' in activation_result:
                        # Parse the code range to extract explanations and doubts
                        if 'code_range' in activation_result and isinstance(activation_result['code_range'], str):
                            code_range_text = activation_result['code_range']
                            
                            # Try to extract explanation and doubt from code_range if they're embedded
                            import re
                            explanation_match = re.search(r'EXPLANATION:(.*?)(?=\n\nDOUBT:|$)', code_range_text, re.DOTALL)
                            doubt_match = re.search(r'DOUBT:(.*?)(?=\n\nCODE RANGE:|$)', code_range_text, re.DOTALL)
                            
                            if explanation_match:
                                activation_result['explanation'] = explanation_match.group(1).strip()
                            
                            if doubt_match:
                                activation_result['doubt'] = doubt_match.group(1).strip()
                    
                    # End of inner try-except
                    # Store the results with a consistent structure
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
                        "result": {
                            "code_range": clean_range,
                            "explanation": "",
                            "doubt": f"Error: {str(e)}",
                            "subtopic": topic_name,
                            "activated_subtopics": [],
                            "codes": [f"Error processing {topic_name}"]
                        }
                    }
            else:
                print(f"Warning: No topic function found for range code {clean_range} (mapped to {category_range})")
        
        # Step 6: Generate questions if needed (before inspector)
        print("\n=== STEP 6: QUESTIONER - GENERATING QUESTIONS IF NEEDED ===")
        questioner_result = process_questioner(processed_scenario, 
                                              cdt_analysis=topics_results, 
                                              icd_analysis=classify_icd_categories(processed_scenario))
        
        # Transform topics into simplified structure for DB storage
        simplified_topics = transform_topics_for_db(topics_results)
        
        # Process subtopics data from topics_results more thoroughly
        subtopics_data = {}
        for range_code, topic_data in topics_results.items():
            topic_name = topic_data.get("name", "Unknown")
            activation_result = topic_data.get("result", {})
            
            # Extract subtopic info if available
            if isinstance(activation_result, dict):
                explanation = activation_result.get('explanation', '')
                doubt = activation_result.get('doubt', '')
                subtopics = activation_result.get('activated_subtopics', [])
                codes = activation_result.get('codes', [])
                
                # Process each code to extract code, explanation, and doubt
                formatted_codes = []
                for code_text in codes:
                    # First try to extract structured code information
                    code_match = re.search(r'CODE:\s*([^\n]+)', code_text)
                    explanation_match = re.search(r'EXPLANATION:\s*([^\n]+(?:\n[^\n]+)*?)(?=\nDOUBT:|\nCODE:|\Z)', code_text)
                    doubt_match = re.search(r'DOUBT:\s*([^\n]+(?:\n[^\n]+)*?)(?=\nCODE:|\nEXPLANATION:|\Z)', code_text)
                    
                    code = code_match.group(1).strip() if code_match else ""
                    code_explanation = explanation_match.group(1).strip() if explanation_match else ""
                    code_doubt = doubt_match.group(1).strip() if doubt_match else ""
                    
                    # If no structured info found, try to extract standalone codes
                    if not code:
                        standalone_codes = re.findall(r'\b([A-Za-z]\d{4,5}|\d{5,6})\b', code_text)
                        if standalone_codes:
                            for standalone_code in standalone_codes:
                                formatted_code = {
                                    "code": standalone_code,
                                    "explanation": code_explanation or explanation,
                                    "doubt": code_doubt or doubt
                                }
                                formatted_codes.append(formatted_code)
                            continue
                    
                    # Add formatted code with any extracted information
                    formatted_code = {
                        "code": code,
                        "explanation": code_explanation or explanation,
                        "doubt": code_doubt or doubt
                    }
                    
                    # If no code was found but we have text content, use it as explanation
                    if not code and code_text.strip():
                        formatted_code["explanation"] = code_text.strip()
                    
                    if code or code_explanation or code_doubt or code_text.strip():
                        formatted_codes.append(formatted_code)
                
                # Add to subtopics data
                subtopics_data[range_code] = {
                    "topic_name": topic_name,
                    "activated_subtopics": subtopics,
                    "specific_codes": formatted_codes,
                    "explanation": explanation,
                    "doubt": doubt
                }

        has_questions = questioner_result.get('has_questions')
        
        # If there are questions, we need to handle them
        if has_questions:
            print(f"Questions identified: {questioner_result.get('cdt_questions', {}).get('questions', [])} | {questioner_result.get('icd_questions', {}).get('questions', [])}")
            
            # For web interface, we would normally show a form with questions
            # Since we're building API functionality, we'll store the questions
            # and return them in the response
            
            # Store questioner data in the database
            questioner_json = json.dumps(questioner_result, default=str)
            db.update_questioner_data(record_id, questioner_json)
            print(f"Questioner data saved to database for ID: {record_id}")
            
            # Skip inspector stage until questions are answered
            inspector_cdt_results = {"pending_questions": True, "codes": []}
            inspector_icd_results = {"pending_questions": True, "codes": []}
            
            # Save preliminary results to database without inspector results
            # Format and combine CDT results
            combined_cdt_results = {
                "cdt_classifier": cdt_classifier_json,
                "topics": simplified_topics,
                "inspector_results": inspector_cdt_results,
                "subtopics_data": subtopics_data,  # Add subtopics data
                "pending_questions": True  # Flag to indicate questions are pending
            }
            
            # No subtopics processing when questions are pending
            
            # Format ICD results 
            icd_result = classify_icd_categories(processed_scenario)
            icd_result["inspector_results"] = inspector_icd_results
            icd_result["pending_questions"] = True
            
            # Convert to JSON string for database
            combined_cdt_json = json.dumps(combined_cdt_results, default=str)
            combined_icd_json = json.dumps(icd_result, default=str)
            
            # Save results to database
            db.update_analysis_results(record_id, combined_cdt_json, combined_icd_json)
            
            # Calculate processing time
            processing_time = time.time() - start_time
            print(f"\nTotal processing time (with pending questions): {round(processing_time, 2)} seconds")
            print("=== ANALYSIS PARTIALLY COMPLETE - WAITING FOR QUESTION ANSWERS ===")
            
            # Return JSON response with the questions
            return {
                "status": "success",
                "data": {
                    "record_id": record_id,
                    "has_questions": True,
                    "subtopics_data": subtopics_data,  # Include subtopics data in response
                    "inspector_results": {"pending_questions": True, "codes": []},
                    "cdt_questions": questioner_result.get('cdt_questions', {}).get('questions', []),
                    "icd_questions": questioner_result.get('icd_questions', {}).get('questions', []),
                    "processing_time": round(processing_time, 2)
                }
            }
        else:
            print("No questions needed, proceeding to inspection stage")
            # Store empty questioner data
            db.update_questioner_data(record_id, json.dumps({"has_questions": False}))

            # Step 7: Final validation with inspectors (after questioner)
            print("\n=== STEP 7: INSPECTOR - VALIDATING CODES ===")

            # Log data sources before calling inspector
            log_inspector_data_source("processed_scenario", processed_scenario, 
                                     "IN-MEMORY (from data_cleaner.process_scenario)")
            log_inspector_data_source("topics_results", topics_results, 
                                     "IN-MEMORY (from topic activation functions)")
            log_inspector_data_source("questioner_data", questioner_result if has_questions else None, 
                                     "IN-MEMORY (from process_questioner)")

            # Check if subtopics_data is structurally different from topics_results
            subtopics_keys = set(subtopics_data.keys())
            topics_keys = set(topics_results.keys())
            if subtopics_keys != topics_keys:
                inspector_logger.warning(f"MISMATCH: subtopics_data keys ({subtopics_keys}) differ from topics_results keys ({topics_keys})")

            # Also check for specific codes
            all_subtopic_codes = []
            for topic_data in subtopics_data.values():
                for code_data in topic_data.get("specific_codes", []):
                    if isinstance(code_data, dict) and code_data.get("code") and code_data.get("code").lower() != "none":
                        all_subtopic_codes.append(code_data.get("code"))

            inspector_logger.info(f"Available codes in subtopics_data: {all_subtopic_codes}")

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
                "topics": simplified_topics,
                "inspector_results": inspector_cdt_results,
                "subtopics_data": subtopics_data,  # Use the already processed subtopics_data
            }

            # Format ICD results to include inspector results
            icd_result = classify_icd_categories(processed_scenario)
            icd_result["inspector_results"] = inspector_icd_results
            
            # Convert to JSON string for database
            combined_cdt_json = json.dumps(combined_cdt_results, default=str)
            combined_icd_json = json.dumps(icd_result, default=str)
            
            # Save results to database
            db.update_analysis_results(record_id, combined_cdt_json, combined_icd_json)
            
            # Calculate processing time
            processing_time = time.time() - start_time
            print(f"\nTotal processing time: {round(processing_time, 2)} seconds")
            print("=== ANALYSIS COMPLETE ===")
            
            # Return JSON response with the database record ID
            return {
                "status": "success",
                "data": {
                    "record_id": record_id,  # Use the database-generated ID
                    "subtopics_data": combined_cdt_results["subtopics_data"],
                    "inspector_results": inspector_cdt_results,
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

@app.get("/")
def test(request: Request):
    return {"message": "Hello, World!"}

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
        
        # Get record from Supabase
        result = db.supabase.table("dental_report").select("*").eq("id", record_id).execute()
        
        if not result.data:
            return None
        
        # Get the first record (should be only one since id is primary key)
        row = result.data[0]
        
        # Create a dict with the record data
        record = {
            "id": row["id"],
            "user_question": row["user_question"],
            "processed_scenario": row["processed_clean_data"],
            "cdt_json": row["cdt_result"],
            "icd_json": row["icd_result"],
            "questioner_json": row["questioner_data"],
            "created_at": row["created_at"]
        }
        
        return record
    except Exception as e:
        logger.error(f"Error retrieving record from database: {e}")
        return None

# Modified view_record to return JSON data instead of using templates
@app.get("/view-record/{record_id}")
async def view_record(record_id: str):
    """View the details of a stored analysis record as JSON."""
    try:
        # Get record from the database
        record = get_record_from_database(record_id)
        
        if not record:
            raise HTTPException(status_code=404, detail=f"No record found with ID: {record_id}")
        
        # Parse JSON data for the response
        response_data = {
            "record_id": record_id,
            "processed_scenario": record.get("processed_scenario", "Not available"),
        }
        
        # Format CDT data
        try:
            if "cdt_json" in record and record["cdt_json"]:
                response_data["cdt_data"] = json.loads(record["cdt_json"])
            else:
                response_data["cdt_data"] = {}
        except Exception as e:
            logger.error(f"Error parsing CDT JSON data: {e}")
            response_data["cdt_data"] = {"error": f"Error parsing data: {str(e)}"}
        
        # Format ICD data
        try:
            if "icd_json" in record and record["icd_json"]:
                response_data["icd_data"] = json.loads(record["icd_json"])
            else:
                response_data["icd_data"] = {}
        except Exception as e:
            logger.error(f"Error parsing ICD JSON data: {e}")
            response_data["icd_data"] = {"error": f"Error parsing data: {str(e)}"}
        
        # Format questioner data
        try:
            if "questioner_json" in record and record["questioner_json"]:
                response_data["questioner_data"] = json.loads(record["questioner_json"])
            else:
                response_data["questioner_data"] = {}
        except Exception as e:
            logger.error(f"Error parsing questioner JSON data: {e}")
            response_data["questioner_data"] = {"error": f"Error parsing data: {str(e)}"}
        
        return response_data
    
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error viewing record: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving record: {str(e)}")

@app.post("/api/store-code-status")
async def store_code_status(request: CodeStatusRequest):
    """Store the status of accepted and denied codes for a record."""
    try:
        print(f"=== STORING CODE STATUS FOR ID: {request.record_id} ===")
        db = MedicalCodingDB()
        
        # Get existing record
        record = get_record_from_database(request.record_id, close_connection=False)
        if not record:
            raise HTTPException(status_code=404, detail="Record not found")
        
        # Parse existing CDT data
        cdt_json = json.loads(record["cdt_json"]) if record["cdt_json"] else {}
        
        # Create code status structure
        code_status = {
            "accepted": request.accepted,
            "denied": request.denied,
            "timestamp": time.time()
        }
        
        # Update CDT data with code status
        cdt_json["code_status"] = code_status
        
        # Update database
        db.supabase.table("dental_report").update({"cdt_result": json.dumps(cdt_json)}).eq("id", request.record_id).execute()
        
        return {
            "status": "success",
            "message": "Code statuses updated successfully",
            "data": {
                "record_id": request.record_id,
                "code_status": code_status
            }
        }
    
    except Exception as e:
        logger.error(f"Error storing code status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/answer-questions/{record_id}")
async def api_answer_questions(record_id: str, request: Request):
    """Process the answers to questions and continue with analysis from API."""
    try:
        print(f"=== PROCESSING ANSWERS FOR ID: {record_id} ===")
        
        # Get the request data
        request_data = await request.json()
        answers_json = request_data.get("answers", "{}")
        
        print(f"Request data: {request_data}")
        print(f"Answers JSON: {answers_json}")
        
        try:
            # Parse the answers JSON
            answers = json.loads(answers_json)
            print(f"Parsed answers: {answers}")
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {str(e)}")
            answers = request_data.get("answers", {})
            print(f"Using raw answers: {answers}")
        
        # Create a new database connection
        db = MedicalCodingDB()
        
        # Get the record from the database - don't close the connection
        record = get_record_from_database(record_id, close_connection=False)
        
        if not record:
            print(f"❌ Record not found: {record_id}")
            # List recent records for debugging
            try:
                recent_records = db.supabase.table("dental_report").select("id, created_at").order("created_at", desc=True).limit(5).execute().data
                print(f"Recent records: {recent_records}")
            except Exception as e:
                print(f"Error fetching recent records: {str(e)}")
            
            return {
                "status": "error",
                "message": f"No record found with ID: {record_id}",
                "data": None
            }
        
        print(f"✅ Record found: {record_id}")
        
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
            db.supabase.table("dental_report").update({"processed_clean_data": updated_scenario}).eq("id", record_id).execute()
            print(f"Updated processed scenario for {record_id}")
        except Exception as e:
            print(f"❌ Error updating processed scenario: {str(e)}")
            # Try to reconnect and retry
            db.connect()
            db.supabase.table("dental_report").update({"processed_clean_data": updated_scenario}).eq("id", record_id).execute()
            print(f"Second attempt: Updated processed scenario for {record_id}")
        
        # Update the questioner data with the answers
        questioner_data["answers"] = answers
        questioner_data["has_answers"] = True
        questioner_data["updated_scenario"] = updated_scenario
        
        # Save the updated questioner data
        try:
            db.supabase.table("dental_report").update({"questioner_data": json.dumps(questioner_data)}).eq("id", record_id).execute()
            print(f"Updated questioner data for {record_id}")
        except Exception as e:
            print(f"❌ Error updating questioner data: {str(e)}")
            # Try to reconnect and retry
            db.connect()
            db.supabase.table("dental_report").update({"questioner_data": json.dumps(questioner_data)}).eq("id", record_id).execute()
            print(f"Second attempt: Updated questioner data for {record_id}")
        
        # Parse CDT and ICD results from the database
        cdt_json = record.get("cdt_json", "{}")
        icd_json = record.get("icd_json", "{}")
        
        cdt_result = json.loads(cdt_json) if cdt_json else {}
        icd_result = json.loads(icd_json) if icd_json else {}
        
        # Get topics_results from CDT result
        topics_results = cdt_result.get("topics", {})
        
        # Preserve existing subtopics_data if it exists
        existing_subtopics_data = cdt_result.get("subtopics_data", {})
        
        # Run the inspectors with the updated scenario and questioner data
        inspector_logger.info(f"{'='*80}")
        inspector_logger.info(f"INSPECTOR DATA FLOW - QUESTION ANSWERS")
        inspector_logger.info(f"{'='*80}")

        # Log data sources before calling inspector for question answers
        log_inspector_data_source("updated_scenario", updated_scenario, 
                                 "COMBINED (DB scenario + new answers)", is_initial_analysis=False)
        log_inspector_data_source("topics_results", topics_results, 
                                 "FROM DATABASE (from cdt_result.get('topics'))", is_initial_analysis=False)
        log_inspector_data_source("questioner_data", questioner_data, 
                                 "COMBINED (DB questions + new answers)", is_initial_analysis=False)

        # Check for available codes in topics_results from database
        all_topic_codes = []
        for topic_name, topic_data in topics_results.items():
            if isinstance(topic_data, dict) and "result" in topic_data:
                result = topic_data.get("result", {})
                if isinstance(result, dict):
                    # Check direct code field
                    if "code" in result and result["code"] and result["code"].lower() != "none":
                        all_topic_codes.append(result["code"])
                    
                    # Check codes array
                    for code_text in result.get("codes", []):
                        import re
                        code_matches = re.findall(r'([A-Z]\d{4,5})', code_text)
                        all_topic_codes.extend(code_matches)
                        
                    # Check specific_codes array
                    for code_data in result.get("specific_codes", []):
                        if isinstance(code_data, dict) and code_data.get("code") and code_data.get("code").lower() != "none":
                            all_topic_codes.append(code_data.get("code"))

        inspector_logger.info(f"Available codes in topics_results: {all_topic_codes}")

        inspector_cdt_results = analyze_dental_scenario(updated_scenario, 
                                                       topics_results, 
                                                       questioner_data=questioner_data)
        
        inspector_icd_results = analyze_icd_scenario(updated_scenario, 
                                                   icd_result.get("icd_topics_results", {}), 
                                                    questioner_data=questioner_data)

        # Update CDT results
        cdt_result["inspector_results"] = inspector_cdt_results
        
        # Transform topics into simplified structure for DB storage if topics exist
        if "topics" in cdt_result:
            # Transform topics into simplified structure for DB storage
            simplified_topics = transform_topics_for_db(cdt_result.get("topics", {}))
            cdt_result["topics"] = simplified_topics

        # Update ICD result with inspector results
        icd_result["inspector_results"] = inspector_icd_results
        
        # Remove the pending_questions flag if it exists
        if "pending_questions" in cdt_result:
            del cdt_result["pending_questions"]
        if "pending_questions" in icd_result:
            del icd_result["pending_questions"]
        
        # Regenerate subtopics_data if it doesn't exist or is empty
        if not existing_subtopics_data:
            print("Generating new subtopics_data from topics_results")
            subtopics_data = {}
            
            # Loop through topics results to extract subtopic data with a cleaner format
            for range_code, topic_data in topics_results.items():
                topic_name = topic_data.get("name", "Unknown")
                activation_result = topic_data.get("result", {})
                
                # Extract subtopic info if available
                if isinstance(activation_result, dict):
                    explanation = activation_result.get('explanation', '')
                    doubt = activation_result.get('doubt', '')
                    subtopics = activation_result.get('activated_subtopics', [])
                    codes = activation_result.get('codes', [])
                    
                    # Process each code to extract code, explanation, and doubt
                    formatted_codes = []
                    for code_text in codes:
                        # First try to extract structured code information
                        code_match = re.search(r'CODE:\s*([^\n]+)', code_text)
                        explanation_match = re.search(r'EXPLANATION:\s*([^\n]+(?:\n[^\n]+)*?)(?=\nDOUBT:|\nCODE:|\Z)', code_text)
                        doubt_match = re.search(r'DOUBT:\s*([^\n]+(?:\n[^\n]+)*?)(?=\nCODE:|\nEXPLANATION:|\Z)', code_text)
                        
                        code = code_match.group(1).strip() if code_match else ""
                        code_explanation = explanation_match.group(1).strip() if explanation_match else ""
                        code_doubt = doubt_match.group(1).strip() if doubt_match else ""
                        
                        # If no structured info found, try to extract standalone codes
                        if not code:
                            standalone_codes = re.findall(r'\b([A-Za-z]\d{4,5}|\d{5,6})\b', code_text)
                            if standalone_codes:
                                for standalone_code in standalone_codes:
                                    formatted_code = {
                                        "code": standalone_code,
                                        "explanation": code_explanation or explanation,
                                        "doubt": code_doubt or doubt
                                    }
                                    formatted_codes.append(formatted_code)
                                continue
                        
                        # Add formatted code with any extracted information
                        formatted_code = {
                            "code": code,
                            "explanation": code_explanation or explanation,
                            "doubt": code_doubt or doubt
                        }
                        
                        # If no code was found but we have text content, use it as explanation
                        if not code and code_text.strip():
                            formatted_code["explanation"] = code_text.strip()
                        
                        if code or code_explanation or code_doubt or code_text.strip():
                            formatted_codes.append(formatted_code)
                    
                    # Add to subtopics data
                    subtopics_data[range_code] = {
                        "topic_name": topic_name,
                        "activated_subtopics": subtopics,
                        "specific_codes": formatted_codes,
                        "explanation": explanation,
                        "doubt": doubt
                    }
                
            # Update the CDT result with the new subtopics_data
            cdt_result["subtopics_data"] = subtopics_data
        else:
            print("Using existing subtopics_data")
            # Keep the existing subtopics_data
            cdt_result["subtopics_data"] = existing_subtopics_data
        
        # Save to database
        try:
            db.supabase.table("dental_report").update({"cdt_result": json.dumps(cdt_result), "icd_result": json.dumps(icd_result)}).eq("id", record_id).execute()
            print(f"Updated analysis results for {record_id}")
        except Exception as e:
            print(f"❌ Error updating analysis results: {str(e)}")
            # Try to reconnect and retry
            db.connect()
            db.supabase.table("dental_report").update({"cdt_result": json.dumps(cdt_result), "icd_result": json.dumps(icd_result)}).eq("id", record_id).execute()
            print(f"Second attempt: Updated analysis results for {record_id}")
        
        # Format data for response
        subtopics_data = cdt_result.get("subtopics_data", {})
        
        # Return the results as JSON
        return {
            "status": "success",
            "data": {
                "record_id": record_id,
                "subtopics_data": subtopics_data,
                "inspector_results": inspector_cdt_results,
                "cdt_questions": [],  # No more questions
                "icd_questions": [],  # No more questions
            }
        }
        
    except Exception as e:
        traceback.print_exc()
        return {
            "status": "error",
            "message": str(e)
        }

def display_database_record(record_id):
    """CLI function to display database record content"""
    print(f"Attempting to retrieve record: {record_id}")
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
                print(json.dumps(cdt_json, indent=2))
            except json.JSONDecodeError:
                print("  [Error parsing CDT JSON data]")
        
        # Display ICD data
        if "icd_json" in record and record["icd_json"]:
            print(f"\nICD DATA:")
            print(f"{'-'*80}")
            try:
                icd_json = json.loads(record["icd_json"])
                print(json.dumps(icd_json, indent=2))
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

@app.post("/api/add-code-data")
async def add_code_data(request: CodeDataRequest):
    """Add code data to the database."""
    try:
        # If cdt_codes is not provided but code is, use code instead
        cdt_codes = request.cdt_codes
        if not cdt_codes and request.code:
            cdt_codes = request.code
            
        if not cdt_codes:
            raise HTTPException(status_code=422, detail="Either cdt_codes or code must be provided")
            
        # Use the ADd_code_data function from add_codes/add_code_data.py
        from add_codes.add_code_data import Add_code_data
        result = Add_code_data(request.scenario, cdt_codes)
        
        # If record_id is provided, use it to link the analysis
        record_id = request.record_id
        if not record_id:
            # Create a new record if none exists
            record_id = db.add_code_analysis(request.scenario, cdt_codes, result)
            
        return {
            "status": "success",
            "data": {
                "scenario": request.scenario,
                "cdt_codes": cdt_codes,
                "record_id": record_id,
                "analysis": result
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Add new endpoint for adding custom codes
class CustomCodeRequest(BaseModel):
    code: str
    scenario: str
    record_id: str

@app.post("/api/add-custom-code")
async def add_custom_code(request: CustomCodeRequest):
    """Process a custom code added by the user for a scenario."""
    try:
        logger.info(f"Processing custom code: {request.code} for record: {request.record_id}")
        
        # Get the record
        record = get_record_from_database(request.record_id)
        if not record:
            return {
                "status": "error",
                "message": f"No record found with ID: {request.record_id}"
            }
        
        # Use the Add_code_data function for analysis
        from add_codes.add_code_data import Add_code_data
        analysis_result = Add_code_data(request.scenario, request.code)
        
        # Create the code data structure
        code_data = {
            "code": request.code,
            "explanation": analysis_result if analysis_result else f"Custom code {request.code} added by user.",
            "doubt": "User-added code"
        }
        
        # Return the results
        return {
            "status": "success",
            "data": {
                "code_data": code_data,
                "record_id": request.record_id,
                "analysis": analysis_result
            }
        }
    except Exception as e:
        logger.error(f"Error adding custom code: {str(e)}")
        traceback.print_exc()
        return {
            "status": "error",
            "message": str(e)
        }

# CLI command handling
if __name__ == "__main__":
    import uvicorn
    
    # Check if we're being asked to view a record
    if len(sys.argv) > 1 and sys.argv[1] == "view-record" and len(sys.argv) == 3:
        record_id = sys.argv[2]
        display_database_record(record_id)
    else:
        # Get port and host from environment variables with fallbacks
        port = int(os.getenv("PORT", 8000))
        host = os.getenv("HOST", "0.0.0.0")
        
        print(f"Starting server on {host}:{port}")
        uvicorn.run("app:app", host=host, port=port, reload=True, timeout_keep_alive=600, timeout_graceful_shutdown=120)