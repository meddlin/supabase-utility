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

    for row in data_list:
        response = supabase.table("places").insert({ 
            'name': row[0], 
            'location': '', 
            'city': row[1],
            'state': row[2],
            'google_maps_link': row[3],
            'notes': row[4],
            'list': row[5]
        }).execute()
        # Check the response
        print(f"[bold green]{response}[/bold green]")

    # response = supabase.table("places").insert(data).execute()

def select_table(table: str):
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    response = supabase.table("places").select().execute()
    print(response)

def empty_table(table: str):
    table_name = "places"
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    try:
        data, error = supabase.table(table_name).delete().neq("id", "").execute()
        if error:
            print(f"Error deleting rows: {error}")
        else:
            print(f"All rows deleted successfully from table '{table_name}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description="Python Supabase Loader Utility")
    parser.add_argument("-s", "--select", type = str, help = "Basic select on a table")
    parser.add_argument("-d", "--delete", type = str, help = "Delete ALL rows from a table")
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
    
    if args.select:
        select_table('places')
    
    if args.delete:
        empty_table('places')

if __name__ == "__main__":
    main()