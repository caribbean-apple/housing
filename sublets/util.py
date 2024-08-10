from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings


def send_email(email, listing):
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

    try:
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        # Save these in case they are useful to debug after project is over
        # print(response.status_code)
        # print(response.body)
        # print(response.headers)
    except Exception as e:
        print(e.message)