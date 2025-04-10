"""
Simple database check script.
"""
from database import MedicalCodingDB
import sys

def check_database():
    """Check if we can connect to the database and list records."""
    try:
        print("Connecting to database...")
        db = MedicalCodingDB()
        print("Connection successful")
        
        print("\nListing recent records:")
        db.cursor.execute("SELECT id, created_at FROM dental_report ORDER BY created_at DESC LIMIT 5")
        records = db.cursor.fetchall()
        
        if not records:
            print("No records found in database")
        else:
            for record in records:
                print(f"  ID: {record[0]}, Created: {record[1]}")
        
        db.close_connection()
        print("Connection closed")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_database() 