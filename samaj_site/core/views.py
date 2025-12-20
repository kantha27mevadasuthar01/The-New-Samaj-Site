from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import FileResponse, Http404
from django.conf import settings
from django.template.loader import render_to_string
import io
from reportlab.pdfgen import canvas

from .models import Post, Member
from .forms import PostForm, MemberForm, HomePageForm

# Staff check decorator
def staff_required(view):
    return login_required(user_passes_test(lambda u: u.is_staff)(view))

# Editor login
class EditorLoginView(LoginView):
    template_name = 'login.html'

# =========================
# PUBLIC VIEWS
# =========================

def home(request):
    posts = Post.objects.filter(post_type='text').order_by('-created_at')[:50]
    return render(request, 'home.html', {'posts': posts})

def photos(request):
    posts = Post.objects.filter(post_type='photo').order_by('-created_at')
    return render(request, 'photos.html', {'posts': posts})

def videos(request):
    posts = Post.objects.filter(post_type='video').order_by('-created_at')
    return render(request, 'videos.html', {'posts': posts})

# =========================
# LOGIN REQUIRED
# =========================

@login_required
def members(request):
    members = Member.objects.all().order_by('name')
    return render(request, 'members.html', {'members': members})

@login_required
def download_post_file(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if not post.file:
        raise Http404("File not found.")
    return FileResponse(post.file.open(), as_attachment=True)

@login_required
def download_members_pdf(request):
    members = Member.objects.all().order_by('name')
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    y = 800
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y, "Members List")
    y -= 30
    p.setFont("Helvetica", 12)
    for member in members:
        p.drawString(50, y, f"{member.name} - {member.email if hasattr(member, 'email') else ''}")
        y -= 20
        if y < 50:
            p.showPage()
            y = 800
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="members.pdf")

# =========================
# STAFF ONLY
# =========================

@staff_required
def manage_members(request):
    members = Member.objects.all().order_by('name')
    return render(request, 'manage_members.html', {'members': members})

@staff_required
def add_member(request):
    form = MemberForm(request.POST or None)
    if form.is_valid():
        member = form.save()
        messages.success(request, f"Member '{member.name}' added successfully.")
        return redirect('manage_members')
    return render(request, 'add_member.html', {'form': form})

@staff_required
def edit_member(request, id):
    member = get_object_or_404(Member, id=id)
    form = MemberForm(request.POST or None, instance=member)
    if form.is_valid():
        form.save()
        messages.success(request, f"Member '{member.name}' updated successfully.")
        return redirect('manage_members')
    return render(request, 'edit_member.html', {'form': form, 'member': member})

@staff_required
def delete_member(request, id):
    member = get_object_or_404(Member, id=id)
    if request.method == 'POST':
        member.delete()
        messages.success(request, f"Member '{member.name}' deleted successfully.")
        return redirect('manage_members')
    return render(request, 'delete_member.html', {'member': member})

@staff_required
def add_post(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        post = form.save()
        messages.success(request, f"Post '{post.title}' added successfully.")
        return redirect('home')
    return render(request, 'add_post.html', {'form': form})

@staff_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        form.save()
        messages.success(request, f"Post '{post.title}' updated successfully.")
        return redirect('home')
    return render(request, 'edit_post.html', {'form': form, 'post': post})

@staff_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        post.delete()
        messages.success(request, f"Post '{post.title}' deleted successfully.")
        return redirect('home')
    return render(request, 'delete_post.html', {'post': post})

@staff_required
def edit_home(request):
    form = HomePageForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Home page updated successfully.")
        return redirect('home')
    return render(request, 'edit_home.html', {'form': form})

# Context processor
def base_context(request):
    return {
        'site_name': 'Samaj Site',
        'user': request.user,
    }
@staff_required
def download_posts_pdf(request, post_type): 
    posts = Post.objects.filter(post_type=post_type).order_by('created_at')
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    y = 800
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y, f"{post_type.capitalize()} Posts List")
    y -= 30
    p.setFont("Helvetica", 12)
    for post in posts:
        p.drawString(50, y, f"{post.title} - {post.created_at.strftime('%Y-%m-%d')}")
        y -= 20
        if y < 50:
            p.showPage()
            y = 800
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f"{post_type}_posts.pdf")  