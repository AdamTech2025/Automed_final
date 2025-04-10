"""
CLI utility to check record format in the database.
Usage: python check_record_format.py [record_id]
"""
import sys
import json
import os
from database import MedicalCodingDB

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

def get_record_from_database(record_id, close_connection=True):
    """
    Retrieve a record from the database by ID.
    Returns a dictionary with all record data or None if not found.
    """
    try:
        db = MedicalCodingDB()
        print(f"Database connection established")
        
        # Get basic record info
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
        print(f"Executing query: {query} with ID: {record_id}")
        db.cursor.execute(query, (record_id,))
        row = db.cursor.fetchone()
        
        if not row:
            print(f"No row returned for ID: {record_id}")
            
            # Debug: List recent records
            try:
                print("Listing recent records:")
                db.cursor.execute("SELECT id, created_at FROM dental_report ORDER BY created_at DESC LIMIT 5")
                recent_records = db.cursor.fetchall()
                for rec in recent_records:
                    print(f"  ID: {rec[0]}, Created: {rec[1]}")
            except Exception as e:
                print(f"Error listing recent records: {e}")
                
            return None
        
        print(f"Record found with ID: {row[0]}")
        
        # Create a dict with the record data
        record = {
            "id": row[0],
            "user_question": row[1],
            "processed_scenario": row[2],
            "cdt_json": row[3],
            "icd_json": row[4],
            "questioner_json": row[5],
            "created_at": row[6]
        }
        
        return record
    except Exception as e:
        print(f"Error retrieving record from database: {e}")
        import traceback
        traceback.print_exc()
        return None
    finally:
        if close_connection and 'db' in locals():
            try:
                db.close_connection()
                print("Database connection closed")
            except Exception as e:
                print(f"Error closing database connection: {e}")

def list_files_in_directory():
    """List files in the current directory."""
    print("\nFiles in current directory:")
    for file in os.listdir('.'):
        print(f"  {file}")

def check_record_format(record_id):
    """
    Check the format of a record in the database and show the transformed topics.
    """
    print(f"Checking record format for ID: {record_id}")
    list_files_in_directory()
    
    record = get_record_from_database(record_id)
    if not record:
        print(f"No record found with ID: {record_id}")
        return
    
    print(f"\n{'='*80}")
    print(f"RECORD ID: {record_id}")
    print(f"{'='*80}")
    
    # Parse CDT data
    if "cdt_json" in record and record["cdt_json"]:
        try:
            print(f"CDT JSON size: {len(record['cdt_json'])} bytes")
            cdt_json = json.loads(record["cdt_json"])
            print(f"CDT JSON parsed successfully")
            
            # Extract topics
            if "topics" in cdt_json:
                topics = cdt_json["topics"]
                print(f"Found {len(topics)} topics")
                
                print(f"\nORIGINAL TOPICS STRUCTURE:")
                print(f"{'-'*80}")
                # Print just the first topic for brevity
                if topics:
                    first_key = next(iter(topics))
                    print(json.dumps({first_key: topics[first_key]}, indent=2))
                    print(f"... ({len(topics)-1} more topics)")
                    
                # Transform topics
                transformed_topics = transform_topics_for_db(topics)
                print(f"\nTRANSFORMED TOPICS STRUCTURE:")
                print(f"{'-'*80}")
                # Print just the first topic for brevity
                if transformed_topics:
                    first_key = next(iter(transformed_topics))
                    print(json.dumps({first_key: transformed_topics[first_key]}, indent=2))
                    print(f"... ({len(transformed_topics)-1} more topics)")
            else:
                print("No topics found in record")
                print("Available keys:", list(cdt_json.keys()))
                
        except json.JSONDecodeError as e:
            print(f"Error parsing CDT JSON data: {e}")
            print("First 100 bytes of CDT JSON:", record["cdt_json"][:100])
    else:
        print("No CDT data found in record")
    
    print(f"\n{'='*80}\n")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_record_format.py [record_id]")
        sys.exit(1)
    
    record_id = sys.argv[1]
    check_record_format(record_id) 