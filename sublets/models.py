from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    saved_listings = models.ManyToManyField("Listing", related_name="users_who_saved")

class Listing(models.Model):
    # These two lists are for the choices parameter of CharField,
    # which takes in iterables containing (actual value, human readable name)
    LISTING_TYPES = [
        ('room_in_apartment', 'Rent a room in a shared apartment'),
        ('entire_apartment', 'Rent an entire apartment to yourself')]
    SUPPORTED_CITIES = [
        ('Boston Area', 'Boston Area'),
        ('New York City', 'New York City'),
        ('Philadelphia', 'Philadelphia')]
    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    description = models.TextField()
    # UPS max = 30char, FedEx max = 35char, USPS max = 46char
    address_line_1 = models.CharField(max_length=35) 
    city = models.CharField(max_length=28, choices=SUPPORTED_CITIES) # 28 according to USPS
    state = models.CharField(max_length=14) # South Carolina is longest
    rent = models.DecimalField(max_digits=7, decimal_places=2)
    listing_type = models.CharField(max_length=20, choices=LISTING_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

def listing_photo_path(instance, filename):
    return f'listing_photos/{instance.listing.id}/{filename}'

class ListingPhoto(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(
        # In a django ImageField, the upload_to option can take a function
        # with two arguments: instance is an instance of the 
        # model (ListingPhoto), and filename is the name of the file 
        # uploaded by the user. A function needs to be passed here
        # instead of a string, because at the time of definition, the
        # listing does not yet exist.
        upload_to=listing_photo_path
    )

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_outbox')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_inbox')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="messages")
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
