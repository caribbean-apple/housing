from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden, JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_http_methods
import random
import json
from .forms import UserRegistrationForm, LoginForm, ListingForm
from .forms import UserProfileForm, SendMessageForm, SearchForm
from .models import User, Listing, ListingPicture, Message, ProfilePicture
from django.core.mail import send_mail

# Function for a user to see their saved lisitings


@login_required
def saved_listings(request):

    user = request.user

    if request.method == "POST":
        
        user.email=request.POST.get('email')
        message="User Email Updated"
    else:
        message=""

    relevant_pages = user.saved_listings.all()

    listing_ids = relevant_pages.values_list('id', flat=True)

    queryset = ListingPicture.objects.none()

    for x in listing_ids:
        queryset |= ListingPicture.objects.filter(listing=Listing.objects.get(pk=x))[:2]

    # Intialize page for pagination
    if request.GET.get('page'):
        page = request.GET.get('page')
    else:
        page = 1

    paginated_pages = Paginator(relevant_pages, 2)
    page_obj = paginated_pages.get_page(page)


    context = {'saved_listings': page_obj,
               "listing_pictures": queryset,
               "message": message
               }
    return render(request, 'sublets/saved-listings.html', context)

# Function to save or unsave a listing.  Asynconous call from the listing page.


@require_http_methods(["PUT"])
@login_required
def save_or_unsave_listing(request):
    # Handle the PUT request from JS
    data = json.loads(request.body)
    listing_id = data.get('listingId')
    listing = Listing.objects.get(pk=listing_id)
    save_or_unsave = data.get('saveorunsaveAction')
    user = request.user

    email_from=settings.EMAIL_HOST_USER
    recipient_list=["scannellstp@gmail.com","sscanne2@alumni.nd.edu"]

    body="You saved the listing"+ str(listing.address_line_1)
    send_mail(
        "You saved a listing",
        body,
        recipient_list,
        email_from,
        fail_silently=False,
    )

    # Execute requests against save or unsave.  If neither option, return non valid selection.
    if save_or_unsave == "save":
        user.saved_listings.add(listing_id)

        return JsonResponse(
            {'message': 'Listing saved successfully.'},
            status=200)
    elif save_or_unsave == "unsave":
        user.saved_listings.remove(listing_id)
        return JsonResponse(
            {'message': 'Listing unsaved successfully.'},
            status=200)
    else:
        return JsonResponse(
            {'error': f'Cannot perform action {save_or_unsave}'},
            status=400)

 
# Create your views here.


def profile_setup(request):

    # Get profile data
    profile_form = UserProfileForm(data=request.POST or None,
                                   files=request.FILES or None)
    
    # If its a post form, so a user has submitted and the info is valid, take the user to their profile.  
    # Otherwise (if it is a get or the form is invalid) take the user back to their own page.
    if request.method == "POST":
        if profile_form.is_valid():
            user_id = profile_form.cleaned_data['user_id']
            profile_user = get_object_or_404(User, id=user_id)
            profile_form.process_and_save(profile_user=profile_user)

            for picture in request.FILES.getlist('pictures'):
                ProfilePicture.objects.create(
                    user=profile_user,
                    picture=picture
                )
            return redirect('profile', user_id=user_id)
    context = {'profile_form': profile_form}
    return render(request, 'sublets/profile-setup.html', context)

# Display profile page function


def profile(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)
    has_profile = hasattr(profile_user, 'profile')

    context = {
        'profile_user': profile_user,
        'has_profile': has_profile
    }
    if has_profile:
        context['profile'] = profile_user.profile
        context['profile_pictures'] = profile_user.profile_pictures.all()
    return render(request, 'sublets/profile.html', context)

# Display listing function.


def listing(request, listing_id):
    form = SendMessageForm(request.POST or None)

    if request.method == "POST":
        # Form to send message to listing owner
        if not request.user.is_authenticated:
            return HttpResponseForbidden("You must be logged in to send a message.")
        if form.is_valid():
            # Handle form submission, then refresh page
            form.process_and_save(sender=request.user)
            return redirect('listing', listing_id=listing_id)
        
    elif request.method == "DELETE":
        # Form for user to delete own listing
        listing_object = get_object_or_404(Listing, pk=listing_id)
        if not request.user.is_authenticated:
            return JsonResponse(
                {'error': 'You must be logged in to delete a listing.'},
                status=403)
        if listing_object.created_by != request.user:
            return JsonResponse(
                {'error': "You are not allowed to \
                 delete another user's listing."}, 
                status=403)
        listing_object.delete()
        return JsonResponse(
            {'message': 'Successfully deleted listing.'},
            status=200)
    
    listing_object = get_object_or_404(Listing, pk=listing_id)
    pictures = ListingPicture.objects.filter(listing=listing_object)
    
    context = {
        'listing': listing_object,
        'pictures': pictures,
        'send_message_form': form}
    if request.user.is_authenticated and listing_object.created_by != request.user:
        context['user_saved_listing'] = request.user.saved_listings.filter(
            id=listing_id).exists()
    return render(request, 'sublets/listing.html', context)

# Send message function, called from the listing page and the messages page.


@require_POST
def send_message(request):
    # Get the form data from the request
    form = SendMessageForm(request.POST)

    # need sender, recipient, listing, body
    if form.is_valid():
        form.process_and_save(sender=request.user)
        return redirect('sent_inbox')
    elif request.POST.get('recipient_id'):
        new_message = SendMessageForm(recipient_id=request.POST.get('recipient_id'),
                                      listing_id=request.POST.get('listing_id'),
                                      body=request.POST.get('body')
                                      )
        new_message.process_and_save(sender=request.user)
        return redirect('sent_inbox')
    else:
        print("Something wrong with form")
        print(request)
        return HttpResponse("Message Failed to send.")

