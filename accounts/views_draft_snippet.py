from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from django.contrib.auth.decorators import login_required
from .models import User

# ... existing views ...

def sub_admin_login_view(request):
    """
    Dedicated login view for Sub-Admins.
    """
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            # Check for Sub-Admin Role
            if user.role in [User.Role.SUB_ADMIN, User.Role.ADMIN, 'SUB_ADMIN', 'ADMIN'] or user.is_superuser:
                login(request, user)
                return redirect('staff_portal') # Redirect to staff portal
            else:
                messages.error(request, "Access Denied: You are not a Sub-Admin.")
        else:
            messages.error(request, "Invalid credentials.")
    else:
        form = LoginForm()
    
    return render(request, 'accounts/sub_admin_login.html', {'form': form})

# ... make sure we didn't overwrite existing views, so we should append implementation ... 
# Wait, I cannot append easily with write_to_file. I need to read the file first or use replace.
# I will use multi_replace to insert this new view into views.py.
