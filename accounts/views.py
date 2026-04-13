from django.shortcuts import render

# Create your views here.

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
    
    # new class SignUpView that extends CreateView, which is a generic view provided by Django for creating new objects. We specify that we want to use the built-in UserCreationForm as our form class, and we set the success_url to reverse_lazy("login"), which means that after a successful registration, the user will be redirected to the login page. Finally, we specify the template_name for rendering the signup form.
    # reverse_lazy is used here to avoid circular import issues, as it allows us to reference the URL pattern by name without needing to import the URL configuration at the top of the file.
    
