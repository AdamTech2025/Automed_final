import sqlite3
import uuid
from datetime import datetime
import os
import time
import json

class MedicalCodingDB:
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MedicalCodingDB, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "med_gpt.sqlite3")
            self.conn = None
            self.cursor = None
            self.connect()
            self._initialized = True
    
    def connect(self):
        """Establish database connection."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            self.create_tables()
            print("✅ Database connected successfully")
        except Exception as e:
            print(f"❌ Database connection error: {str(e)}")
            self.conn = None
            self.cursor = None
            raise
    
    def ensure_connection(self):
        """Check if the connection is valid and reconnect if needed."""
        if self.conn is None or self.cursor is None:
            print("Database connection is not established, reconnecting...")
            self.connect()
            return True
            
        # Test if the connection is still valid
        try:
            self.cursor.execute("SELECT 1")
            return True
        except sqlite3.Error:
            print("Database connection lost, reconnecting...")
            self.close_connection()
            self.connect()
            return True
        except Exception as e:
            print(f"❌ Error checking database connection: {str(e)}")
            self.close_connection()
            self.connect()
            return True
    
    def create_tables(self):
        """Create necessary database tables if they don't exist."""
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS dental_report (
                    id TEXT PRIMARY KEY,
                    user_question TEXT,
                    processed_clean_data TEXT,
                    cdt_result TEXT,
                    icd_result TEXT,
                    questioner_data TEXT,
                    created_at DATETIME DEFAULT (datetime('now', 'localtime'))
                )
            """)
            
            # Check if questioner_data column exists, if not add it
            try:
                self.cursor.execute("SELECT questioner_data FROM dental_report LIMIT 1")
            except sqlite3.OperationalError:
                # Column doesn't exist, so add it
                self.cursor.execute("ALTER TABLE dental_report ADD COLUMN questioner_data TEXT")
                print("✅ Added questioner_data column to existing table")
                
            self.conn.commit()
            print("✅ Database table created/verified successfully")
        except Exception as e:
            print(f"❌ Table creation error: {str(e)}")
            raise

    def create_analysis_record(self, data: dict):
        """Insert a new record into the dental_analysis table."""
        self.ensure_connection()
        try:
            record_id = str(uuid.uuid4())
            query = """
            INSERT INTO dental_report (
                id, user_question, processed_clean_data, 
                cdt_result, icd_result, questioner_data
            ) VALUES (?, ?, ?, ?, ?, ?)
            """
            values = (
                record_id,
                data.get("user_question", ""),
                data.get("processed_clean_data", ""),
                data.get("cdt_result", "{}"),
                data.get("icd_result", "{}"),
                data.get("questioner_data", "{}")
            )
            self.cursor.execute(query, values)
            self.conn.commit()
            print(f"✅ Analysis record added successfully with ID: {record_id}")
            return [{"id": record_id}]
        except sqlite3.OperationalError as e:
            print(f"❌ Error creating analysis record: {str(e)}")
            # Try to reconnect and retry once
            self.connect()
            self.cursor.execute(query, values)
            self.conn.commit()
            return [{"id": record_id}]
        except Exception as e:
            print(f"❌ Error creating analysis record: {str(e)}")
            return None

    def update_processed_scenario(self, record_id, processed_scenario):
        """Update the processed scenario for a given record."""
        self.ensure_connection()
        try:
            query = """
            UPDATE dental_report 
            SET processed_clean_data = ?
            WHERE id = ?
            """
            self.cursor.execute(query, (processed_scenario, record_id))
            self.conn.commit()
            print(f"✅ Processed scenario updated successfully for ID: {record_id}")
            return True
        except Exception as e:
            print(f"❌ Error updating processed scenario: {str(e)}")
            # Try to reconnect and retry once
            try:
                self.connect()
                self.cursor.execute(query, (processed_scenario, record_id))
                self.conn.commit()
                print(f"✅ Retry: Processed scenario updated successfully for ID: {record_id}")
                return True
            except Exception as retry_e:
                print(f"❌ Retry failed: {str(retry_e)}")
                return False

    def update_analysis_results(self, record_id, cdt_result, icd_result):
        """Update the CDT and ICD results for a given record."""
        self.ensure_connection()
        try:
            # Log the size of data being stored
            cdt_size = len(cdt_result) if cdt_result else 0
            icd_size = len(icd_result) if icd_result else 0
            print(f"Storing CDT result (size: {cdt_size} bytes) and ICD result (size: {icd_size} bytes)")
            
            query = """
            UPDATE dental_report 
            SET cdt_result = ?, icd_result = ?
            WHERE id = ?
            """
            self.cursor.execute(query, (cdt_result, icd_result, record_id))
            self.conn.commit()
            print(f"✅ Analysis results updated successfully for ID: {record_id}")
            
            # Verify the data was stored correctly
            self.cursor.execute("SELECT length(cdt_result), length(icd_result) FROM dental_report WHERE id = ?", (record_id,))
            stored_sizes = self.cursor.fetchone()
            if stored_sizes:
                print(f"✓ Verified: CDT data stored ({stored_sizes[0]} bytes), ICD data stored ({stored_sizes[1]} bytes)")
            
            return True
        except Exception as e:
            print(f"❌ Error updating analysis results: {str(e)}")
            # Try to reconnect and retry once
            try:
                self.connect()
                self.cursor.execute(query, (cdt_result, icd_result, record_id))
                self.conn.commit()
                print(f"✅ Retry: Analysis results updated successfully for ID: {record_id}")
                return True
            except Exception as retry_e:
                print(f"❌ Retry failed: {str(retry_e)}")
                return False

    def get_analysis_by_id(self, record_id):
        """Retrieve a single analysis record by its ID."""
        self.ensure_connection()
        try:
            query = "SELECT processed_clean_data, cdt_result, icd_result FROM dental_report WHERE id = ?"
            self.cursor.execute(query, (record_id,))
            record = self.cursor.fetchone()
            
            if record:
                cdt_size = len(record[1]) if record[1] else 0
                icd_size = len(record[2]) if record[2] else 0
                print(f"Retrieved record ID: {record_id} - CDT data size: {cdt_size} bytes, ICD data size: {icd_size} bytes")
            else:
                print(f"No record found with ID: {record_id}")
            
            return record
        except Exception as e:
            print(f"❌ Error retrieving analysis by ID: {str(e)}")
            # Try to reconnect and retry once
            try:
                self.connect()
                self.cursor.execute(query, (record_id,))
                return self.cursor.fetchone()
            except Exception:
                return None
    
    def get_latest_processed_scenario(self):
        """Retrieve the latest processed scenario."""
        self.ensure_connection()
        try:
            query = "SELECT processed_clean_data FROM dental_report WHERE processed_clean_data IS NOT NULL AND processed_clean_data != '' ORDER BY created_at DESC LIMIT 1"
            self.cursor.execute(query)
            record = self.cursor.fetchone()
            if record and record[0]:
                return record[0]
            return None
        except Exception as e:
            print(f"❌ Error getting latest processed scenario: {str(e)}")
            return None

    def get_all_analyses(self):
        """Retrieve all analysis records."""
        self.ensure_connection()
        query = "SELECT * FROM dental_report ORDER BY created_at DESC"
        self.cursor.execute(query)
        records = self.cursor.fetchall()
        return records

    def close_connection(self):
        """Close the database connection."""
        if self.conn:
            try:
                self.conn.close()
                self.conn = None
                self.cursor = None
                print("✅ Database connection closed successfully")
            except Exception as e:
                print(f"❌ Error closing database connection: {str(e)}")
                # Reset connection objects even if close fails
                self.conn = None
                self.cursor = None

    def __del__(self):
        """Ensure connection is closed when object is destroyed."""
        self.close_connection()

    def update_questioner_data(self, record_id, questioner_data):
        """Update the questioner data for a given record."""
        self.ensure_connection()
        try:
            query = """
            UPDATE dental_report 
            SET questioner_data = ?
            WHERE id = ?
            """
            self.cursor.execute(query, (questioner_data, record_id))
            self.conn.commit()
            print(f"✅ Questioner data updated successfully for ID: {record_id}")
            return True
        except Exception as e:
            print(f"❌ Error updating questioner data: {str(e)}")
            # Try to reconnect and retry once
            try:
                self.connect()
                self.cursor.execute(query, (questioner_data, record_id))
                self.conn.commit()
                print(f"✅ Retry: Questioner data updated successfully for ID: {record_id}")
                return True
            except Exception as retry_e:
                print(f"❌ Retry failed: {str(retry_e)}")
                return False

    def export_analysis_results(self, record_id, export_dir=None):
        """Export CDT and ICD results for a given record to JSON files for inspection."""
        try:
            # Default to current directory if not specified
            if not export_dir:
                export_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Make sure the directory exists
            if not os.path.exists(export_dir):
                os.makedirs(export_dir)
            
            # Get the record data
            query = "SELECT processed_clean_data, cdt_result, icd_result, user_question FROM dental_report WHERE id = ?"
            self.cursor.execute(query, (record_id,))
            record = self.cursor.fetchone()
            
            if not record:
                print(f"❌ No record found with ID: {record_id}")
                return False
            
            processed_scenario, cdt_result_json, icd_result_json, user_question = record
            
            # Parse the JSON data
            try:
                cdt_data = json.loads(cdt_result_json) if cdt_result_json else {}
                icd_data = json.loads(icd_result_json) if icd_result_json else {}
            except json.JSONDecodeError as e:
                print(f"❌ Error parsing JSON data: {str(e)}")
                return False
            
            # Create the export files
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            cdt_filename = os.path.join(export_dir, f"cdt_result_{record_id}_{timestamp}.json")
            icd_filename = os.path.join(export_dir, f"icd_result_{record_id}_{timestamp}.json")
            summary_filename = os.path.join(export_dir, f"analysis_summary_{record_id}_{timestamp}.txt")
            
            # Save the CDT data
            with open(cdt_filename, 'w') as f:
                json.dump(cdt_data, f, indent=2)
            
            # Save the ICD data
            with open(icd_filename, 'w') as f:
                json.dump(icd_data, f, indent=2)
            
            # Create a summary file
            with open(summary_filename, 'w') as f:
                f.write(f"ANALYSIS SUMMARY FOR RECORD: {record_id}\n")
                f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(f"USER QUESTION:\n{user_question}\n\n")
                f.write(f"PROCESSED SCENARIO:\n{processed_scenario}\n\n")
                
                # Write CDT summary
                f.write("CDT ANALYSIS SUMMARY:\n")
                if 'cdt_classifier' in cdt_data and 'range_codes_string' in cdt_data['cdt_classifier']:
                    f.write(f"CDT Code Ranges: {cdt_data['cdt_classifier']['range_codes_string']}\n")
                
                # Write topic and subtopic summary
                if 'subtopics_data' in cdt_data:
                    f.write("\nACTIVATED TOPICS AND SUBTOPICS:\n")
                    for code_range, subtopic_data in cdt_data['subtopics_data'].items():
                        f.write(f"- {subtopic_data.get('topic_name', 'Unknown')} ({code_range}):\n")
                        for subtopic in subtopic_data.get('activated_subtopics', []):
                            f.write(f"  - {subtopic}\n")
                
                # Write inspector results
                if 'inspector_results' in cdt_data and 'codes' in cdt_data['inspector_results']:
                    f.write("\nVALIDATED CDT CODES:\n")
                    for code in cdt_data['inspector_results']['codes']:
                        f.write(f"- {code}\n")
                    if 'explanation' in cdt_data['inspector_results']:
                        f.write(f"\nExplanation: {cdt_data['inspector_results']['explanation']}\n")
                
                # Write ICD summary
                f.write("\nICD ANALYSIS SUMMARY:\n")
                if 'categories' in icd_data:
                    for i, category in enumerate(icd_data.get('categories', [])):
                        f.write(f"- Category: {category}\n")
                        if 'code_lists' in icd_data and i < len(icd_data['code_lists']):
                            f.write(f"  Codes: {', '.join(icd_data['code_lists'][i])}\n")
                        if 'explanations' in icd_data and i < len(icd_data['explanations']):
                            f.write(f"  Explanation: {icd_data['explanations'][i]}\n")
                
                # Write ICD inspector results
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
            query = """
            SELECT id, user_question, processed_clean_data, created_at 
            FROM dental_report 
            ORDER BY created_at DESC 
            LIMIT 1
            """
            self.cursor.execute(query)
            record = self.cursor.fetchone()
            
            if record:
                record_id, user_question, processed_scenario, created_at = record
                print(f"✅ Retrieved most recent analysis record:")
                print(f"- ID: {record_id}")
                print(f"- Created at: {created_at}")
                print(f"- Question: {user_question[:50]}...")
                return record_id
            else:
                print("No analysis records found in the database")
                return None
        except Exception as e:
            print(f"❌ Error retrieving most recent analysis: {str(e)}")
            return None

# ===========================
# Example Usage
# ===========================
if __name__ == "__main__":
    db = MedicalCodingDB()
    
    # Test the connection and table creation
    print("Database initialized successfully")
    
    # Show menu of options
    print("\nDental Analysis Database Tools")
    print("==============================")
    print("1. Export most recent analysis results")
    print("2. Export specific analysis results (enter ID)")
    print("3. View all analysis records")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ")
    
    if choice == "1":
        # Export most recent analysis
        most_recent_id = db.get_most_recent_analysis()
        if most_recent_id:
            db.export_analysis_results(most_recent_id)
    
    elif choice == "2":
        # Export specific analysis
        record_id = input("Enter the analysis record ID to export: ")
        db.export_analysis_results(record_id)
    
    elif choice == "3":
        # View all analysis records
        records = db.get_all_analyses()
        if records:
            print("\nAll Analysis Records:")
            print("=====================")
            for record in records:
                record_id, user_question, processed_data, cdt_result, icd_result, questioner_data, created_at = record
                cdt_size = len(cdt_result) if cdt_result else 0
                icd_size = len(icd_result) if icd_result else 0
                print(f"ID: {record_id}")
                print(f"Created: {created_at}")
                print(f"Question: {user_question[:50]}...")
                print(f"CDT Data Size: {cdt_size} bytes")
                print(f"ICD Data Size: {icd_size} bytes")
                print("-" * 40)
    
    print("Database tool completed")
    db.close_connection()

