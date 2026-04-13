#need two thing to run fast api
# FASTAPI and UVICORN
#UNVICORN is ASGI server to run FASTAPI application, in simple words it is used to serve the application
import os
from fastapi import FastAPI

from supabase import create_client, Client

from dotenv import load_dotenv
load_dotenv() # take environment variables from .env.file

import brains

from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Allow all origins (you can specify specific origins if needed)
    allow_methods=["GET", "POST"],  # Allow all HTTP methods
    allow_headers=["*"],
)  


url: str = os.environ.get('SUPABASE_URL')
key: str = os.environ.get('SUPABASE_KEY')

supabase: Client = create_client(url, key) # this is the cursor to interact with the database


@app.get("/")
def root():
    return {
        "Message": "API WORKING",
    }

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

@app.get("/login/{email}/{password}/{username}")
async def check_email(email: str, password: str, username: str):
    response = supabase.table('Users').select("*").eq('email', email).execute();

    if len(response.data) == 0:
         #update the user with password
        try:
            code = brains.create_user_verification(email, password, username) #create users in database and give us user auth code
            email_res = brains.send_verification_email(email, code)


            


            return {"Message": "Verification email sent"}



        except (Exception) as e:
            return {"Message": "Error sending verification email" + str(e)}
    
    else:
        dic = response.data[0]
        if dic["is_verify"] == True:
            return {"Message": "User already verfied"}
        else:
            return {"Message": "User not verified yet"}



#-------------------- LOGIN PROCCES --------------------
#one login api that did three things
#check if user exits
# check if email is verifeid 
# check if password is correct (we will add password later)

@app.get("/user_login/{email}/{password}")
async def user_login(email:str, password: str):
    response = supabase.table("Users").select("*").eq("email",email.lower()).execute()
    data = response.data

    try:

        if len(data) == 0: #chec if user exits 
            return {"Message": "User not found"}
        
        user = data[0]

        if user["is_verify"] == False: #check if email is verified
            return {"Message": "Email not verified"}
        
        if user["password"] != password: #check if password is correct
            return {"Message": "Incorrect password"}
    
    except Exception as e:
        return e

    return {"Message": "Login successful"}


#-------------------- LOGIN PROCCES --------------------

#-------------------- FETCH USER FOR GLOBAL STATE --------------------

@app.get("/fetch_user/{email}")
async def fetch_user(email: str):
    response = supabase.table("Users").select("*").eq("email", email).execute()
    data = response.data
    try:
        user = data[0]
        return {
            "Message": "User data fetched successfully",
            "email": user["email"],
            "admin": user["admin"],
            "listings": user["listings"],
            "id": user["id"]
            }
    
    except Exception as e:
        return {"Message": "Error fetching user data for global state"}


#-------------------- FETCH USER FOR GLOBAL STATE --------------------

@app.get("/fetch_user_again/{id}")
async def fetch_user(id: int):
    response = supabase.table("Users").select("*").eq("id", id).execute()
    data = response.data
    try:
        user = data[0]
        return {
            "Message": "User data fetched successfully",
            "email": user["email"]
            }
    
    except Exception as e:
        return {"Message": "Error fetching user data for global state"}


#-------------------- FETCH global Listings --------------------

@app.get("/fetch_listings/{user_id}")
async def fetch_listings(user_id: int):

    if user_id == 0:
        response = supabase.table("Listings").select("*").execute()

    else:
        response = supabase.table("Listings").select("*").eq("user", user_id).execute()

    
    data = response.data

    try:
        return {
            "Listings": data
        }

    except Exception as e:
        return {"Message": "Error fetching global listings"}


#-------------------- FETCH global Listings--------------------

#-------------------- FETCH one Listings --------------------

@app.get("/fetch_one_listings/{listing_id}")
async def fetch_listings(listing_id: int):


    response = supabase.table("Listings").select("*").eq("id", listing_id).execute()

    
    data = response.data

    try:
        return {
            "Listings": data
        }

    except Exception as e:
        return {"Message": "Error fetching one listings" + str(e)}


#-------------------- FETCH one Listings--------------------



#-------------------- Post A Listings --------------------

@app.get("/post_listing/{user_id}/{title}/{category}/{price}/{description}")
async def post_listing(user_id: int, title: str, category:str, price: str, description: str):
    try:
        supabase.table("Listings").insert({"price": price, "title": title, "category": category, "user": user_id, "desc": description, "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcShyIEH174BuP8HA8owI9rt6vMpr7ugakpYOA&s"}).execute()

        return{
            "Message": "Listing posted successfully",
        }

    except Exception as e:
        return {"Message": "Error posting listing" + str(e)}


#-------------------- Post A Listings --------------------



#-------------------- Create Users --------------------

@app.get("/post_listing/{user_id}/{title}/{category}/{price}/{description}")
async def post_listing(user_id: int, title: str, category:str, price: str, description: str):
    try:
        supabase.table("Listings").insert({"price": price, "title": title, "category": category, "user": user_id, "desc": description, "img": None}).execute()

        return{
            "Message": "Listing posted successfully",
        }

    except Exception as e:
        return {"Message": "Error posting listing" + str(e)}


#-------------------- Create Users --------------------




@app.get("/verify_email/{code}")
async def verify_email(code: str):
    response = supabase.table("Users").select("*").eq("code", code).execute()
    if len(response.data) == 1:
        res = response.data[0]

        if res["is_verify"] == True:
            return {"Message": "Email already verified"}

        try:
                
            supabase.table("Users").update({"is_verify": True}).eq("code", code).execute()
            return {"Message": "Email verified successfully"}
        
        except:
            return {"Message": "Error verifying email"}
        
    else:
        return {"Message": "Invalid verification code"}

