from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Listing, Message
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

class ListingForm(forms.Form):
    #Form to enter a new listing to the database.
    class Meta:
        # This meta info class is used for ModelForms, whose fields are
        # defined based on what's in the corresponding model (listing model).
        # It determines which fields from the model to include in the form.
        model=Listing
        fields=['description', 'address_line_1', 'city', 'state', 'zip_code', 'rent',
                 'listing_type', 'start_date', 'end_date', 'bathroom_count', 'bedroom_count']

    def clean_start_date(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        if start_date and start_date < datetime.date.today():
            raise forms.ValidationError("Start date cannot be in the past.")
        
    def clean_end_date(self):
        cleaned_data = super().clean()
        end_date = cleaned_data.get('end_date')
        if end_date and end_date < datetime.date.today():
            raise forms.ValidationError("End date cannot be in the past.")
        if end_date and end_date < cleaned_data.get('start_date'):
            raise forms.ValidationError("End date must be later than start date.")
        
    def clean_bedroom_count(self):
        cleaned_data = super().clean()
        bedroom_count = cleaned_data.get('bedroom_count')
        if bedroom_count < 1:
            raise forms.ValidationError("Listings must have at least one bedroom.")
        return cleaned_data

class SearchForm(forms.Form):

    Selected_City = forms.MultipleChoiceField(
        choices=SUPPORTED_CITIES,
    )
    
class SendMessageForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))
    class Meta:
        model = Message
        fields = ['body']
