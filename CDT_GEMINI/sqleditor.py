import os
import uuid
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_ANON_KEY")
supabase: Client = create_client(url, key)

print(supabase)


class SupabaseService:
    def __init__(self, table: str):
        self.url = os.environ.get("SUPABASE_URL")
        self.key = os.environ.get("SUPABASE_ANON_KEY")
        self.client: Client = create_client(self.url, self.key)

    def create_analysis_record(self, data: dict):
        """Create a new record"""
        # Add UUID for id field
        data['id'] = str(uuid.uuid4())
        response = self.client.table("dental_report").insert(data).execute()
        return response.data

    def read_all(self):
        """Read all records"""
        response = self.client.table(self.table).select("*").execute()
        return response.data

    def read_by_id(self, record_id: int):
        """Read a single record by ID"""
        response = self.client.table(self.table).select("*").eq("id", record_id).single().execute()
        return response.data

    def update(self, record_id: int, updated_data: dict):
        """Update a record by ID"""
        response = self.client.table(self.table).update(updated_data).eq("id", record_id).execute()
        return response.data

    def delete(self, record_id: int):
        """Delete a record by ID"""
        response = self.client.table(self.table).delete().eq("id", record_id).execute()
        return response.data

    def update_processed_scenario(self, record_id: str, processed_data: str):
        """Update processed data for a record"""
        response = self.client.table("dental_report").update({
            "processed_clean_data": processed_data
        }).eq("id", record_id).execute()
        return response.data
