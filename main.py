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

def read_csv(file_name: str, has_header: bool):
    file_contents = []

    if '.csv' in file_name:
        if has_header:
            with open(file_name, mode='r', newline='') as file:
                reader = csv.reader(file)
                headers = next(reader, None)
                for row in reader:
                    file_contents.append(row)
            # with open(file_name, mode = 'r', newline = '') as file:
            #     reader = csv.DictReader(file)
            #     for row in reader:
            #         file_contents.append(row)
        else:
            with open(file_name, mode='r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    file_contents.append(row)
    else:
        print('Error: File type must be .csv')
        sys.exit(1)

    return file_contents

def ingest_data(data_list: list):
    # Initialize client
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    # Insert data into the "users" table
    # data = {
    #     "name": "the good place",
    #     "location": "",
    #     "google_maps_link": ""
    # }

    for row in data_list:
        response = supabase.table("places").insert({ 
            'name': row[0], 
            'location': '', 
            'google_maps_link': row[2],
            'list': row[4]
        }).execute()
        # Check the response
        print(f"[bold green]{response}[/bold green]")

    # response = supabase.table("places").insert(data).execute()

def main():
    parser = argparse.ArgumentParser(description="Python Supabase Loader Utility")
    parser.add_argument("-f", "--file", type=str, help = "File to import. MUST BE CSV.")
    parser.add_argument("--header", action = argparse.BooleanOptionalAction, help = "has header")
    args = parser.parse_args()
    
    if args.header and args.file:
        file_name = args.file
        data = read_csv(file_name, args.header)
        ingest_data(data)
        sys.exit(0)

    if args.file:
        file_name = args.file
        data = read_csv(file_name)
        print(data)
        sys.exit(0)

if __name__ == "__main__":
    main()