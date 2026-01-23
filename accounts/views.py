from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from .forms import CustomUserCreationForm
from .models import User

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = User.Role.MEMBER 
            user.save()
            auth_login(request, user)
            messages.success(request, f"Welcome to the Samaj, {user.username}!")
            return redirect('home')
        else:
            messages.error(request, "Registration failed.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    
    def form_valid(self, form):
        messages.success(self.request, "Login successful.")
        return super().form_valid(form)

# Logout is handled by built-in LogoutView or simple function
