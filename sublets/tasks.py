# Create your tasks here
from __future__ import absolute_import
from django.conf import settings
from celery import shared_task
from .models import User
from django.core.mail import send_mail

@shared_task(bind=True)
def send_email_func(user_pk):
    # Operations
    print("Test to see if we reached the task")
    # user = User.objectsbjects.get(pk=user_pk)
    # email_from=settings.EMAIL_HOST_USER
    # to_email=["scannellstp@gmail.com","sscanne2@alumni.nd.edu"]
    # mail_subject="TEST EMAIL"
    # message = "TEST MESSAGE TO SEE IF THIS WORKS"

    # # send email ...
    # send_mail(
    #         subject= mail_subject,
    #         message=message,
    #         from_email=settings.EMAIL_HOST_USER,
    #         recipient_list=[to_email],
    #         fail_silently=True,
    #     )
    return "Done"