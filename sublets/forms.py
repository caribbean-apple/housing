from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Listing

class UserRegistrationForm(UserCreationForm):
    # Username and password are included by default through UserCreationForm.
    # Can add fields here later if we need more information from registration
    class Meta:
        # This meta info class is used for ModelForms, whose fields are
        # defined based on what's in the corresponding model (user model).
        # It determines which fields from the model to include in the form.
        model = User
        fields = ['username', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    # AuthenticationForm is not a ModelForm, so meta class would
    # have no effect here. It has username and password fields by
    # default. It has built-in security features compared to
    # implementing manually.
    pass

class ListingForm(forms.Form):
    #Form to enter a new listing to the database.
    class Meta:
        # This meta info class is used for ModelForms, whose fields are
        # defined based on what's in the corresponding model (listing model).
        # It determines which fields from the model to include in the form.
        model=Listing
        fields=['description', 'address_line_1', 'city', 'state', 'zip_code', 'rent',
                 'listing_type', 'start_date', 'end_date', 'bathroom_count', 'bedroom_count' ]

    pass