from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import UserRegistrationForm, LoginForm
from .models import User, Listing, ListingPicture

# Create your views here.
def listing(request, listing_id):
    listing_object = get_object_or_404(Listing, pk=listing_id)
    pictures = ListingPicture.objects.filter(listing=listing_object)
    has_pictures = pictures.exists()
    context = {
        'listing': listing_object,
        'has_pictures': has_pictures,
        'pictures': pictures}
    return render(request, 'sublets/listing.html', context)

def index(request):
    return render(request, 'sublets/index.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'sublets/login.html', {
                'message': 'Invalid username and/or password.'
            })
    login_form = LoginForm()
    context = {'login_form': login_form}
    return render(request, 'sublets/login.html', context)

def logout_view(request):
    logout(request)
    return redirect('index')

def register_view(request):
    registration_form = UserRegistrationForm(request.POST or None)
    if registration_form.is_valid(): # This returns False if method != POST
        # This returns the newly created User object, because for any
        # ModelForm, .save() returns the newly created model object.
        # Note: This would not work for ordinary forms.Form
        user = registration_form.save() 
        login(request, user)
        return redirect('index')
    context =  {
        'registration_form': registration_form
    }
    return render(request, 'sublets/register.html', context)


def search_results(request):

    return HttpResponse('Successfully reached Search Results Page')
