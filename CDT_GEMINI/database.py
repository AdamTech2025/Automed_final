from supabase import create_client, Client
import os
from dotenv import load_dotenv
import uuid
from datetime import datetime
import json
import logging

load_dotenv()

logger = logging.getLogger(__name__)

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

    def create_analysis_record(self, data: dict, user_id: str | None = None):
        """Insert a new record into the dental_report table."""
        self.ensure_connection()
        try:
            record_data = {
                "user_question": data.get("user_question", ""),
                "processed_clean_data": data.get("processed_clean_data", ""),
                "cdt_result": data.get("cdt_result", "{}"),
                "icd_result": data.get("icd_result", "{}"),
                "questioner_data": data.get("questioner_data", "{}"),
                "inspector_results": data.get("inspector_results", "{}"),
                "user_id": user_id
            }
            
            result = self.supabase.table("dental_report").insert(record_data).execute()
            if result.data and len(result.data) > 0:
                new_id = result.data[0].get('id')
                logger.info(f"✅ Analysis record added successfully with ID: {new_id} for user: {user_id or 'Anonymous'}")
                return result.data
            else:
                logger.error(f"❌ Supabase insert for dental_report returned no data. User: {user_id or 'Anonymous'}, Input Data: {data}")
                return None
        except Exception as e:
            logger.error(f"❌ Error creating analysis record for user {user_id or 'Anonymous'}: {str(e)}", exc_info=True)
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

    def get_complete_analysis(self, record_id):
        """Retrieve a complete analysis record by its ID."""
        self.ensure_connection()
        try:
            result = self.supabase.table("dental_report").select(
                "processed_clean_data, cdt_result, icd_result, questioner_data, user_question, inspector_results"
            ).eq("id", record_id).execute()
            
            if result.data:
                record = result.data[0]
                cdt_size = len(record['cdt_result']) if record['cdt_result'] else 0
                icd_size = len(record['icd_result']) if record['icd_result'] else 0
                questioner_size = len(record['questioner_data']) if record['questioner_data'] else 0
                inspector_size = len(record['inspector_results']) if 'inspector_results' in record and record['inspector_results'] else 0
                print(f"Retrieved complete record ID: {record_id}")
                print(f"- CDT data size: {cdt_size} bytes")
                print(f"- ICD data size: {icd_size} bytes")
                print(f"- Questioner data size: {questioner_size} bytes")
                print(f"- Inspector data size: {inspector_size} bytes")
                return record
            else:
                print(f"No record found with ID: {record_id}")
                return None
        except Exception as e:
            print(f"❌ Error retrieving complete analysis by ID: {str(e)}")
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

    def update_inspector_results(self, record_id, inspector_results):
        """Update the inspector results for a given record."""
        self.ensure_connection()
        try:
            result = self.supabase.table("dental_report").update({
                "inspector_results": inspector_results
            }).eq("id", record_id).execute()
            
            print(f"✅ Inspector results updated successfully for ID: {record_id}")
            return True
        except Exception as e:
            print(f"❌ Error updating inspector results: {str(e)}")
            return False

    def get_user_by_email(self, email: str):
        """Retrieve a user record by email address."""
        self.ensure_connection()
        try:
            result = self.supabase.table("Users").select("*").eq("email", email).limit(1).execute()
            if result.data:
                logger.info(f"User found with email: {email}")
                return result.data[0]
            else:
                logger.info(f"No user found with email: {email}")
                return None
        except Exception as e:
            logger.error(f"Error retrieving user by email {email}: {str(e)}", exc_info=True)
            return None

    def create_user(self, user_data: dict):
        """Insert a new user record (initially unverified)."""
        self.ensure_connection()
        try:
            if not user_data.get('name') or not user_data.get('email'):
                raise ValueError("Name and email are required to create a user.")
            # Also require hashed_password for creation now
            if not user_data.get('hashed_password'):
                raise ValueError("Hashed password is required to create a user.")
                
            data_to_insert = {
                "name": user_data['name'],
                "email": user_data['email'],
                "hashed_password": user_data['hashed_password'], # Store the hashed password
                "phone": user_data.get('phone'), # Optional
                "is_email_verified": False # Default to false
            }
            result = self.supabase.table("Users").insert(data_to_insert).execute()
            if result.data:
                logger.info(f"New user created successfully with email: {user_data['email']}")
                return result.data
            else:
                logger.error(f"Supabase insert operation did not return data for email: {user_data['email']}")
                return None
        except Exception as e:
            # Catch potential unique constraint violation for email
            if "violates unique constraint" in str(e):
                 logger.warning(f"Attempted to create user with existing email: {user_data.get('email')}")
                 # Optionally, retrieve and return the existing user here if needed
                 # return self.get_user_by_email(user_data['email'])
                 raise ValueError(f"Email {user_data.get('email')} already exists.")
            logger.error(f"Error creating user {user_data.get('email')}: {str(e)}", exc_info=True)
            return None
            
    def update_user_details(self, user_id: str, details: dict):
        """Update user details like name or phone."""
        self.ensure_connection()
        try:
            update_data = {}
            if 'name' in details: update_data['name'] = details['name']
            if 'phone' in details: update_data['phone'] = details['phone']
            
            if not update_data:
                 logger.warning(f"No details provided to update for user ID: {user_id}")
                 return False
                 
            result = self.supabase.table("Users").update(update_data).eq("id", user_id).execute()
            # Check if the update affected any rows (Supabase might return empty data if no match)
            # Supabase Python v1 might not provide count, rely on lack of error for now
            logger.info(f"User details updated for ID: {user_id}")
            return True
        except Exception as e:
            logger.error(f"Error updating details for user ID {user_id}: {str(e)}", exc_info=True)
            return False

    def update_user_otp(self, user_id: str, otp: str | None, otp_expires_at: datetime | None):
        """Update the user's current OTP and its expiry time."""
        self.ensure_connection()
        try:
            expiry_str = otp_expires_at.isoformat() if otp_expires_at else None
            result = self.supabase.table("Users").update({
                "otp": otp,
                "otp_expires_at": expiry_str
            }).eq("id", user_id).execute()
            logger.info(f"OTP updated for user ID: {user_id}")
            return True
        except Exception as e:
            logger.error(f"Error updating OTP for user ID {user_id}: {str(e)}", exc_info=True)
            return False

    def verify_user_email(self, user_id: str):
        """Mark the user's email as verified and clear OTP fields."""
        self.ensure_connection()
        try:
            result = self.supabase.table("Users").update({
                "is_email_verified": True,
                "otp": None,  # Clear OTP after verification
                "otp_expires_at": None # Clear expiry
            }).eq("id", user_id).execute()
            logger.info(f"Email verified for user ID: {user_id}")
            return True
        except Exception as e:
            logger.error(f"Error verifying email for user ID {user_id}: {str(e)}", exc_info=True)
            return False

    def save_code_selections(self, record_id, accepted_cdt, rejected_cdt, accepted_icd, rejected_icd, user_id: str | None = None):
        """Insert or update code selections in the code_selections table."""
        self.ensure_connection()
        try:
            selection_data = {
                "analysis_record_id": record_id,
                "accepted_cdt_codes": accepted_cdt,
                "rejected_cdt_codes": rejected_cdt,
                "accepted_icd_codes": accepted_icd,
                "rejected_icd_codes": rejected_icd,
                "user_id": user_id
                # selection_timestamp will be set by default in the DB
            }
            
            # Upsert based on the analysis_record_id to handle resubmissions
            result = self.supabase.table("code_selections").upsert(
                selection_data,
                on_conflict="analysis_record_id" 
            ).execute()
            
            if result.data:
                logger.info(f"✅ Code selections saved/updated successfully for analysis record ID: {record_id} by user: {user_id or 'Anonymous'}")
                return result.data[0] # Return the saved/updated record
            else:
                 # Handle potential case where upsert might not return data as expected (check Supabase docs/behavior)
                 logger.warning(f"⚠️ Code selections upsert executed for {record_id} by user {user_id or 'Anonymous'}, but no data returned in response.")
                 # We might assume success if no exception was raised.
                 return { # Return the input data as confirmation
                     "analysis_record_id": record_id,
                     "accepted_cdt_codes": accepted_cdt,
                     "rejected_cdt_codes": rejected_cdt,
                     "accepted_icd_codes": accepted_icd,
                     "rejected_icd_codes": rejected_icd,
                     "user_id": user_id
                 }

        except Exception as e:
            logger.error(f"❌ Error saving code selections for record {record_id} by user {user_id or 'Anonymous'}: {str(e)}", exc_info=True)
            # Consider re-raising or returning a specific error indicator
            # raise e 
            return None

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

    def add_code_analysis(self, scenario: str, cdt_codes: str, response: str, user_id: str | None = None) -> int | None:
        """Add a new dental code analysis record."""
        self.ensure_connection()
        try:
            record_data = {
                "scenario": scenario,
                "cdt_codes": cdt_codes,
                "response": response,
                "user_id": user_id
            }
            
            result = self.supabase.table("dental_code_analysis").insert(record_data).execute()
            if result.data and len(result.data) > 0:
                new_id = result.data[0].get('id')
                logger.info(f"✅ Code analysis record added successfully with ID: {new_id} for user: {user_id or 'Anonymous'}")
                return str(new_id) if new_id else None
            else:
                logger.error(f"❌ Supabase insert for dental_code_analysis returned no data. User: {user_id or 'Anonymous'}, Input Data: {record_data}")
                return None
        except Exception as e:
            logger.error(f"❌ Error adding code analysis for user {user_id or 'Anonymous'}: {str(e)}", exc_info=True)
            return None

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


