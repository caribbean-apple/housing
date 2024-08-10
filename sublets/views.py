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
from .forms import UserEmailForm
from .models import User, Listing, ListingPicture, Message, ProfilePicture
from .util import send_email


@login_required
def saved_listings(request):
    """
    On this page, user can see a list of listings they have saved.

    For GET requests:
    Render all saved listings, each with up to 2 pictures.
    Includes pagination.
    Above the saved listings is a form to submit or change your email,
    which sends an email to the user if the listing is deleted.

    For POST requests:
    User is trying to save their email. Save it if email is valid.
    """
    user = request.user
    email_form = UserEmailForm(request.POST or None)
    message = ""
    if request.method == "POST":
        if email_form.is_valid():
            user.email = request.POST.get('email')
            user.save()
            message = "Email saved!"

    saved_listings = user.saved_listings.all()
    listing_ids = saved_listings.values_list('id', flat=True)

    # Get the first two pictures for each listing.
    queryset = ListingPicture.objects.none()
    for x in listing_ids:
        # Python bitwise OR assignment is used to combine querysets.
        # Django simply defines it / overloads it that way.
        queryset |= ListingPicture.objects.filter(
            listing=Listing.objects.get(pk=x))[:2]

    context = {'saved_listings': saved_listings,
               "listing_pictures": queryset,
               "email_form": email_form,
               "message": message
               }
    return render(request, 'sublets/saved-listings.html', context)


@require_http_methods(["PUT"])
@login_required
def save_or_unsave_listing(request):
    """
    Function to add or remove a listing from a user's saved listings.
    Separated from the listing page view because it is more clear.
    The same function handles both actions.
    Asynconous call from the listing page.
    """
    # Handle the PUT request from JS
    data = json.loads(request.body)
    listing_id = data.get('listingId')
    save_or_unsave = data.get('saveorunsaveAction')
    user = request.user

    # Execute requests against save or unsave.
    # If neither option, return non valid selection.
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


def profile_setup(request):
    """
    This displays the page with a form to make your own profile.

    For POST requests, it saves the user profile that was just created.

    For GET requests or invalid POST requests,
    it simply displays the form (possibly with errors)
    """

    # Get profile data
    profile_form = UserProfileForm(data=request.POST or None,
                                   files=request.FILES or None)

    # If its a POST request, check if user has submitted and info is valid.
    # Then, or if it's a GET request take the user to their profile page.
    # If no profile has been created, there is alternate content.
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


def profile(request, user_id):
    """
    Display the profile page of a user.
    Users who haven't made a profile see a suggestion/button to make one.
    Viewing the profile of another user who has no profile shows a button
    to poke that user to create a profile. That button is just for fun,
    as it was not part of the project specs, and is not yet functional.
    """
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


def listing(request, listing_id):
    """
    For a GET request:
    This displays the details for a sublet listing.

    For a POST request:
    User is trying to send a message to the user who created the listing.
    Save that message.

    For a DELETE request:
    User is trying to delete their own listing.
    Delete it from the database and email anyone who is following it
    """
    form = SendMessageForm(request.POST or None)

    if request.method == "POST":
        # Form to send message to listing owner
        if not request.user.is_authenticated:
            return HttpResponseForbidden(
                "You must be logged in to send a message.")
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
        # Use the sendgrid API to send an email to the user
        # if they have an email saved. It is fast now, but if we
        # scale the app, it would be important to make this
        # email request asynchronous.
        users_who_saved = listing_object.users_who_saved.all()
        users_with_email = users_who_saved.filter(email__isnull=False)
        if users_with_email:
            emails = users_who_saved.values_list('email', flat=True)
            for email in emails:
                send_email(email, listing_object)
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
    if (request.user.is_authenticated
            and listing_object.created_by != request.user):
        context['user_saved_listing'] = request.user.saved_listings.filter(
            id=listing_id).exists()
    return render(request, 'sublets/listing.html', context)


@require_POST
def send_message(request):
    """
    Send a message to the user who created the listing.
    This function is called from the message template.
    It is not called from the listing page, which does not use JS
    to send a message.
    """
    # Get the form data from the request
    form = SendMessageForm(request.POST)

    if form.is_valid():
        # Custom save method that places the form logic in the form.
        form.process_and_save(sender=request.user)
        return redirect('sent_inbox')

    else:
        return HttpResponse("Message Failed to send.")


