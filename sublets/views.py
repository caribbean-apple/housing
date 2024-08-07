from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
import random
from .forms import UserRegistrationForm, LoginForm, ListingForm
from .forms import UserProfileForm, SendMessageForm, SearchForm
from .models import User, Listing, ListingPicture, Message, ProfilePicture

@login_required
def saved_listings(request):
    # I'm too lazy to add Pagination for now
    user = request.user
    listings = user.saved_listings.all()
    context = {'saved_listings': listings}
    return render(request, 'sublets/saved-listings.html', context)

# def save_listing(request):
#     # Handle the PUT request from JS
#     if request.method == "PUT":

# Create your views here.
def profile_setup(request):
    profile_form = UserProfileForm(data=request.POST or None,
                                   files=request.FILES or None)
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
    listing_ids = Listing.objects.values_list('id', flat=True)
    if listing_ids:
        featured_listing = Listing.objects.get(id=random.choice(listing_ids))
        context['featured_listing'] = featured_listing
        pictures = ListingPicture.objects.filter(listing=featured_listing)
        context['pictures'] = pictures
    return render(request, 'sublets/index.html', context)


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

        paginated_pages=Paginator(relevant_pages, 2)
        page_obj=paginated_pages.get_page(page)

        #Render Page

        return render(request, "sublets/search_results.html",{
                    "page_obj": page_obj,
                    "selected_city": selected_city
                    })

    else: 
        print("Form is not valid")
        return redirect('index')
    

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
    context = { 'listing_form': listing_form}
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
    