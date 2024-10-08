from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    saved_listings = models.ManyToManyField("Listing",
                                            related_name="users_who_saved")
    email = models.EmailField(max_length=35, null=True)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name="profile")
    looking_for = models.TextField(blank=True)
    about_me = models.TextField(blank=True)

    def __str__(self):
        about_me_segment = (self.about_me[:30] + '...'
                            if len(self.about_me) > 30
                            else self.about_me)
        return f"Profile: {self.user.username}. {about_me_segment}"


class ProfilePicture(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="profile_pictures")
    picture = models.ImageField(upload_to='profile_pictures/')


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

    # Using this to limit bathroom options.  This can be expanded to include
    # more options. It was chosen instead of allowing user a free input,
    # which could be confusing.
    BATHROOM_OPTIONS = [
        ('1', 'One'),
        ('1.5', 'One and a half'),
        ('2',  'Two'),
        ('2.5', 'Two and a half'),
        ('3', 'Three'),
        ('3.5', 'Three and a half'),
        ('4', 'Four')
    ]

    created_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_name='listings')
    description = models.TextField()
    # UPS max = 30char, FedEx max = 35char, USPS max = 46char
    address_line_1 = models.CharField(max_length=35)
    # 28 according to USPS
    city = models.CharField(max_length=28, choices=SUPPORTED_CITIES)
    state = models.CharField(max_length=14)  # South Carolina is longest
    zip_code = models.CharField(max_length=5)
    rent = models.DecimalField(max_digits=7, decimal_places=2)
    listing_type = models.CharField(max_length=20, choices=LISTING_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    bedroom_count = models.IntegerField()
    bathroom_count = models.CharField(max_length=14,
                                      choices=BATHROOM_OPTIONS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f'{self.city} - listing by {self.created_by} at {self.zip_code}')


def listing_picture_path(instance, filename):
    return f'listing_pictures/{instance.listing.id}/{filename}'


class ListingPicture(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE,
                                related_name='pictures')
    picture = models.ImageField(
        # In a django ImageField, the upload_to option can take a function
        # with two arguments: instance is an instance of the
        # model (ListingPicture), and filename is the name of the file
        # uploaded by the user. A function needs to be passed here
        # instead of a string, because at the time of definition, the
        # listing does not yet exist.
        upload_to=listing_picture_path
    )


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='message_outbox')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name='message_inbox')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE,
                                related_name="messages")
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        formatted_time = timezone.localtime(
            self.sent_at).strftime("%m.%d.%Y %H:%M")
        message_segment = (self.body[:40] + '...'
                           if len(self.body) > 40
                           else self.body)
        return (f'From {self.sender} to '
                + f'{self.recipient} ({formatted_time}): {message_segment}')

    def serialize(self):
        return {
            "id": self.id,
            "sender": self.sender.username,
            "sender_id": self.sender.id,
            "recipient": [self.recipient.username],
            "body": self.body,
            "listing": self.listing.address_line_1,
            "listing_id": self.listing.id,
            "timestamp": self.sent_at.strftime("%b %d %Y, %I:%M %p")
        }
