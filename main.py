from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

def main():
    # Initialize client
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    # Insert data into the "users" table
    data = {
        "name": "the good place",
        "location": "",
        "google_maps_link": ""
    }

    response = supabase.table("places").insert(data).execute()

    # Check the response
    print(response)

if __name__ == "__main__":
    main()