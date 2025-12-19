from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Post, Member
from .forms import PostForm, MemberForm
from .forms import HomePageForm


# Staff check decorator
def staff_required(view):
    return login_required(user_passes_test(lambda u: u.is_staff)(view))

# Editor login
class EditorLoginView(LoginView):
    template_name = 'login.html'

# Home page (latest text posts + inline add/edit/delete)
def home(request):
    posts = Post.objects.filter(post_type='text').order_by('-created_at')[:50]

    # Handle new post submission
    if request.method == 'POST' and request.user.is_authenticated and request.user.is_staff:
        title = request.POST.get('title')
        content = request.POST.get('content')
        post_type = request.POST.get('post_type')
        file = request.FILES.get('file')

        post = Post.objects.create(
            title=title,
            content=content,
            post_type=post_type,
            file=file
        )
        messages.success(request, f"Post '{post.title}' added successfully.")

        # Redirect based on post type
        if post_type == "text":
            return redirect('home')
        elif post_type == "photo":
            return redirect('photos')
        else:
            return redirect('videos')

    return render(request, 'home.html', {'posts': posts})

# Photos page
def photos(request):
    posts = Post.objects.filter(post_type='photo').order_by('-created_at')
    return render(request, 'photos.html', {'posts': posts})

# Videos page
def videos(request):
    posts = Post.objects.filter(post_type='video').order_by('-created_at')
    return render(request, 'videos.html', {'posts': posts})

# Members page (public)
def members(request):
    members = Member.objects.all().order_by('name')
    return render(request, 'members.html', {'members': members})

# Members management (staff only)
@staff_required
def manage_members(request):
    members = Member.objects.all().order_by('name')
    return render(request, 'manage_members.html', {'members': members})

@staff_required
def add_member(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            member = form.save()
            messages.success(request, f"Member '{member.name}' added successfully.")
            return redirect('manage_members')
    else:
        form = MemberForm()
    return render(request, 'add_member.html', {'form': form})

@staff_required
def edit_member(request, id):
    member = get_object_or_404(Member, id=id)
    if request.method == 'POST':
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, f"Member '{member.name}' updated successfully.")
            return redirect('manage_members')
    else:
        form = MemberForm(instance=member)
    return render(request, 'edit_member.html', {'form': form, 'member': member})

@staff_required
def delete_member(request, id):
    member = get_object_or_404(Member, id=id)
    if request.method == 'POST':
        member.delete()
        messages.success(request, f"Member '{member.name}' deleted successfully.")
        return redirect('manage_members')
    return render(request, 'delete_member.html', {'member': member})

# Edit post (staff only)
@staff_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES or None, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, f"Post '{post.title}' updated successfully.")

            # Redirect based on post type
            if post.post_type == "text":
                return redirect('home')
            elif post.post_type == "photo":
                return redirect('photos')
            else:
                return redirect('videos')
    else:
        form = PostForm(instance=post)
    return render(request, 'edit_post.html', {'form': form, 'post': post})

# Delete post (staff only)
@staff_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post_type = post.post_type
    if request.method == 'POST':
        post.delete()
        messages.success(request, f"Post '{post.title}' deleted successfully.")

        if post_type == "text":
            return redirect('home')
        elif post_type == "photo":
            return redirect('photos')
        else:
            return redirect('videos')
    return render(request, 'delete_post.html', {'post': post})

# Context processor
def base_context(request):
    return {
        'site_name': 'Samaj Site',
        'user': request.user,
    }
# Edit home page content (staff only)
@staff_required
def edit_home(request):
    if request.method == 'POST':
        form = HomePageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Home page content updated successfully.")
            return redirect('home')
    else:
        form = HomePageForm()

    return render(request, 'edit_home.html', {'form': form})

@staff_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            messages.success(request, f"Post '{post.title}' added successfully.")
            if post.post_type == "text":
                return redirect('home')
            elif post.post_type == "photo":
                return redirect('photos')
            else:
                return redirect('videos')
    else:
        form = PostForm()
    return render(request, 'add_post.html', {'form': form})