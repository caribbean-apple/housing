from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings
import json
import traceback

class EmailException(Exception):
    def __init__(self, message, status_code):
        super().__init__(message)
        self.status_code = status_code

def send_email(email, listing, logger):
    try:
        listing_id = listing.id
        subject = "Your saved listing was deleted"
        website_name = "mysublets.com"
        body = ("The following listing was deleted:<br>" +
                website_name + "/listing/" + str(listing_id) + "<br>"
                +f"at address {listing.address_line_1}.")
        
        api_key = settings.SENDGRID_API_KEY

        message = Mail(
        from_email='housingCS33@gmail.com',
        to_emails=email,
        subject=subject,
        html_content=body)

        sg = SendGridAPIClient(api_key)
        # response has properties including 
        # status_code, headers, body
        response = sg.send(message)
        if response.status_code > 399:
            raise EmailException("Failed to send email with status code " +
                                 str(response.status_code), 
                                 status_code=response.status_code)
    except Exception as e:
        error_data = {
            "error_message": (
                "Error while sending email to delete in views/listing()"),
            "recipient": email,
            "subject": subject,
            "body": body,
            "exception": str(e),
            "traceback": traceback.format_exc(),
            "response_status_code": getattr(e, 'status_code', None),
            "exception_detailed": repr(e),
        }
        print("==== Exception while sending email to delete in views/listing() ====")
        print(error_data)
        logger.error(json.dumps(error_data))