def index(request):
    """
    This is the homepage where you can search for a listing.
    You can also see a featured listing.
    """
    search_form = SearchForm()
    context = {'search_form': search_form}
    listing_ids = Listing.objects.values_list('id', flat=True)
    if listing_ids:
        featured_listing = Listing.objects.get(id=random.choice(listing_ids))
        context['featured_listing'] = featured_listing
        pictures = ListingPicture.objects.filter(listing=featured_listing)
        context['pictures'] = pictures
    return render(request, 'sublets/index.html', context)


def login_view(request):
    """
    The login page.
    For GET, it displays login form.
    For POST, it handles that form and logs the user in.
    Made by hand.
    """
    login_form = LoginForm(data=request.POST or None)
    if request.method == "POST":
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(
                request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    context = {'login_form': login_form}
    return render(request, 'sublets/login.html', context)


def logout_view(request):
    """
    Logs the user out.
    """
    logout(request)
    return redirect('index')


def register_view(request):
    """
    For GET requests, it displays the registration form.
    For POST, it handles that form and logs the user in.
    """
    registration_form = UserRegistrationForm(request.POST or None)
    if request.method == "POST":
        if registration_form.is_valid():
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


def search_results(request):
    """
    This displays the search results after a user chooses the city.
    It includes additional filters that can be added,
    and the search results are paginated.
    """
    form = SearchForm(request.GET)
    if form.is_valid():
        selected_city = form.cleaned_data["selected_city"]
        relevant_pages = Listing.objects.filter(city=selected_city)
        listing_ids = relevant_pages.values_list('id', flat=True)
        # Variable to hold photos.
        queryset = ListingPicture.objects.none()

        # Go through all the photos and join them.
        # Doing this to create an append type function.
        for x in listing_ids:
            queryset |= ListingPicture.objects.filter(
                listing=Listing.objects.get(pk=x))[:2]

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
            relevant_pages = Listing.objects.filter(
                city=selected_city, start_date__gte=date)
        else:
            relevant_pages = Listing.objects.filter(
                city=selected_city, start_date__gte=date, listing_type=type)

        listing_ids = relevant_pages.values_list('id', flat=True)

        queryset = ListingPicture.objects.none()

        for x in listing_ids:
            queryset |= ListingPicture.objects.filter(
                listing=Listing.objects.get(pk=x))[:2]

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
        return redirect('index')


@login_required
def create(request):
    """
    For GET requests, this view displays a form,
    where the user can create a new sublet listing.

    For POST requests, this view handles submission and
    saves the new listing.
    """
    listing_form = ListingForm(data=request.POST or None,
                               files=request.FILES or None)
    if request.method == "POST":
        if listing_form.is_valid():
            listing_to_add = listing_form.save(commit=False)
            listing_to_add.created_by = request.user
            listing_to_add.save()

            for picture in request.FILES.getlist('pictures'):
                ListingPicture.objects.create(
                    listing=listing_to_add,
                    picture=picture)
            return redirect('listing', listing_to_add.id)
    context = {'listing_form': listing_form}
    return render(request, 'sublets/create.html', context)


@login_required
def messages(request):
    """
    This view is for the message inbox page, which contains JS
    that loads the message reply page.
    """
    user = User.objects.get(username=request.user)
    message_form = SendMessageForm()
    user_messages = Message.objects.filter(recipient=user)
    incoming_messages = user_messages.order_by('sent_at').reverse()

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


def message_fetch(request, message_id):
    """
    This is a supporting view which simply returns messages by ID.
    """

    # Query for requested message
    message_to_return = Message.objects.get(pk=message_id)

    try:
        message_to_return = Message.objects.get(pk=message_id)
        return JsonResponse(message_to_return.serialize())
    except message_to_return.DoesNotExist:
        return JsonResponse({"error": "message not found."}, status=404)


# Sent inbox function, to show all sent messages.
@login_required
def sent_inbox(request):
    """
    On this page, the user can view all messages they already sent.
    """
    user = User.objects.get(username=request.user)
    user_messages = Message.objects.filter(sender=user)
    outgoing_messages = user_messages.order_by('sent_at').reverse()

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
