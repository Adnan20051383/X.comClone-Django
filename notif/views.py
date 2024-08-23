from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from notif.models import Notification

@login_required
def show_notif(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    Notification.objects.filter(user=request.user).update(is_seen=True)
    context = {'notifications': notifications}
    return render(request, 'notif.html', context)


@login_required
def delete_notif(request, notif_id):
    notification = Notification.objects.filter(id=notif_id)
    notification.delete()
    return redirect('notifications')
