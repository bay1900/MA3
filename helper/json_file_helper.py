import json
import os
from pathlib import Path


from dotenv import load_dotenv
from fastapi import HTTPException


# ENV
load_dotenv()
USER_API_KEY_PATH = os.getenv('USER_API_KEY_PATH')


def create_json ( payload ) -> bool: 
    try:
        with open(USER_API_KEY_PATH, 'w') as file:
                json.dump(payload, file, indent=4)
        # return {"message": "API key stored successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error storing API key: {e}")
    
def write_json(payload):
    print ( 'write_json' )
    USER_API_KEY_PATH = Path( os.getenv('USER_API_KEY_PATH') ) 

    try:
        if USER_API_KEY_PATH.exists():
            with USER_API_KEY_PATH.open("r") as file:
                try:
                    existing_data = json.load(file)
                    if not isinstance(existing_data, list): #Added check to make sure the data is a list.
                        existing_data = [] #If it is not a list, then start with an empty list.
                except json.JSONDecodeError:
                    existing_data = []
        else:
            existing_data = []

        existing_data.append(payload)

        with USER_API_KEY_PATH.open("w") as file:
            json.dump(existing_data, file, indent=4)

        return {"message": "Data appended successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error appending data: {e}")


def read_json(): 
    try:
        with open(USER_API_KEY_PATH, 'r') as file:
             data = json.load(file)
             return data 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading API key: {e}")
 