
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from documents.models import Document, DocumentPermission
from audit.models import AuditLog


# User Registration
def register_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')

        else:
            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            messages.success(request, 'Registration successful!')
            return redirect('login')

    return render(request, 'accounts/register.html')


# User Login
def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'accounts/login.html')


# User Dashboard with Real Statistics
@login_required
def dashboard_view(request):

    user = request.user

    # Check whether the user is an administrator
    is_admin = user.is_superuser

    if not is_admin:
        try:
            is_admin = user.userprofile.role == 'ADMIN'
        except AttributeError:
            is_admin = False

    if is_admin:
        # Admin sees overall system statistics
        total_documents = Document.objects.count()

        shared_documents = Document.objects.filter(
            permissions__isnull=False
        ).distinct().count()

        total_downloads = AuditLog.objects.filter(
            action='DOWNLOAD'
        ).count()

        security_incidents = AuditLog.objects.filter(
            action='ACCESS_DENIED'
        ).count()

    else:
        # Other users see their own statistics
        total_documents = Document.objects.filter(
            owner=user
        ).count()

        shared_documents = Document.objects.filter(
            permissions__user=user
        ).distinct().count()

        total_downloads = AuditLog.objects.filter(
            actor=user,
            action='DOWNLOAD'
        ).count()

        security_incidents = AuditLog.objects.filter(
            actor=user,
            action='ACCESS_DENIED'
        ).count()

    context = {
        'total_documents': total_documents,
        'shared_documents': shared_documents,
        'total_downloads': total_downloads,
        'security_incidents': security_incidents,
    }

    return render(
        request,
        'accounts/dashboard.html',
        context
    )


# User Logout
@login_required
@require_POST
def logout_view(request):

    logout(request)

    return redirect('login')