# The index page, which shows the initial city selection options.


def index(request):
    search_form = SearchForm()
    context = {'search_form': search_form}
    listing_ids = Listing.objects.values_list('id', flat=True)
    if listing_ids:
        featured_listing = Listing.objects.get(id=random.choice(listing_ids))
        context['featured_listing'] = featured_listing
        pictures = ListingPicture.objects.filter(listing=featured_listing)
        context['pictures'] = pictures
    return render(request, 'sublets/index.html', context)

# Login view, default from django classes.


def login_view(request):
    login_form = LoginForm(data=request.POST or None)
    if request.method == "POST":
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    context = {'login_form': login_form}
    return render(request, 'sublets/login.html', context)

# Logout view, default from django classes.


def logout_view(request):
    logout(request)
    return redirect('index')

# Register view, default from django classes.


def register_view(request):
    registration_form = UserRegistrationForm(request.POST or None)
    if registration_form.is_valid():  # This returns False if method != POST
        # This returns the newly created User object, because for any
        # ModelForm, .save() returns the newly created model object.
        # Note: This would not work for ordinary forms.Form
        user = registration_form.save() 
        login(request, user)
        return redirect('index')
    context = {
        'registration_form': registration_form
    }
    return render(request, 'sublets/register.html', context)

# Search results view.  If the results is from the search page, load all options.  Otherwise respond to filters


def search_results(request):
    form = SearchForm(request.GET)
    if form.is_valid():
        selected_city = form.cleaned_data["selected_city"]
        relevant_pages = Listing.objects.filter(city=selected_city)
        listing_ids = relevant_pages.values_list('id', flat=True)
        # Variable to hold photos.
        queryset = ListingPicture.objects.none()

        # Go through all the photos and join them.  Doing this to create an append type function.
        for x in listing_ids:
            queryset |= ListingPicture.objects.filter(listing=Listing.objects.get(pk=x))[:2]

        # Intialize page for pagination
        if request.GET.get('page'):
            page = request.GET.get('page')
        else:
            page = 1

        paginated_pages = Paginator(relevant_pages, 2)
        page_obj = paginated_pages.get_page(page)

        # Render Page
        return render(request, "sublets/search_results.html", {
            "page_obj": page_obj,
            "selected_city": selected_city,
            "listing_pictures": queryset
        })

    if request.method == "POST":
        selected_city = request.POST.get('selected_city')
        type = request.POST.get('types')
        date = request.POST.get('trip-start')    

        if type == "both":
            relevant_pages = Listing.objects.filter(city=selected_city, start_date__gte=date)
        else:
            relevant_pages = Listing.objects.filter(
                city=selected_city, start_date__gte=date, listing_type=type)

        listing_ids = relevant_pages.values_list('id', flat=True)

        queryset = ListingPicture.objects.none()

        for x in listing_ids:
            queryset |= ListingPicture.objects.filter(listing=Listing.objects.get(pk=x))[:2]

        # Intialize page for pagination
        if request.GET.get('page'):
            page = request.GET.get('page')
        else:
            page = 1

        paginated_pages = Paginator(relevant_pages, 2)
        page_obj = paginated_pages.get_page(page)

        # Render Page
        return render(request, "sublets/search_results.html", {
            "page_obj": page_obj,
            "selected_city": selected_city,
            "listing_pictures": queryset
        })

    else: 
        print("Form is not valid")
        return redirect('index')
    

# Create listing function


@login_required
def create(request):
    listing_form = ListingForm(data=request.POST or None, 
                               files=request.FILES or None)
    if request.method == "POST":
        if listing_form.is_valid():
            listing_to_add = listing_form.save(commit=False)
            listing_to_add.created_by = request.user
            listing_to_add.save()

            for picture in request.FILES.getlist('pictures'):
                ListingPicture.objects.create(listing=listing_to_add, picture=picture)
            return redirect('listing', listing_to_add.id)
    context = {'listing_form': listing_form}
    return render(request, 'sublets/create.html', context)

# Show messages function


@login_required
def messages(request):

    user = User.objects.get(username=request.user)
    message_form = SendMessageForm()

    incoming_messages = Message.objects.filter(recipient=user).order_by('sent_at').reverse()

    # Intialize page for pagination
    if request.GET.get('page'):
        page = request.GET.get('page')
    else:
        page = 1

    incoming_paginated_pages = Paginator(incoming_messages, 10)
    
    page_obj_in = incoming_paginated_pages.get_page(page)

    return render(request, "sublets/messages.html", {
        "page_obj_in": page_obj_in,
        "send_message_form": message_form

    })
    
# Get message from API to support Javascript functions.


def message_fetch(request, message_id):

    # Query for requested message

    print(message_id)
    message_to_return = Message.objects.get(pk=message_id)

    print(message_to_return)
    try:
        message_to_return = Message.objects.get(pk=message_id)
        
        return JsonResponse(message_to_return.serialize())
    except message_to_return.DoesNotExist:
        return JsonResponse({"error": "message not found."}, status=404)


# Sent inbox function, to show all sent messages.
@login_required
def sent_inbox(request):
    user = User.objects.get(username=request.user)
    outgoing_messages = Message.objects.filter(sender=user).order_by('sent_at').reverse()

    # Intialize page for pagination
    if request.GET.get('page'):
        page = request.GET.get('page')
    else:
        page = 1

    outgoing_paginated_pages = Paginator(outgoing_messages, 10)

    page_obj_out = outgoing_paginated_pages.get_page(page)

    return render(request, "sublets/sent-inbox.html", {
        "page_obj_out": page_obj_out

    })    