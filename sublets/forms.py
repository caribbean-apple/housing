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

class ListingForm(forms.ModelForm):
    #Form to enter a new listing to the database.
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        # This meta info class is used for ModelForms, whose fields are
        # defined based on what's in the corresponding model (listing model).
        # It determines which fields from the model to include in the form.
        model = Listing
        fields=['address_line_1', 'city', 'state', 'zip_code', 'rent',
                 'listing_type', 'start_date', 'end_date', 'bathroom_count', 'bedroom_count', 'description']

    def clean_start_date(self):
        start_date = self.cleaned_data['start_date']
        # breakpoint()
        if start_date and start_date < datetime.date.today():
            raise forms.ValidationError("Start date cannot be in the past.")
        return start_date
        
    def clean_end_date(self):
        end_date = self.cleaned_data['end_date']
        if end_date and end_date < datetime.date.today():
            raise forms.ValidationError("End date cannot be in the past.")
        return end_date
        
    def clean_bedroom_count(self):
        bedroom_count = self.cleaned_data['bedroom_count']
        if bedroom_count < 1:
            raise forms.ValidationError("Listings must have at least one bedroom.")
        return bedroom_count
    
    def clean(self):
        print("CLEANING")
        # Must call super().clean() in clean(), but not in clean_x.
        # This is enough to run all validation defined in ModelForm.
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError("End date must be later than start date.")
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
