
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q

from .models import AuditLog


@login_required
def activity_logs_view(request):

    # Only administrators can access activity logs
    if not request.user.is_superuser:
        try:
            if request.user.userprofile.role != 'ADMIN':
                raise PermissionDenied
        except AttributeError:
            raise PermissionDenied

    # Get search and filter values
    search_query = request.GET.get('search', '').strip()
    action_filter = request.GET.get('action', '').strip()
    date_filter = request.GET.get('date', '').strip()

    # Get all activity logs
    logs = AuditLog.objects.select_related(
        'actor',
        'document',
        'target_user'
    )

    # Search by username, document title or details
    if search_query:
        logs = logs.filter(
            Q(actor__username__icontains=search_query) |
            Q(target_user__username__icontains=search_query) |
            Q(document__title__icontains=search_query) |
            Q(details__icontains=search_query)
        )

    # Filter by activity type
    if action_filter:
        valid_actions = [
            choice[0] for choice in AuditLog.ACTION_CHOICES
        ]

        if action_filter in valid_actions:
            logs = logs.filter(action=action_filter)

    # Filter by date
    if date_filter:
        logs = logs.filter(timestamp__date=date_filter)

    logs = logs.order_by('-timestamp')

    return render(
        request,
        'audit/activity_logs.html',
        {
            'logs': logs,
            'search_query': search_query,
            'action_filter': action_filter,
            'date_filter': date_filter,
            'action_choices': AuditLog.ACTION_CHOICES,
        }
    )
