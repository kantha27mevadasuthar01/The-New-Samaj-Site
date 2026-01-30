from django.shortcuts import render, redirect, resolve_url
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LoginView
from django.contrib import messages
from .forms import CustomUserCreationForm
from .models import User
from django.contrib.auth.forms import AuthenticationForm

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

def sub_admin_login_view(request):
    """
    Dedicated login view for Sub-Admins.
    Checks if the user has specific roles before allowing access.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            # Strict Role Check
            if user.role in [User.Role.SUB_ADMIN, User.Role.ADMIN] or user.is_superuser:
                auth_login(request, user)
                return redirect('staff_portal')
            else:
                messages.error(request, "Access Denied: You are not a Sub-Admin.")
        else:
            messages.error(request, "Invalid credentials or account inactive.")
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/sub_admin_login.html', {'form': form})
