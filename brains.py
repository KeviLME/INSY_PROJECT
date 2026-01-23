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


def get_verification_email(link_url):
    # You can paste huge, beautiful HTML strings here
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            .button {{
                background-color: #074270;
                color: #ffffff;
                padding: 10px 20px;
                text-decoration: none !important;
                border-radius: 5px;
            }}

            .button a{{
                color: #ffffff !important;
                text-decoration: none;
            }}
        </style>
    </head>
    <body>
        <h1>Welcome to MavMarket — we’re excited to have you join our community! 🎉</h1>
        <p>Before you start exploring, please take a moment to verify your account. This helps keep MavMarket safe and ensures full access to all our features.</p>
        <br>
        <a href="{link_url}" class="button">Verify My Account</a>
        <br><br>
        <p>THANK YOU FOR JOINING US!</p>
        <br><br>

    </body>
    </html>
    """



def send_verification_email(email: str, code: str):
    link = f"https://insy-project.onrender.com/verify_email/{code}"
    mail = get_verification_email(link)

    params = {
            "from": "onboarding@resend.dev", # Resend gives you this test email automatically
            "to": [email],
            "subject": "MAV MARKET - Verify your account",
            "html": mail
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


