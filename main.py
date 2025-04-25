from supabase import create_client, Client
import os
from dotenv import load_dotenv
from rich import print
import csv

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

def read_csv():
    file_path = 'ingest_data.csv'
    
    with open(file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        
        for row in reader:
            print(row)

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
    print(f"[bold green]{response}[/bold green]")

if __name__ == "__main__":
    main()