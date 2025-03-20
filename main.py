import secrets
import os 
import json

from pydantic import BaseModel
from fastapi import FastAPI, Depends, HTTPException, Header
from typing import Optional
from pathlib import Path
from helper import api_helper, json_file_helper

 
app = FastAPI(
    title="MA3 API",
    description="MA3 - GenAssist",
    version="1.0.0",
    # openapi_tags=[
    #     {
    #         "name": "items",
    #         "description": "Operations with items.",
    #     },
    #     {
    #         "name": "users",
    #         "description": "Operations with users.",
    #     },
    # ],
    # servers=[
    #     {"url": "https://my-api.com", "description": "Production server"},
    #     {"url": "http://localhost:8000", "description": "Local development server"}
    # ]
) 

API_KEYS = {} # In a real application, store API keys securely (e.g., environment variables, a database)
USER_API_KEY_PATH = Path(os.getenv( 'USER_API_KEY_PATH'))

# Open and read the JSON file
with open(USER_API_KEY_PATH, 'r') as file:
     API_KEYS = json.load(file)

 
def generate_api_key( name, st_id):
    """Generates a secure API key."""
    api_key = secrets.token_hex(32)  # Generates a 64-character hex string
 
    payload = { 
                "name": name,
                "stid": st_id,
                "key" : api_key
           }
     
    api_key_handler ( payload )
    
    return api_key
 
def api_key_handler (payload) -> bool:
    
    # Check if the file exists
    if os.path.exists(USER_API_KEY_PATH):
        json_file_helper.write_json ( payload )
    else:
        json_file_helper.create_json ( payload )
        
    return True

def get_api_key(api_key: Optional[str] = Header(None)) -> str:
    """Dependency to validate the API key."""
    if api_key is None:
        raise HTTPException(status_code=400, detail="API Key missing")
    
    """CHECK IF API KEY IS EXIST""" 
    exit_api_key = api_helper.check_exist_api_key ( api_key )
    if not exit_api_key:
        raise HTTPException(status_code=401, detail="Invalid API Key")
 
    return api_key

@app.post("/generate_key")
async def generate_key_endpoint(payload: dict):
    
    ########################
    ##### POST PAYLAOD #####
    ########################
    name  = payload.get( "name", "")
    st_id = payload.get( "st_id", "")
        
    # """Endpoint to generate a new API key.""" 
    gen_key = generate_api_key(name, st_id)
    
    ##############################
    ###### RESPONSE PAYLAOD ######
    ##############################
    response = { 
                "api_key": gen_key, 
                "name": name,
                "st_id": st_id
                
               }
    return response

@app.get("/data")  #endpoint protected by API key
async def get_data(api_key: str = Depends(get_api_key)):
    
    name = api_helper.get_name_by_api_key (API_KEYS, api_key )
    
    payload = { 
               "name": name,
               "msg" : "Suceessfully access data"
            #    "api" : api_key
              }

    return payload


# Example payload model
class chat_payload(BaseModel):
    chat: str
    
    
@app.post("/chat")  #endpoint protected by API key
async def get_chat( 
                    payload: chat_payload,
                    api_key: str = Depends(get_api_key)
                    
                  ):
     print( "chat endpoint ... ",  api_key )
     print( "payload ... ",  payload.chat )


     return payload


