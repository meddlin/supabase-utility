import os
import sys
import csv
import argparse
from dotenv import load_dotenv
from rich import print
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

def read_csv(file_name: str):
    if '.csv' in file_name:
        with open(file_name, mode='r', newline='') as file:
            reader = csv.reader(file)
            
            for row in reader:
                print(row)
    
    print('Error: File type must be .csv')
    sys.exit(1)

def insert_row():
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

def main():
    parser = argparse.ArgumentParser(description="Python Supabase Loader Utility")
    parser.add_argument("-f", "--file", type=str, help = "File to import. MUST BE CSV.")
    args = parser.parse_args()
    
    if args.file:
        file_name = args.file
        read_csv(file_name)

if __name__ == "__main__":
    main()