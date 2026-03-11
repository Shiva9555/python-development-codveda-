"""
=============================================================
  
  Django Web Application with Authentication
  
  HOW TO USE:
    1. pip install django
    2. python setup_django_project.py
    3. cd codveda_blog
    4. python manage.py makemigrations accounts
    5. python manage.py migrate
    6. python manage.py createsuperuser
    7. python manage.py runserver
    8. Open http://127.0.0.1:8000/
=============================================================
"""

import os

# ── root folder name ──────────────────────────────────────
PROJECT = "codveda_blog"

# ── helper: create file + all parent dirs ─────────────────
def write(path, content):
    full = os.path.join(PROJECT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Created  {path}")

# ══════════════════════════════════════════════════════════
#  FILE CONTENTS
# ══════════════════════════════════════════════════════════

FILES = {}

# ── manage.py ─────────────────────────────────────────────
FILES["manage.py"] = '''#!/usr/bin/env python
import os, sys
def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Install Django: pip install django") from exc
    execute_from_command_line(sys.argv)
if __name__ == "__main__":
    main()
'''

# ── core/__init__.py ──────────────────────────────────────
FILES["core/__init__.py"] = ""

# ── core/settings.py ──────────────────────────────────────
FILES["core/settings.py"] = '''
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = "django-insecure-codveda-2024-change-in-production"
DEBUG = True
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "accounts",
    "blog",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [BASE_DIR / "templates"],
    "APP_DIRS": True,
    "OPTIONS": {"context_processors": [
        "django.template.context_processors.debug",
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
    ]},
}]

WSGI_APPLICATION = "core.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
STATIC_URL = "/static/"
MEDIA_URL  = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL            = "/accounts/login/"
LOGIN_REDIRECT_URL   = "/dashboard/"
LOGOUT_REDIRECT_URL  = "/accounts/login/"

# ── Email: prints to terminal in development ──────────────
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
# For real Gmail SMTP, replace the line above with:
# EMAIL_BACKEND       = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST          = "smtp.gmail.com"
# EMAIL_PORT          = 587
# EMAIL_USE_TLS       = True
# EMAIL_HOST_USER     = "you@gmail.com"
# EMAIL_HOST_PASSWORD = "your-app-password"
# DEFAULT_FROM_EMAIL  = "you@gmail.com"
'''

# ── core/urls.py ──────────────────────────────────────────
FILES["core/urls.py"] = '''
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/",     admin.site.urls),
    path("accounts/",  include("accounts.urls")),
    path("accounts/",  include("django.contrib.auth.urls")),  # password_reset etc.
    path("",           include("blog.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
'''

# ── core/wsgi.py ──────────────────────────────────────────
FILES["core/wsgi.py"] = '''
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
application = get_wsgi_application()
'''

# ══════════════════════════════════════════════════════════
#  ACCOUNTS APP
# ══════════════════════════════════════════════════════════

FILES["accounts/__init__.py"] = ""

FILES["accounts/apps.py"] = '''
from django.apps import AppConfig
class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"
'''

FILES["accounts/models.py"] = '''
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ("admin",  "Admin"),
        ("editor", "Editor"),
        ("viewer", "Viewer"),
    ]
    user      = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role      = models.CharField(max_length=20, choices=ROLE_CHOICES, default="viewer")
    bio       = models.TextField(blank=True)
    avatar    = models.ImageField(upload_to="avatars/", blank=True, null=True)
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"

    @property
    def is_admin_role(self):
        return self.role == "admin"

    @property
    def is_editor_role(self):
        return self.role in ("admin", "editor")
'''

FILES["accounts/forms.py"] = '''
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile


def _w(widget, **attrs):
    widget.attrs.update({"class": "form-control", **attrs})
    return widget


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50,
        widget=forms.TextInput(attrs={"class":"form-control","placeholder":"First name"}))
    last_name  = forms.CharField(max_length=50,
        widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Last name"}))
    email      = forms.EmailField(required=True,
        widget=forms.EmailInput(attrs={"class":"form-control","placeholder":"Email address"}))

    class Meta:
        model  = User
        fields = ["username","first_name","last_name","email","password1","password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs.setdefault("class", "form-control")

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"class":"form-control","placeholder":"Username"})
        self.fields["password"].widget.attrs.update({"class":"form-control","placeholder":"Password"})


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model   = UserProfile
        fields  = ["bio", "role"]
        widgets = {
            "bio":  forms.Textarea(attrs={"class":"form-control","rows":3}),
            "role": forms.Select(attrs={"class":"form-select"}),
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model   = User
        fields  = ["first_name","last_name","email"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class":"form-control"}),
            "last_name":  forms.TextInput(attrs={"class":"form-control"}),
            "email":      forms.EmailInput(attrs={"class":"form-control"}),
        }
'''

FILES["accounts/views.py"] = '''
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileUpdateForm, UserUpdateForm
from .models import UserProfile


def _profile(user):
    obj, _ = UserProfile.objects.get_or_create(user=user)
    return obj


# ── Register ─────────────────────────────────────────────
def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            grp, _ = Group.objects.get_or_create(name="Viewer")
            user.groups.add(grp)
            UserProfile.objects.create(user=user, role="viewer")
            messages.success(request, "Account created! Please log in.")
            return redirect("login")
        messages.error(request, "Please fix the errors below.")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


# ── Login ─────────────────────────────────────────────────
def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(request,
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"])
            if user:
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name or user.username}!")
                return redirect("dashboard")
        messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})


# ── Logout ────────────────────────────────────────────────
@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("login")


# ── Dashboard ─────────────────────────────────────────────
@login_required
def dashboard_view(request):
    from blog.models import Post
    profile   = _profile(request.user)
    my_posts  = Post.objects.filter(author=request.user).order_by("-created_at")[:5]
    all_users = None
    if profile.is_admin_role or request.user.is_staff:
        all_users = User.objects.all().select_related("profile")
    return render(request, "accounts/dashboard.html", {
        "profile":   profile,
        "my_posts":  my_posts,
        "all_users": all_users,
    })


# ── Profile ───────────────────────────────────────────────
@login_required
def profile_view(request):
    profile = _profile(request.user)
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save(); p_form.save()
            messages.success(request, "Profile updated!")
            return redirect("profile")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)
    return render(request, "accounts/profile.html",
                  {"u_form": u_form, "p_form": p_form, "profile": profile})


# ── Admin Panel ───────────────────────────────────────────
@login_required
def admin_panel_view(request):
    profile = _profile(request.user)
    if not (profile.is_admin_role or request.user.is_staff):
        messages.error(request, "Access denied! Admins only.")
        return redirect("dashboard")

    # Change role action
    if request.method == "POST":
        uid  = request.POST.get("user_id")
        role = request.POST.get("role")
        if uid and role:
            target = get_object_or_404(User, pk=uid)
            tprof  = _profile(target)
            tprof.role = role; tprof.save()
            messages.success(request, f"Role updated for {target.username}.")

    users = User.objects.all().select_related("profile")
    return render(request, "accounts/admin_panel.html", {"users": users})
'''

FILES["accounts/urls.py"] = '''
from django.urls import path
from . import views

urlpatterns = [
    path("register/",    views.register_view,    name="register"),
    path("login/",       views.login_view,        name="login"),
    path("logout/",      views.logout_view,       name="logout"),
    path("dashboard/",   views.dashboard_view,    name="dashboard"),
    path("profile/",     views.profile_view,      name="profile"),
    path("admin-panel/", views.admin_panel_view,  name="admin_panel"),
]
'''

FILES["accounts/admin.py"] = '''
from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display  = ["user", "role", "created_at"]
    list_filter   = ["role"]
    search_fields = ["user__username", "user__email"]
'''

# ══════════════════════════════════════════════════════════
#  BLOG APP
# ══════════════════════════════════════════════════════════

FILES["blog/__init__.py"] = ""

FILES["blog/apps.py"] = '''
from django.apps import AppConfig
class BlogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "blog"
'''

FILES["blog/models.py"] = '''
from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title      = models.CharField(max_length=200)
    content    = models.TextField()
    author     = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published  = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Comment(models.Model):
    post       = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author     = models.ForeignKey(User, on_delete=models.CASCADE)
    content    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"
'''

FILES["blog/forms.py"] = '''
from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model   = Post
        fields  = ["title", "content", "published"]
        widgets = {
            "title":   forms.TextInput(attrs={"class":"form-control","placeholder":"Post title"}),
            "content": forms.Textarea(attrs={"class":"form-control","rows":8}),
            "published": forms.CheckboxInput(attrs={"class":"form-check-input"}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model   = Comment
        fields  = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={"class":"form-control","rows":3,
                                              "placeholder":"Write a comment..."}),
        }
        labels = {"content": ""}
'''

FILES["blog/views.py"] = '''
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, Comment
from .forms import PostForm, CommentForm


# ── Home / Post list ──────────────────────────────────────
def home_view(request):
    posts = Post.objects.filter(published=True).select_related("author")
    return render(request, "blog/home.html", {"posts": posts})


# ── Post detail + comments ────────────────────────────────
def post_detail(request, pk):
    post     = get_object_or_404(Post, pk=pk, published=True)
    comments = post.comments.select_related("author")
    form     = CommentForm()

    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.warning(request, "Log in to comment.")
            return redirect("login")
        form = CommentForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.post   = post
            c.author = request.user
            c.save()
            messages.success(request, "Comment posted!")
            return redirect("post_detail", pk=pk)

    return render(request, "blog/post_detail.html",
                  {"post": post, "comments": comments, "form": form})


# ── Create post ───────────────────────────────────────────
@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post        = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Post published!")
            return redirect("post_detail", pk=post.pk)
    else:
        form = PostForm()
    return render(request, "blog/post_form.html", {"form": form, "action": "Create"})


# ── Edit post ─────────────────────────────────────────────
@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    from accounts.models import UserProfile
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if post.author != request.user and not (profile.is_admin_role or request.user.is_staff):
        messages.error(request, "You can only edit your own posts.")
        return redirect("home")
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated!")
            return redirect("post_detail", pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, "blog/post_form.html", {"form": form, "action": "Edit"})


# ── Delete post ───────────────────────────────────────────
@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    from accounts.models import UserProfile
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if post.author != request.user and not (profile.is_admin_role or request.user.is_staff):
        messages.error(request, "You can only delete your own posts.")
        return redirect("home")
    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted.")
        return redirect("home")
    return render(request, "blog/post_confirm_delete.html", {"post": post})
'''

FILES["blog/urls.py"] = '''
from django.urls import path
from . import views

urlpatterns = [
    path("",            views.home_view,    name="home"),
    path("dashboard/",  views.home_view,    name="dashboard_redirect"),
    path("post/<int:pk>/",        views.post_detail, name="post_detail"),
    path("post/create/",          views.post_create, name="post_create"),
    path("post/<int:pk>/edit/",   views.post_edit,   name="post_edit"),
    path("post/<int:pk>/delete/", views.post_delete, name="post_delete"),
]
'''

FILES["blog/admin.py"] = '''
from django.contrib import admin
from .models import Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display  = ["title", "author", "published", "created_at"]
    list_filter   = ["published"]
    search_fields = ["title", "author__username"]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display  = ["author", "post", "created_at"]
'''

# ══════════════════════════════════════════════════════════
#  BASE TEMPLATE
# ══════════════════════════════════════════════════════════

FILES["templates/base.html"] = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{% block title %}Codveda Blog{% endblock %}</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
  <style>
    :root{--primary:#00d4aa;--dark:#1a1a2e;}
    body{background:#f4f6f9;font-family:"Segoe UI",sans-serif;}
    .navbar{background:linear-gradient(135deg,var(--dark),#16213e)!important;}
    .navbar-brand{color:var(--primary)!important;font-weight:700;font-size:1.4rem;}
    .nav-link{color:rgba(255,255,255,.8)!important;transition:.2s;}
    .nav-link:hover{color:var(--primary)!important;}
    .card{border:none;border-radius:14px;box-shadow:0 3px 20px rgba(0,0,0,.08);}
    .btn-primary{background:var(--primary);border-color:var(--primary);color:#fff;}
    .btn-primary:hover{background:#00b894;border-color:#00b894;}
    .badge-admin{background:#e74c3c!important;}
    .badge-editor{background:#f39c12!important;}
    .badge-viewer{background:#3498db!important;}
    .post-card:hover{transform:translateY(-3px);transition:.3s;}
    footer{background:var(--dark);color:rgba(255,255,255,.6);}
  </style>
</head>
<body>

<nav class="navbar navbar-expand-lg shadow-sm">
 <div class="container">
  <a class="navbar-brand" href="{% url 'home' %}"><i class="fas fa-blog"></i> Codveda Blog</a>
  <button class="navbar-toggler border-0" type="button" data-bs-toggle="collapse" data-bs-target="#nb">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="nb">
   <ul class="navbar-nav ms-auto align-items-center gap-1">
    {% if user.is_authenticated %}
      <li class="nav-item"><a class="nav-link" href="{% url 'home' %}"><i class="fas fa-home"></i> Home</a></li>
      <li class="nav-item"><a class="nav-link" href="{% url 'post_create' %}"><i class="fas fa-plus"></i> New Post</a></li>
      <li class="nav-item"><a class="nav-link" href="{% url 'dashboard' %}"><i class="fas fa-tachometer-alt"></i> Dashboard</a></li>
      <li class="nav-item"><a class="nav-link" href="{% url 'profile' %}"><i class="fas fa-user"></i> {{ user.username }}</a></li>
      {% if user.is_staff %}
      <li class="nav-item"><a class="nav-link" href="{% url 'admin_panel' %}"><i class="fas fa-cogs"></i> Admin</a></li>
      {% endif %}
      <li class="nav-item">
        <a class="btn btn-sm btn-outline-warning ms-2" href="{% url 'logout' %}"><i class="fas fa-sign-out-alt"></i> Logout</a>
      </li>
    {% else %}
      <li class="nav-item"><a class="nav-link" href="{% url 'login' %}"><i class="fas fa-sign-in-alt"></i> Login</a></li>
      <li class="nav-item"><a class="btn btn-sm btn-primary ms-2" href="{% url 'register' %}"><i class="fas fa-user-plus"></i> Register</a></li>
    {% endif %}
   </ul>
  </div>
 </div>
</nav>

<div class="container mt-3">
{% for m in messages %}
<div class="alert alert-{{ m.tags }} alert-dismissible fade show shadow-sm" role="alert">
  <i class="fas fa-info-circle me-2"></i>{{ m }}
  <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
</div>
{% endfor %}
</div>

<main class="container my-4">
  {% block content %}{% endblock %}
</main>

<footer class="py-4 mt-5">
  <div class="container text-center">
    <p class="mb-0"><i class="fas fa-code text-success"></i> Codveda Blog &mdash; Python Internship Level 3</p>
  </div>
</footer>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
'''

# ══════════════════════════════════════════════════════════
#  ACCOUNTS TEMPLATES
# ══════════════════════════════════════════════════════════

FILES["templates/accounts/register.html"] = '''{% extends "base.html" %}
{% block title %}Register{% endblock %}
{% block content %}
<div class="row justify-content-center">
 <div class="col-md-6 col-lg-5">
  <div class="card p-4 mt-3">
   <div class="text-center mb-3">
    <i class="fas fa-user-plus fa-3x text-primary mb-2"></i>
    <h3 class="fw-bold">Create Account</h3>
    <p class="text-muted">Join Codveda Blog today</p>
   </div>
   <form method="POST">
    {% csrf_token %}
    {% for field in form %}
     <div class="mb-3">
      <label class="form-label fw-semibold">{{ field.label }}</label>
      {{ field }}
      {% if field.help_text %}<div class="form-text">{{ field.help_text }}</div>{% endif %}
      {% if field.errors %}<div class="text-danger small mt-1">{{ field.errors }}</div>{% endif %}
     </div>
    {% endfor %}
    <div class="d-grid mt-2">
     <button class="btn btn-primary btn-lg"><i class="fas fa-user-plus me-2"></i>Register</button>
    </div>
   </form>
   <hr>
   <p class="text-center mb-0">Already have an account? <a href="{% url 'login' %}">Login here</a></p>
  </div>
 </div>
</div>
{% endblock %}
'''

FILES["templates/accounts/login.html"] = '''{% extends "base.html" %}
{% block title %}Login{% endblock %}
{% block content %}
<div class="row justify-content-center">
 <div class="col-md-5 col-lg-4">
  <div class="card p-4 mt-4">
   <div class="text-center mb-3">
    <i class="fas fa-lock fa-3x text-primary mb-2"></i>
    <h3 class="fw-bold">Welcome Back</h3>
    <p class="text-muted">Login to your account</p>
   </div>
   <form method="POST">
    {% csrf_token %}
    {% for field in form %}
     <div class="mb-3">
      <label class="form-label fw-semibold">{{ field.label }}</label>
      {{ field }}
      {% if field.errors %}<div class="text-danger small mt-1">{{ field.errors }}</div>{% endif %}
     </div>
    {% endfor %}
    <div class="d-grid mt-2">
     <button class="btn btn-primary btn-lg"><i class="fas fa-sign-in-alt me-2"></i>Login</button>
    </div>
   </form>
   <hr>
   <div class="text-center d-flex justify-content-between">
    <a href="{% url 'password_reset' %}"><i class="fas fa-key me-1"></i>Forgot Password?</a>
    <a href="{% url 'register' %}"><i class="fas fa-user-plus me-1"></i>Register</a>
   </div>
  </div>
 </div>
</div>
{% endblock %}
'''

FILES["templates/accounts/dashboard.html"] = '''{% extends "base.html" %}
{% block title %}Dashboard{% endblock %}
{% block content %}
<div class="row g-4">

 <!-- Welcome banner -->
 <div class="col-12">
  <div class="card p-4" style="background:linear-gradient(135deg,#1a1a2e,#16213e);color:#fff;">
   <div class="row align-items-center">
    <div class="col">
     <h2 class="mb-1">Hello, {{ user.first_name|default:user.username }}! 👋</h2>
     <p class="mb-0 opacity-75">
      Role:
      {% if profile.role == "admin" %}<span class="badge badge-admin">Admin</span>
      {% elif profile.role == "editor" %}<span class="badge badge-editor">Editor</span>
      {% else %}<span class="badge badge-viewer">Viewer</span>{% endif %}
      &nbsp;|&nbsp; {{ user.email }}
     </p>
    </div>
    <div class="col-auto"><i class="fas fa-user-circle fa-5x opacity-25"></i></div>
   </div>
  </div>
 </div>

 <!-- Stats -->
 <div class="col-md-4">
  <div class="card p-3 text-center h-100">
   <i class="fas fa-pen-nib fa-2x text-primary mb-2"></i>
   <h6 class="text-muted">My Posts</h6>
   <h3 class="fw-bold">{{ user.posts.count }}</h3>
  </div>
 </div>
 <div class="col-md-4">
  <div class="card p-3 text-center h-100">
   <i class="fas fa-calendar fa-2x text-success mb-2"></i>
   <h6 class="text-muted">Member Since</h6>
   <h5 class="fw-bold">{{ user.date_joined|date:"d M Y" }}</h5>
  </div>
 </div>
 <div class="col-md-4">
  <div class="card p-3 text-center h-100">
   <i class="fas fa-clock fa-2x text-warning mb-2"></i>
   <h6 class="text-muted">Last Login</h6>
   <h5 class="fw-bold">{{ user.last_login|date:"d M Y" }}</h5>
  </div>
 </div>

 <!-- Quick Actions -->
 <div class="col-12">
  <div class="card p-4">
   <h5 class="mb-3"><i class="fas fa-bolt text-warning me-2"></i>Quick Actions</h5>
   <div class="d-flex gap-2 flex-wrap">
    <a href="{% url 'post_create' %}" class="btn btn-primary"><i class="fas fa-plus me-1"></i>New Post</a>
    <a href="{% url 'profile' %}" class="btn btn-outline-secondary"><i class="fas fa-user-edit me-1"></i>Edit Profile</a>
    <a href="{% url 'password_change' %}" class="btn btn-outline-secondary"><i class="fas fa-key me-1"></i>Change Password</a>
    {% if profile.is_admin_role or user.is_staff %}
    <a href="{% url 'admin_panel' %}" class="btn btn-outline-danger"><i class="fas fa-cogs me-1"></i>Admin Panel</a>
    {% endif %}
   </div>
  </div>
 </div>

 <!-- My Recent Posts -->
 <div class="col-12">
  <div class="card p-4">
   <h5 class="mb-3"><i class="fas fa-newspaper me-2 text-primary"></i>My Recent Posts</h5>
   {% if my_posts %}
    <div class="table-responsive">
     <table class="table table-hover align-middle">
      <thead class="table-light"><tr><th>Title</th><th>Status</th><th>Date</th><th>Actions</th></tr></thead>
      <tbody>
       {% for post in my_posts %}
       <tr>
        <td><a href="{% url 'post_detail' post.pk %}" class="text-decoration-none fw-semibold">{{ post.title }}</a></td>
        <td>{% if post.published %}<span class="badge bg-success">Published</span>{% else %}<span class="badge bg-secondary">Draft</span>{% endif %}</td>
        <td>{{ post.created_at|date:"d M Y" }}</td>
        <td>
         <a href="{% url 'post_edit' post.pk %}" class="btn btn-sm btn-outline-primary me-1"><i class="fas fa-edit"></i></a>
         <a href="{% url 'post_delete' post.pk %}" class="btn btn-sm btn-outline-danger"><i class="fas fa-trash"></i></a>
        </td>
       </tr>
       {% endfor %}
      </tbody>
     </table>
    </div>
   {% else %}
    <p class="text-muted">No posts yet. <a href="{% url 'post_create' %}">Create your first post!</a></p>
   {% endif %}
  </div>
 </div>

 <!-- Admin: All users -->
 {% if all_users %}
 <div class="col-12">
  <div class="card p-4">
   <h5 class="mb-3"><i class="fas fa-users me-2 text-danger"></i>All Users (Admin View)</h5>
   <div class="table-responsive">
    <table class="table table-hover">
     <thead class="table-dark"><tr><th>ID</th><th>Username</th><th>Email</th><th>Role</th><th>Staff</th><th>Joined</th></tr></thead>
     <tbody>
      {% for u in all_users %}
      <tr>
       <td>{{ u.id }}</td>
       <td><strong>{{ u.username }}</strong></td>
       <td>{{ u.email }}</td>
       <td>{% if u.profile %}<span class="badge {% if u.profile.role == 'admin' %}badge-admin{% elif u.profile.role == 'editor' %}badge-editor{% else %}badge-viewer{% endif %}">{{ u.profile.role|capfirst }}</span>{% endif %}</td>
       <td>{% if u.is_staff %}<i class="fas fa-check text-success"></i>{% else %}<i class="fas fa-times text-danger"></i>{% endif %}</td>
       <td>{{ u.date_joined|date:"d M Y" }}</td>
      </tr>
      {% endfor %}
     </tbody>
    </table>
   </div>
  </div>
 </div>
 {% endif %}

</div>
{% endblock %}
'''

FILES["templates/accounts/profile.html"] = '''{% extends "base.html" %}
{% block title %}Edit Profile{% endblock %}
{% block content %}
<div class="row justify-content-center">
 <div class="col-md-7">
  <div class="card p-4">
   <h4 class="mb-4"><i class="fas fa-user-edit text-primary me-2"></i>Edit Profile</h4>
   <form method="POST">
    {% csrf_token %}
    <h6 class="text-muted mb-3 border-bottom pb-2">Personal Information</h6>
    {% for field in u_form %}
     <div class="mb-3">
      <label class="form-label fw-semibold">{{ field.label }}</label>
      {{ field }}
      {% if field.errors %}<div class="text-danger small">{{ field.errors }}</div>{% endif %}
     </div>
    {% endfor %}
    <h6 class="text-muted mb-3 mt-4 border-bottom pb-2">About & Role</h6>
    {% for field in p_form %}
     <div class="mb-3">
      <label class="form-label fw-semibold">{{ field.label }}</label>
      {{ field }}
     </div>
    {% endfor %}
    <div class="d-grid mt-3">
     <button class="btn btn-primary btn-lg"><i class="fas fa-save me-2"></i>Save Changes</button>
    </div>
   </form>
  </div>
 </div>
</div>
{% endblock %}
'''

FILES["templates/accounts/admin_panel.html"] = '''{% extends "base.html" %}
{% block title %}Admin Panel{% endblock %}
{% block content %}
<div class="card p-4">
 <h4 class="mb-4"><i class="fas fa-cogs text-danger me-2"></i>Admin Panel — Manage Users</h4>
 <div class="table-responsive">
  <table class="table table-hover align-middle">
   <thead class="table-dark">
    <tr><th>ID</th><th>Username</th><th>Email</th><th>Current Role</th><th>Change Role</th></tr>
   </thead>
   <tbody>
    {% for u in users %}
    <tr>
     <td>{{ u.id }}</td>
     <td><strong>{{ u.username }}</strong></td>
     <td>{{ u.email }}</td>
     <td>{% if u.profile %}<span class="badge {% if u.profile.role == 'admin' %}bg-danger{% elif u.profile.role == 'editor' %}bg-warning text-dark{% else %}bg-primary{% endif %}">{{ u.profile.role|capfirst }}</span>{% endif %}</td>
     <td>
      <form method="POST" class="d-flex gap-2">
       {% csrf_token %}
       <input type="hidden" name="user_id" value="{{ u.id }}">
       <select name="role" class="form-select form-select-sm" style="width:130px;">
        <option value="viewer"  {% if u.profile.role == "viewer"  %}selected{% endif %}>Viewer</option>
        <option value="editor"  {% if u.profile.role == "editor"  %}selected{% endif %}>Editor</option>
        <option value="admin"   {% if u.profile.role == "admin"   %}selected{% endif %}>Admin</option>
       </select>
       <button class="btn btn-sm btn-primary" type="submit"><i class="fas fa-save"></i></button>
      </form>
     </td>
    </tr>
    {% endfor %}
   </tbody>
  </table>
 </div>
</div>
{% endblock %}
'''

# ══════════════════════════════════════════════════════════
#  PASSWORD RESET TEMPLATES
# ══════════════════════════════════════════════════════════

FILES["templates/registration/password_reset_form.html"] = '''{% extends "base.html" %}
{% block title %}Reset Password{% endblock %}
{% block content %}
<div class="row justify-content-center">
 <div class="col-md-5">
  <div class="card p-4 mt-4">
   <div class="text-center mb-3">
    <i class="fas fa-key fa-3x text-warning mb-2"></i>
    <h3 class="fw-bold">Forgot Password?</h3>
    <p class="text-muted">Enter your email to receive reset instructions.</p>
   </div>
   <form method="POST">{% csrf_token %}
    <div class="mb-3">
     <label class="form-label fw-semibold">Email Address</label>
     <input type="email" name="email" class="form-control" placeholder="your@email.com" required>
    </div>
    <div class="d-grid">
     <button class="btn btn-warning btn-lg"><i class="fas fa-paper-plane me-2"></i>Send Reset Link</button>
    </div>
   </form>
   <div class="text-center mt-3"><a href="{% url 'login' %}">Back to Login</a></div>
  </div>
 </div>
</div>
{% endblock %}
'''

FILES["templates/registration/password_reset_done.html"] = '''{% extends "base.html" %}
{% block title %}Email Sent{% endblock %}
{% block content %}
<div class="row justify-content-center">
 <div class="col-md-5">
  <div class="card p-4 text-center mt-4">
   <i class="fas fa-envelope-open-text fa-4x text-success mb-3"></i>
   <h3>Check Your Email</h3>
   <p class="text-muted">If an account exists for that email, a password reset link has been sent.<br>(Check your terminal in development mode)</p>
   <a href="{% url 'login' %}" class="btn btn-primary mt-2">Back to Login</a>
  </div>
 </div>
</div>
{% endblock %}
'''

FILES["templates/registration/password_reset_confirm.html"] = '''{% extends "base.html" %}
{% block title %}Set New Password{% endblock %}
{% block content %}
<div class="row justify-content-center">
 <div class="col-md-5">
  <div class="card p-4 mt-4">
   <h3 class="text-center mb-4"><i class="fas fa-lock-open text-primary me-2"></i>Set New Password</h3>
   {% if validlink %}
   <form method="POST">{% csrf_token %}
    {% for field in form %}
     <div class="mb-3">
      <label class="form-label fw-semibold">{{ field.label }}</label>
      <input type="password" name="{{ field.html_name }}" class="form-control" required>
      {% if field.errors %}<div class="text-danger small">{{ field.errors }}</div>{% endif %}
     </div>
    {% endfor %}
    <div class="d-grid"><button class="btn btn-primary btn-lg">Set Password</button></div>
   </form>
   {% else %}
   <div class="alert alert-danger">This reset link is invalid or expired. <a href="{% url 'password_reset' %}">Request a new one.</a></div>
   {% endif %}
  </div>
 </div>
</div>
{% endblock %}
'''

FILES["templates/registration/password_reset_complete.html"] = '''{% extends "base.html" %}
{% block title %}Password Reset Complete{% endblock %}
{% block content %}
<div class="row justify-content-center">
 <div class="col-md-5">
  <div class="card p-4 text-center mt-4">
   <i class="fas fa-check-circle fa-4x text-success mb-3"></i>
   <h3>Password Reset!</h3>
   <p class="text-muted">Your password has been set successfully.</p>
   <a href="{% url 'login' %}" class="btn btn-primary mt-2"><i class="fas fa-sign-in-alt me-2"></i>Login Now</a>
  </div>
 </div>
</div>
{% endblock %}
'''

FILES["templates/registration/password_change_form.html"] = '''{% extends "base.html" %}
{% block title %}Change Password{% endblock %}
{% block content %}
<div class="row justify-content-center">
 <div class="col-md-5">
  <div class="card p-4 mt-4">
   <h4 class="mb-4"><i class="fas fa-key text-primary me-2"></i>Change Password</h4>
   <form method="POST">{% csrf_token %}
    {% for field in form %}
     <div class="mb-3">
      <label class="form-label fw-semibold">{{ field.label }}</label>
      <input type="password" name="{{ field.html_name }}" class="form-control" required>
      {% if field.errors %}<div class="text-danger small">{{ field.errors }}</div>{% endif %}
     </div>
    {% endfor %}
    <div class="d-grid"><button class="btn btn-primary btn-lg">Update Password</button></div>
   </form>
  </div>
 </div>
</div>
{% endblock %}
'''

FILES["templates/registration/password_change_done.html"] = '''{% extends "base.html" %}
{% block title %}Password Changed{% endblock %}
{% block content %}
<div class="row justify-content-center">
 <div class="col-md-5">
  <div class="card p-4 text-center mt-4">
   <i class="fas fa-check-circle fa-4x text-success mb-3"></i>
   <h3>Password Changed!</h3>
   <a href="{% url 'dashboard' %}" class="btn btn-primary mt-2">Go to Dashboard</a>
  </div>
 </div>
</div>
{% endblock %}
'''

# ══════════════════════════════════════════════════════════
#  BLOG TEMPLATES
# ══════════════════════════════════════════════════════════

FILES["templates/blog/home.html"] = '''{% extends "base.html" %}
{% block title %}Home - Codveda Blog{% endblock %}
{% block content %}
<div class="row">
 <div class="col-12 mb-4">
  <div class="card p-4 text-center" style="background:linear-gradient(135deg,#1a1a2e,#16213e);color:#fff;">
   <h1 class="fw-bold"><i class="fas fa-blog me-2" style="color:#00d4aa"></i>Codveda Blog</h1>
   <p class="opacity-75 mb-3">Django Web App &mdash; Codveda Python Internship Level 3</p>
   {% if not user.is_authenticated %}
   <div class="d-flex justify-content-center gap-3">
    <a href="{% url 'register' %}" class="btn btn-primary"><i class="fas fa-user-plus me-1"></i>Register</a>
    <a href="{% url 'login' %}" class="btn btn-outline-light"><i class="fas fa-sign-in-alt me-1"></i>Login</a>
   </div>
   {% else %}
   <a href="{% url 'post_create' %}" class="btn btn-primary"><i class="fas fa-plus me-1"></i>Write New Post</a>
   {% endif %}
  </div>
 </div>

 {% if posts %}
  {% for post in posts %}
  <div class="col-md-6 col-lg-4 mb-4">
   <div class="card h-100 post-card">
    <div class="card-body d-flex flex-column">
     <h5 class="card-title fw-bold">{{ post.title }}</h5>
     <p class="card-text text-muted flex-grow-1">{{ post.content|truncatewords:25 }}</p>
     <div class="d-flex justify-content-between align-items-center mt-3">
      <small class="text-muted"><i class="fas fa-user me-1"></i>{{ post.author.username }}</small>
      <small class="text-muted">{{ post.created_at|date:"d M Y" }}</small>
     </div>
    </div>
    <div class="card-footer bg-transparent d-flex justify-content-between">
     <a href="{% url 'post_detail' post.pk %}" class="btn btn-sm btn-primary"><i class="fas fa-book-open me-1"></i>Read</a>
     {% if user == post.author or user.is_staff %}
     <div>
      <a href="{% url 'post_edit' post.pk %}" class="btn btn-sm btn-outline-secondary me-1"><i class="fas fa-edit"></i></a>
      <a href="{% url 'post_delete' post.pk %}" class="btn btn-sm btn-outline-danger"><i class="fas fa-trash"></i></a>
     </div>
     {% endif %}
    </div>
   </div>
  </div>
  {% endfor %}
 {% else %}
  <div class="col-12 text-center py-5">
   <i class="fas fa-inbox fa-4x text-muted mb-3"></i>
   <h4 class="text-muted">No posts yet!</h4>
   {% if user.is_authenticated %}
   <a href="{% url 'post_create' %}" class="btn btn-primary mt-2">Write the First Post</a>
   {% endif %}
  </div>
 {% endif %}
</div>
{% endblock %}
'''

FILES["templates/blog/post_detail.html"] = '''{% extends "base.html" %}
{% block title %}{{ post.title }}{% endblock %}
{% block content %}
<div class="row justify-content-center">
 <div class="col-lg-8">
  <div class="card p-4 mb-4">
   <h2 class="fw-bold mb-2">{{ post.title }}</h2>
   <div class="d-flex gap-3 text-muted mb-4 small">
    <span><i class="fas fa-user me-1"></i>{{ post.author.username }}</span>
    <span><i class="fas fa-calendar me-1"></i>{{ post.created_at|date:"d M Y, H:i" }}</span>
    <span><i class="fas fa-comments me-1"></i>{{ comments.count }} comment{{ comments.count|pluralize }}</span>
   </div>
   <div class="border-top pt-3" style="white-space:pre-wrap;line-height:1.8;">{{ post.content }}</div>
   {% if user == post.author or user.is_staff %}
   <div class="d-flex gap-2 mt-4 border-top pt-3">
    <a href="{% url 'post_edit' post.pk %}" class="btn btn-outline-primary btn-sm"><i class="fas fa-edit me-1"></i>Edit</a>
    <a href="{% url 'post_delete' post.pk %}" class="btn btn-outline-danger btn-sm"><i class="fas fa-trash me-1"></i>Delete</a>
   </div>
   {% endif %}
  </div>

  <!-- Comments -->
  <div class="card p-4 mb-4">
   <h5 class="mb-3"><i class="fas fa-comments text-primary me-2"></i>Comments ({{ comments.count }})</h5>
   {% for c in comments %}
   <div class="border-bottom pb-3 mb-3">
    <div class="d-flex justify-content-between mb-1">
     <strong><i class="fas fa-user-circle me-1 text-primary"></i>{{ c.author.username }}</strong>
     <small class="text-muted">{{ c.created_at|date:"d M Y, H:i" }}</small>
    </div>
    <p class="mb-0">{{ c.content }}</p>
   </div>
   {% empty %}
   <p class="text-muted">No comments yet. Be the first!</p>
   {% endfor %}
  </div>

  <!-- Add comment -->
  <div class="card p-4">
   <h5 class="mb-3"><i class="fas fa-pen text-primary me-2"></i>Leave a Comment</h5>
   {% if user.is_authenticated %}
   <form method="POST">
    {% csrf_token %}
    {{ form }}
    <div class="d-grid mt-2">
     <button class="btn btn-primary"><i class="fas fa-paper-plane me-2"></i>Post Comment</button>
    </div>
   </form>
   {% else %}
   <p class="text-muted"><a href="{% url 'login' %}">Login</a> to leave a comment.</p>
   {% endif %}
  </div>

 </div>
</div>
{% endblock %}
'''

FILES["templates/blog/post_form.html"] = '''{% extends "base.html" %}
{% block title %}{{ action }} Post{% endblock %}
{% block content %}
<div class="row justify-content-center">
 <div class="col-lg-7">
  <div class="card p-4">
   <h4 class="mb-4"><i class="fas fa-pen-nib text-primary me-2"></i>{{ action }} Post</h4>
   <form method="POST">
    {% csrf_token %}
    {% for field in form %}
     <div class="mb-3">
      <label class="form-label fw-semibold">{{ field.label }}</label>
      {{ field }}
      {% if field.errors %}<div class="text-danger small">{{ field.errors }}</div>{% endif %}
     </div>
    {% endfor %}
    <div class="d-flex gap-2 mt-3">
     <button class="btn btn-primary btn-lg"><i class="fas fa-save me-2"></i>{{ action }} Post</button>
     <a href="{% url 'home' %}" class="btn btn-outline-secondary btn-lg">Cancel</a>
    </div>
   </form>
  </div>
 </div>
</div>
{% endblock %}
'''

FILES["templates/blog/post_confirm_delete.html"] = '''{% extends "base.html" %}
{% block title %}Delete Post{% endblock %}
{% block content %}
<div class="row justify-content-center">
 <div class="col-md-5">
  <div class="card p-4 text-center">
   <i class="fas fa-exclamation-triangle fa-3x text-danger mb-3"></i>
   <h4>Delete Post?</h4>
   <p class="text-muted">Are you sure you want to delete <strong>"{{ post.title }}"</strong>? This cannot be undone.</p>
   <form method="POST" class="d-flex justify-content-center gap-3">
    {% csrf_token %}
    <button type="submit" class="btn btn-danger"><i class="fas fa-trash me-2"></i>Yes, Delete</button>
    <a href="{% url 'home' %}" class="btn btn-outline-secondary">Cancel</a>
   </form>
  </div>
 </div>
</div>
{% endblock %}
'''

# ══════════════════════════════════════════════════════════
#  CREATE ALL FILES
# ══════════════════════════════════════════════════════════

def main():
    print(f"\n{'='*55}")
    print(f"  Creating Django project: {PROJECT}/")
    print(f"{'='*55}\n")

    for path, content in FILES.items():
        write(path, content.lstrip("\n"))

    # touch __init__.py files
    for pkg in ["core", "accounts", "blog"]:
        init = os.path.join(PROJECT, pkg, "__init__.py")
        if not os.path.exists(init):
            open(init, "w").close()

    print(f"\n{'='*55}")
    print("  ✅  Project created successfully!")
    print(f"{'='*55}")
    print(f"""
  NEXT STEPS:
  -----------
  1.  cd {PROJECT}
  2.  pip install django
  3.  python manage.py makemigrations accounts blog
  4.  python manage.py migrate
  5.  python manage.py createsuperuser
  6.  python manage.py runserver

  Then open:  http://127.0.0.1:8000/

  PAGES:
  ------
  /                     → Blog home
  /accounts/register/   → Register
  /accounts/login/      → Login
  /dashboard/           → User dashboard
  /profile/             → Edit profile
  /admin-panel/         → Manage user roles (admin only)
  /post/create/         → Write new post
  /accounts/password_reset/ → Forgot password
  /admin/               → Django admin panel
""")

main()
