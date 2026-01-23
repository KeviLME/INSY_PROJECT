import secrets
from supabase import create_client, Client
import os
import dotenv

import resend

dotenv.load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
resend.api_key = os.environ.get("RESEND_KEY")
supabase: Client = create_client(url, key)


def send_verification_email(email: str, code: str):
    link = f"https://insy-project.onrender.com/verify_email/{code}"

    params = {
            "from": "onboarding@resend.dev", # Resend gives you this test email automatically
            "to": [email],
            "subject": "Verify your account",
            "html": f"<p>Click this link to verify: <a href='{link}'>Verify Me</a></p>"
        }


    email = resend.Emails.send(params)
    return email


def create_user_verification(email: str):
    try:
        code = secrets.token_urlsafe(16) #returns a random url safe string

        data = {
            "email": email,
            "code": code,
            "is_verify": False
            }

        response = supabase.table("Users").insert(data).execute()
        
        if len(response.data) == 0:
            return {"Message": "Error creating user"}
        
        return code
    
    except:
        return {"Message": "Error creating user"}


