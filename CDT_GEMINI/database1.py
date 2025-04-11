from supabase import create_client, Client
import os
from dotenv import load_dotenv
import uuid
from datetime import datetime
import json

load_dotenv()

class MedicalCodingDB:
    def __init__(self):
        self.url: str = os.getenv("SUPABASE_URL")
        self.key: str = os.getenv("SUPABASE_KEY")
        self.supabase: Client = create_client(self.url, self.key)

    def connect(self):
        if not self.url or not self.key:
            raise ValueError("Supabase URL and key must be set")
        self.supabase = create_client(self.url, self.key)

    def ensure_connection(self):
        if not self.supabase:
            self.connect()

    def create_analysis_record(self, data: dict):
        """Insert a new record into the dental_report table."""
        self.ensure_connection()
        try:
            record_data = {
                "user_question": data.get("user_question", ""),
                "processed_clean_data": data.get("processed_clean_data", ""),
                "cdt_result": data.get("cdt_result", "{}"),
                "icd_result": data.get("icd_result", "{}"),
                "questioner_data": data.get("questioner_data", "{}")
            }
            
            result = self.supabase.table("dental_report").insert(record_data).execute()
            print(f"✅ Analysis record added successfully with ID: {result.data[0]['id']}")
            return result.data
        except Exception as e:
            print(f"❌ Error creating analysis record: {str(e)}")
            return None

    def update_processed_scenario(self, record_id, processed_scenario):
        """Update the processed scenario for a given record."""
        self.ensure_connection()
        try:
            result = self.supabase.table("dental_report").update(
                {"processed_clean_data": processed_scenario}
            ).eq("id", record_id).execute()
            
            print(f"✅ Processed scenario updated successfully for ID: {record_id}")
            return True
        except Exception as e:
            print(f"❌ Error updating processed scenario: {str(e)}")
            return False

    def update_analysis_results(self, record_id, cdt_result, icd_result):
        """Update the CDT and ICD results for a given record."""
        self.ensure_connection()
        try:
            cdt_size = len(cdt_result) if cdt_result else 0
            icd_size = len(icd_result) if icd_result else 0
            print(f"Storing CDT result (size: {cdt_size} bytes) and ICD result (size: {icd_size} bytes)")
            
            result = self.supabase.table("dental_report").update({
                "cdt_result": cdt_result,
                "icd_result": icd_result
            }).eq("id", record_id).execute()
            
            print(f"✅ Analysis results updated successfully for ID: {record_id}")
            return True
        except Exception as e:
            print(f"❌ Error updating analysis results: {str(e)}")
            return False

    def get_analysis_by_id(self, record_id):
        """Retrieve a single analysis record by its ID."""
        self.ensure_connection()
        try:
            result = self.supabase.table("dental_report").select(
                "processed_clean_data, cdt_result, icd_result"
            ).eq("id", record_id).execute()
            
            if result.data:
                record = result.data[0]
                cdt_size = len(record['cdt_result']) if record['cdt_result'] else 0
                icd_size = len(record['icd_result']) if record['icd_result'] else 0
                print(f"Retrieved record ID: {record_id} - CDT data size: {cdt_size} bytes, ICD data size: {icd_size} bytes")
                return record
            else:
                print(f"No record found with ID: {record_id}")
                return None
        except Exception as e:
            print(f"❌ Error retrieving analysis by ID: {str(e)}")
            return None

    def get_latest_processed_scenario(self):
        """Retrieve the latest processed scenario."""
        self.ensure_connection()
        try:
            result = self.supabase.table("dental_report").select(
                "processed_clean_data"
            ).order("created_at", desc=True).limit(1).execute()
            
            if result.data and result.data[0]['processed_clean_data']:
                return result.data[0]['processed_clean_data']
            return None
        except Exception as e:
            print(f"❌ Error getting latest processed scenario: {str(e)}")
            return None

    def get_all_analyses(self):
        """Retrieve all analysis records."""
        self.ensure_connection()
        try:
            result = self.supabase.table("dental_report").select("*").order("created_at", desc=True).execute()
            return result.data
        except Exception as e:
            print(f"❌ Error getting all analyses: {str(e)}")
            return []

    def update_questioner_data(self, record_id, questioner_data):
        """Update the questioner data for a given record."""
        self.ensure_connection()
        try:
            result = self.supabase.table("dental_report").update({
                "questioner_data": questioner_data
            }).eq("id", record_id).execute()
            
            print(f"✅ Questioner data updated successfully for ID: {record_id}")
            return True
        except Exception as e:
            print(f"❌ Error updating questioner data: {str(e)}")
            return False

    def export_analysis_results(self, record_id, export_dir=None):
        """Export CDT and ICD results for a given record to JSON files."""
        try:
            if not export_dir:
                export_dir = os.path.dirname(os.path.abspath(__file__))
            
            if not os.path.exists(export_dir):
                os.makedirs(export_dir)
            
            result = self.supabase.table("dental_report").select(
                "processed_clean_data, cdt_result, icd_result, user_question"
            ).eq("id", record_id).execute()
            
            if not result.data:
                print(f"❌ No record found with ID: {record_id}")
                return False
            
            record = result.data[0]
            processed_scenario = record['processed_clean_data']
            cdt_result_json = record['cdt_result']
            icd_result_json = record['icd_result']
            user_question = record['user_question']
            
            try:
                cdt_data = json.loads(cdt_result_json) if cdt_result_json else {}
                icd_data = json.loads(icd_result_json) if icd_result_json else {}
            except json.JSONDecodeError as e:
                print(f"❌ Error parsing JSON data: {str(e)}")
                return False
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            cdt_filename = os.path.join(export_dir, f"cdt_result_{record_id}_{timestamp}.json")
            icd_filename = os.path.join(export_dir, f"icd_result_{record_id}_{timestamp}.json")
            summary_filename = os.path.join(export_dir, f"analysis_summary_{record_id}_{timestamp}.txt")
            
            with open(cdt_filename, 'w') as f:
                json.dump(cdt_data, f, indent=2)
            
            with open(icd_filename, 'w') as f:
                json.dump(icd_data, f, indent=2)
            
            with open(summary_filename, 'w') as f:
                f.write(f"ANALYSIS SUMMARY FOR RECORD: {record_id}\n")
                f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(f"USER QUESTION:\n{user_question}\n\n")
                f.write(f"PROCESSED SCENARIO:\n{processed_scenario}\n\n")
                
                if 'cdt_classifier' in cdt_data and 'range_codes_string' in cdt_data['cdt_classifier']:
                    f.write(f"CDT Code Ranges: {cdt_data['cdt_classifier']['range_codes_string']}\n")
                
                if 'subtopics_data' in cdt_data:
                    f.write("\nACTIVATED TOPICS AND SUBTOPICS:\n")
                    for code_range, subtopic_data in cdt_data['subtopics_data'].items():
                        f.write(f"- {subtopic_data.get('topic_name', 'Unknown')} ({code_range}):\n")
                        for subtopic in subtopic_data.get('activated_subtopics', []):
                            f.write(f"  - {subtopic}\n")
                
                if 'inspector_results' in cdt_data and 'codes' in cdt_data['inspector_results']:
                    f.write("\nVALIDATED CDT CODES:\n")
                    for code in cdt_data['inspector_results']['codes']:
                        f.write(f"- {code}\n")
                    if 'explanation' in cdt_data['inspector_results']:
                        f.write(f"\nExplanation: {cdt_data['inspector_results']['explanation']}\n")
                
                f.write("\nICD ANALYSIS SUMMARY:\n")
                if 'categories' in icd_data:
                    for i, category in enumerate(icd_data.get('categories', [])):
                        f.write(f"- Category: {category}\n")
                        if 'code_lists' in icd_data and i < len(icd_data['code_lists']):
                            f.write(f"  Codes: {', '.join(icd_data['code_lists'][i])}\n")
                        if 'explanations' in icd_data and i < len(icd_data['explanations']):
                            f.write(f"  Explanation: {icd_data['explanations'][i]}\n")
                
                if 'inspector_results' in icd_data and 'codes' in icd_data['inspector_results']:
                    f.write("\nVALIDATED ICD CODES:\n")
                    for code in icd_data['inspector_results']['codes']:
                        f.write(f"- {code}\n")
                    if 'explanation' in icd_data['inspector_results']:
                        f.write(f"\nExplanation: {icd_data['inspector_results']['explanation']}\n")
            
            print(f"✅ Analysis results exported successfully:")
            print(f"- CDT data saved to: {cdt_filename}")
            print(f"- ICD data saved to: {icd_filename}")
            print(f"- Summary saved to: {summary_filename}")
            return True
        except Exception as e:
            print(f"❌ Error exporting analysis results: {str(e)}")
            return False

    def get_most_recent_analysis(self):
        """Get the most recent analysis record from the database."""
        try:
            result = self.supabase.table("dental_report").select(
                "id, user_question, processed_clean_data, created_at"
            ).order("created_at", desc=True).limit(1).execute()
            
            if result.data:
                record = result.data[0]
                print(f"✅ Retrieved most recent analysis record:")
                print(f"- ID: {record['id']}")
                print(f"- Created at: {record['created_at']}")
                print(f"- Question: {record['user_question'][:50]}...")
                return record['id']
            else:
                print("No analysis records found in the database")
                return None
        except Exception as e:
            print(f"❌ Error retrieving most recent analysis: {str(e)}")
            return None

    def add_code_analysis(self, scenario: str, cdt_codes: str, response: str) -> int:
        """Add a new dental code analysis record."""
        self.ensure_connection()
        try:
            record_data = {
                "scenario": scenario,
                "cdt_codes": cdt_codes,
                "response": response
            }
            
            result = self.supabase.table("dental_code_analysis").insert(record_data).execute()
            print(f"✅ Code analysis record added successfully with ID: {result.data[0]['id']}")
            return result.data[0]['id']
        except Exception as e:
            print(f"❌ Error adding code analysis: {str(e)}")
            raise

