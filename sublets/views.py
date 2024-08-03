from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required #, require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator
from .forms import UserRegistrationForm, LoginForm, ListingForm, SearchForm, SendMessageForm
from .models import User, Listing, ListingPicture

# Create your views here.
def listing(request, listing_id):
    listing_object = get_object_or_404(Listing, pk=listing_id)
    pictures = ListingPicture.objects.filter(listing=listing_object)
    send_message_form = SendMessageForm()
    context = {
        'listing': listing_object,
        'pictures': pictures,
        'send_message_form': send_message_form}
    return render(request, 'sublets/listing.html', context)

# @require_POST
def send_message(request):
    # Get the form data from the request
    form = SendMessageForm(request.POST)
    # need sender, recipient, listing, body
    if form.is_valid():
        form.save()

def index(request):
    search_form = SearchForm()
    context = {'search_form': search_form}
    return render(request, 'sublets/index.html', context)

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

@login_required(login_url='login')
def search_results(request):

    if request.method == "POST":

        selected_city=request.POST["Selected_City"]

        print(selected_city)

        relevant_pages=Listing.objects.filter(city=selected_city)

        # Intialize page for pagination
        if request.GET.get('page'):
            page=request.GET.get('page')
        else:
            page=1

        paginated_pages=Paginator(relevant_pages, 10)
        page_obj=paginated_pages.get_page(page)

        #Render Page

        return render(request, "sublets/search_results.html",{
                    "page_obj": page_obj
                    })

    else: 

        return redirect('index')
    

@login_required(login_url='login')
def create(request):

    listing_form=ListingForm(request.POST or None)

    if request.method == "POST":
        if listing_form.is_valid():

            listing_to_add = listing_form.save() 
            listing(request, listing_to_add.id)


    else:
        context = {
            'listing_form': listing_form
            }
    
    return render(request, 'sublets/create.html', context)

    