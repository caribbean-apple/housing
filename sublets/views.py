from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, LoginForm

# Create your views here.
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