# ===========================
# Example Usage
# ===========================
if __name__ == "__main__":
    db = MedicalCodingDB()
    db.connect()
    print("Database connected")
    
    # Show menu of options
    print("\nDental Analysis Database Tools")
    print("==============================")
    print("1. Export most recent analysis results")
    print("2. Export specific analysis results (enter ID)")
    print("3. View all analysis records")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ")
    
    if choice == "1":
        most_recent_id = db.get_most_recent_analysis()
        if most_recent_id:
            db.export_analysis_results(most_recent_id)
    
    elif choice == "2":
        record_id = input("Enter the analysis record ID to export: ")
        db.export_analysis_results(record_id)
    
    elif choice == "3":
        records = db.get_all_analyses()
        if records:
            print("\nAll Analysis Records:")
            print("=====================")
            for record in records:
                cdt_size = len(record['cdt_result']) if record['cdt_result'] else 0
                icd_size = len(record['icd_result']) if record['icd_result'] else 0
                print(f"ID: {record['id']}")
                print(f"Created: {record['created_at']}")
                print(f"Question: {record['user_question'][:50]}...")
                print(f"CDT Data Size: {cdt_size} bytes")
                print(f"ICD Data Size: {icd_size} bytes")
                print("-" * 40)
    
    print("Database tool completed")


