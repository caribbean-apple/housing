from django.urls import path
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
    # Add your URL patterns here
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    path("search_results/", views.search_results, name="search"),
    path("listing/<int:listing_id>/", views.listing, name="listing"),
    path("create/", views.create, name="create"),
    path("message/", views.messages, name="messages"),
    path("send-message", views.send_message, name="send_message"),
    path("profile/<int:user_id>/", views.profile, name="profile"),
    path("profile-setup", views.profile_setup, name="profile_setup"),
    path("robots.txt",
        TemplateView.as_view(template_name="robots.txt", 
                             content_type="text/plain"), name="robots"),
]
