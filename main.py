#need two thing to run fast api
# FASTAPI and UVICORN
#UNVICORN is ASGI server to run FASTAPI application, in simple words it is used to serve the application
import os
from fastapi import FastAPI

from supabase import create_client, Client

from dotenv import load_dotenv
load_dotenv() # take environment variables from .env.file

import brains


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

@app.get("/login/{email}")
async def check_email(email: str):
    response = supabase.table('Users').select("*").eq('email', email).execute()

    if len(response.data) == 0:
        try:
            code = brains.create_user_verification(email) #create users in database and give us user auth code
            email_res = brains.send_verification_email(email, code)

            return {"Message": "Verification email sent"}



        except:
            return {"Message": "Error sending verification email"}
    
    else:
        dic = response.data[0]
        if dic["is_verify"] == True:
            return {"Message": "User already verfied"}
        else:
            return {"Message": "User not verified yet"}

@app.get("/verify_email/{code}")
async def verify_email(code: str):
    response = supabase.table("Users").select("*").eq("code", code).execute()
    if len(response.data) == 1:
        try:
                
            supabase.table("Users").update({"is_verify": True}).eq("code", code).execute()
            return {"Message": "Email verified successfully"}
        
        except:
            return {"Message": "Error verifying email"}
        
    else:
        return {"Message": "Invalid verification code"}

