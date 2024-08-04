from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.urls import reverse
from .forms import UserRegistrationForm, LoginForm, ListingForm, SearchForm, SendMessageForm
from .models import User, Listing, ListingPicture, Message

# Create your views here.
def listing(request, listing_id):
    form = SendMessageForm(request.POST or None)
    if request.user.is_authenticated and request.method == "POST":
        if form.is_valid():
            # Handle form submission, then refresh page
            form.process_and_save(sender=request.user)
            return redirect('listing', listing_id=listing_id)
    listing_object = get_object_or_404(Listing, pk=listing_id)
    pictures = ListingPicture.objects.filter(listing=listing_object)
    context = {
        'listing': listing_object,
        'pictures': pictures,
        'send_message_form': form}
    return render(request, 'sublets/listing.html', context)

@require_POST
def send_message(request):
    # Get the form data from the request
    form = SendMessageForm(request.POST)
    # need sender, recipient, listing, body
    if form.is_valid():
        form.process_and_save(sender=request.user)
        return redirect(f'listing/{listing.id}')

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

def search_results(request):
    form = SearchForm(request.GET)
    if form.is_valid():
        selected_city=form.cleaned_data["selected_city"]
        print("selected city", selected_city)
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
        print("Form is not valid")
        return redirect('index')
    

@login_required
def create(request):

    listing_form=ListingForm(request.POST or None)
    if request.method == "POST":
        listing_form = ListingForm(request.POST)
        if listing_form.is_valid():
            listing_to_add = listing_form.save(commit=False)
            listing_to_add.created_by = request.user
            listing_to_add.save()
            return redirect('listing', listing_to_add.id)

    context = { 'listing_form': listing_form }
    return render(request, 'sublets/create.html', context)


@login_required
def messages(request):

    user=User.objects.get(username=request.user)

    outgoing_messages=Message.objects.filter(sender=user)
    incoming_messages=Message.objects.filter(recipient=user)

    # Intialize page for pagination
    if request.GET.get('page'):
        page=request.GET.get('page')
    else:
        page=1

    incoming_paginated_pages=Paginator(incoming_messages, 10)
    outgoing_paginated_pages=Paginator(outgoing_messages, 10)
    
    page_obj_in=incoming_paginated_pages.get_page(page)
    page_obj_out=outgoing_paginated_pages.get_page(page)

    print(outgoing_messages)
    print(incoming_messages)



    return render(request, "sublets/messages.html", {
        "page_obj_in": page_obj_in,
        "page_obj_out": page_obj_out

    })
    