from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Donation

@login_required
def donate_view(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        # Mock payment process
        Donation.objects.create(
            user=request.user,
            amount=amount,
            transaction_id=f"TXN-{request.user.id}-{amount}" # Mock ID
        )
        messages.success(request, f"Thank you for your donation of ₹{amount}!")
        return redirect('my_donations')
    return render(request, 'donations/donate.html')

@login_required
def my_donations(request):
    donations = Donation.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'donations/my_donations.html', {'donations': donations})
