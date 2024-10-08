from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
import datetime
from .models import User, Listing, Message, UserProfile


SUPPORTED_CITIES = [
    ('Boston Area', 'Boston Area'),
    ('New York City', 'New York City'),
    ('Philadelphia', 'Philadelphia'),
]


class UserEmailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']


class MultipleFileInput(forms.ClearableFileInput):
    """
    This class is an ingredient for our MultipleFileField class,
    which allows for multiple file uploads.
    """
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    """
    This is a custom form for inputting multiple photos here.
    It feeds into UserProfileForm and ListingForm, to allow uploads
    of multiple photos for profiles and sublet listings.
    The default form only accepts submission of one file in django 5.0.7,
    so this was our solution.
    This was created with help from a wise user on stackexchange who had
    the same issue we encountered.
    """
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class UserProfileForm(forms.ModelForm):
    user_id = forms.IntegerField(widget=forms.HiddenInput())
    pictures = MultipleFileField(label='Select files', required=False)

    class Meta:
        model = UserProfile
        fields = ['looking_for', 'about_me']
        widgets = {
            'looking_for': forms.Textarea(attrs={'rows': 4, 'cols': 45}),
            'about_me': forms.Textarea(attrs={'rows': 4, 'cols': 45}),
        }

    def process_and_save(self, profile_user=None, commit=True):
        if profile_user is None:
            raise ValueError("Must specify user_id to save a UserProfile.")
        if not self.is_valid():
            raise ValueError("Check if form is valid before saving.")
        profile = super().save(commit=False)
        profile.user = profile_user
        if commit:
            profile.save()
        return profile


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
    # Annoyingly, when passing in data with request.POST, you must
    # specify LoginForm(data=request.POST), because the first argument
    # is not data, unlike other forms.
    pass


class ListingForm(forms.ModelForm):
    # Form to enter a new listing to the database.
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    pictures = MultipleFileField(label='Select files', required=False)

    class Meta:
        # This meta info class is used for ModelForms, whose fields are
        # defined based on what's in the corresponding model (listing model).
        # It determines which fields from the model to include in the form.
        model = Listing
        fields = ['address_line_1', 'city', 'state', 'zip_code', 'rent',
                  'listing_type', 'start_date', 'end_date',
                  'bathroom_count', 'bedroom_count', 'description']

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
            raise forms.ValidationError(
                "Listings must have at least one bedroom.")
        return bedroom_count

    def clean(self):
        # Must call super().clean() in clean(), but not in clean_x.
        # This is enough to run the validation defined in ModelForm.
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError(
                "End date must be later than start date.")
        return cleaned_data


class SearchForm(forms.Form):
    selected_city = forms.ChoiceField(
        choices=SUPPORTED_CITIES,
        widget=forms.Select(attrs={'id': 'city-selector'})
    )


class SendMessageForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(
        attrs={'rows': 4, 'id': 'listing-message-textarea'}))
    recipient_id = forms.IntegerField(widget=forms.HiddenInput())
    listing_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Message
        fields = ['body']

    def process_and_save(self, sender=None, commit=True):
        if sender is None:
            raise ValueError("Must specify sender to save a message.")
        if not self.is_valid():
            raise ValueError("Check if message form is valid before saving.")
        message = super().save(commit=False)
        message.sender = sender
        message.recipient = User.objects.get(
            id=self.cleaned_data['recipient_id'])
        message.listing = Listing.objects.get(
            id=self.cleaned_data['listing_id'])
        if commit:
            message.save()
        return message
