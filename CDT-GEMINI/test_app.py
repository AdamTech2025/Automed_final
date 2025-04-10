#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import analyze_dental_scenario_cli
from supabase import MedicalCodingDB
import json

def test_app_with_sample_data():
    """Run the application with a sample dental scenario and check the database records."""
    print("=== TESTING APP WITH SAMPLE DENTAL SCENARIO ===")
    
    # Sample dental scenario
    sample_scenario = "A new patient, age 11, was seen for a first exam, cleaning, and fluoride varnish application. During the exam, the dentist noted that the erupting tooth #4 was impinging on the fixed space maintainer that spanned both the right and left side of the mouth. This space maintainer had been placed by another dentist but it was decided that the space maintainer needed to be removed now."
    
    # Run the analysis
    print("\nRunning analysis with sample scenario...")
    analyze_dental_scenario_cli(sample_scenario)
    
    # Check the database records
    print("\n=== CHECKING DATABASE RECORDS ===")
    db = MedicalCodingDB()
    
    try:
        # Get the most recent record
        db.cursor.execute("""
            SELECT id, user_question, processed_clean_data, cdt_result, icd_result
            FROM dental_report 
            ORDER BY created_at DESC
            LIMIT 1
        """)
        record = db.cursor.fetchone()
        
        if not record:
            print("No records found in the database.")
            return
            
        record_id, user_question, processed_scenario, cdt_result_json, icd_result_json = record
        
        # Basic record information
        print(f"\nRecord ID: {record_id}")
        print(f"Question Length: {len(user_question)} characters")
        print(f"Processed Scenario Length: {len(processed_scenario)} characters")
        
        # Parse and analyze CDT result
        try:
            cdt_data = json.loads(cdt_result_json)
            print(f"\nCDT Result Data:")
            print(f"- Size: {len(cdt_result_json)} bytes")
            print(f"- Contains cdt_classifier: {'cdt_classifier' in cdt_data}")
            print(f"- Contains topics: {'topics' in cdt_data}")
            print(f"- Contains inspector_results: {'inspector_results' in cdt_data}")
            print(f"- Contains subtopics_data: {'subtopics_data' in cdt_data}")
            
            # Check for CDT classifier data
            if 'cdt_classifier' in cdt_data:
                classifier = cdt_data['cdt_classifier']
                print(f"\nCDT Classifier Data:")
                print(f"- Contains formatted_results: {'formatted_results' in classifier}")
                print(f"- Contains range_codes_string: {'range_codes_string' in classifier}")
                if 'range_codes_string' in classifier:
                    print(f"- Range Codes: {classifier['range_codes_string']}")
            
            # Check for topics data
            if 'topics' in cdt_data:
                topics = cdt_data['topics']
                print(f"\nTopics Data:")
                print(f"- Number of topics: {len(topics)}")
                for code_range, topic_data in topics.items():
                    print(f"- Topic: {topic_data.get('name', 'Unknown')} ({code_range})")
            
            # Check for subtopics data
            if 'subtopics_data' in cdt_data:
                subtopics = cdt_data['subtopics_data']
                print(f"\nSubtopics Data:")
                print(f"- Number of entries: {len(subtopics)}")
                for code_range, subtopic_data in subtopics.items():
                    activated = subtopic_data.get('activated_subtopics', [])
                    print(f"- {subtopic_data.get('topic_name', 'Unknown')} ({code_range}):")
                    print(f"  - Activated subtopics: {len(activated)}")
            
            # Check for inspector results
            if 'inspector_results' in cdt_data:
                inspector = cdt_data['inspector_results']
                print(f"\nInspector Results:")
                print(f"- Contains codes: {'codes' in inspector}")
                if 'codes' in inspector:
                    print(f"- Number of codes: {len(inspector['codes'])}")
                    print(f"- Codes: {inspector['codes']}")
        
        except json.JSONDecodeError as e:
            print(f"Error parsing CDT JSON data: {str(e)}")
        
        # Parse and analyze ICD result
        try:
            icd_data = json.loads(icd_result_json)
            print(f"\nICD Result Data:")
            print(f"- Size: {len(icd_result_json)} bytes")
            print(f"- Contains categories: {'categories' in icd_data}")
            print(f"- Contains code_lists: {'code_lists' in icd_data}")
            print(f"- Contains inspector_results: {'inspector_results' in icd_data}")
            
            # Check for categories
            if 'categories' in icd_data:
                print(f"\nICD Categories:")
                print(f"- Number of categories: {len(icd_data['categories'])}")
                for i, category in enumerate(icd_data['categories']):
                    print(f"- Category {i+1}: {category}")
            
            # Check for inspector results
            if 'inspector_results' in icd_data:
                inspector = icd_data['inspector_results']
                print(f"\nICD Inspector Results:")
                print(f"- Contains codes: {'codes' in inspector}")
                if 'codes' in inspector:
                    print(f"- Number of codes: {len(inspector['codes'])}")
                    print(f"- Codes: {inspector['codes']}")
        
        except json.JSONDecodeError as e:
            print(f"Error parsing ICD JSON data: {str(e)}")
        
        # Export the data for detailed inspection
        print("\nExporting data for detailed inspection...")
        db.export_analysis_results(record_id)
        
    except Exception as e:
        print(f"Error checking database records: {str(e)}")
    
    finally:
        db.close_connection()
        print("\n=== TEST COMPLETED ===")

if __name__ == "__main__":
    test_app_with_sample_data() 