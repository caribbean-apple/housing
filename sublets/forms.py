from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Listing
import datetime

SUPPORTED_CITIES = ['Boston Area', 'New York City', 'Philadelphia']

SUPPORTED_CITIES = {'Boston Area': 'Boston Area',
        'New York City': 'New York City',
        'Philadelphia': 'Philadelphia'
        }
    

class UserRegistrationForm(UserCreationForm):
    # Username and password are included by default through UserCreationForm.
    # Can add fields here later if we need more information from registration
    class Meta:
        # This meta info class is used for ModelForms, whose fields are
        # defined based on what's in the corresponding model (user model).
        # It determines which fields from the model to include in the form.
        # Generally a ModelForm is used when you want to create or edit lines
        # in a single existing database table.
        model = User
        fields = ['username', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    # AuthenticationForm is not a ModelForm, so meta class would
    # have no effect here. It has username and password fields by
    # default. It has built-in security features compared to
    # implementing manually.
    pass

class ListingForm(forms.ModelForm):
    #Form to enter a new listing to the database.
    class Meta:
        # This meta info class is used for ModelForms, whose fields are
        # defined based on what's in the corresponding model (listing model).
        # It determines which fields from the model to include in the form.
        model = Listing
        fields=['address_line_1', 'city', 'state', 'zip_code', 'rent',
                 'listing_type', 'start_date', 'end_date', 'bathroom_count', 'bedroom_count', 'description']

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        bedroom_count = cleaned_data.get('bedroom_count')
        if start_date and start_date < datetime.date.today():
            raise forms.ValidationError("Start date cannot be in the past.")
        if end_date and end_date < datetime.date.today():
            raise forms.ValidationError("End date cannot be in the past.")
        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("End date must be later than start date.")
        if bedroom_count < 1:
            raise forms.ValidationError("Listings must have at least one bedroom.")
        return cleaned_data

class SearchForm(forms.Form):

    Selected_City = forms.MultipleChoiceField(
        choices=SUPPORTED_CITIES,
    )
    
