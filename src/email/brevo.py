from fastapi.responses import JSONResponse
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from uuid import uuid4
from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env

# === Brevo Setup for sending transactional emails ===
BREVO_EMAIL_API_KEY = os.getenv("BREVO_EMAIL_API_KEY")  # Replace with your actual Brevo API key
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = BREVO_EMAIL_API_KEY
email_api = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))


def sendRegistrationConfirmEmail(user_id: str, username: str, email: str):
    confirmation_url = f"http://localhost:8000/confirm/{user_id}"
    subject = "Please Confirm Your Registration"
    body = f"""
    Hi {username or 'there'},

    Thanks for registering! Please confirm your email address by clicking the link below:

    {confirmation_url}

    If you did not request this, you can ignore the message.
    """

    # Build the email
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": email}],
        subject=subject,
        html_content=f"<html><body><p>{body.replace(chr(10), '<br>')}</p></body></html>",
        sender={"email": "rickhoro@gmail.com", "Rick": "Bookstore Pricing"},
    )

    try:
        email_api.send_transac_email(send_smtp_email)
    except ApiException as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

    return {"message": "Registration successful. Please check your email to confirm."}

sendRegistrationConfirmEmail("myuserid", "Rick Horo", "rickhoro@gmail.com")