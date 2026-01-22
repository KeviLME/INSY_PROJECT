#need two thing to run fast api
# FASTAPI and UVICORN
#UNVICORN is ASGI server to run FASTAPI application, in simple words it is used to serve the application
import os
from fastapi import FastAPI

from supabase import create_client, Client

from dotenv import load_dotenv
load_dotenv() # take environment variables from .env.file


app = FastAPI()

url: str = os.environ.get('SUPABASE_URL')
key: str = os.environ.get('SUPABASE_KEY')

supabase: Client = create_client(url, key) # this is the cursor to interact with the database


@app.get("/")
def root():
    response = supabase.table('Test').select("*").execute()
    return response.data

@app.get("/adding/{num1}/{num2}")
async def add(num1: int, num2: int):
    return {
        'results': num1 + num2
    }


@app.get("/name/{your_name}")
async def name(your_name: str):
    return {
        'message': f"hello {your_name}"
    }