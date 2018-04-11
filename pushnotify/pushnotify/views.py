from django.http import HttpResponse
from django.views.generic.list import ListView
from django.contrib.auth.models import User, Group
from fcm_django.models import FCMDevice
from django.db.models import Q
from datetime import datetime, timedelta
from django.views.generic import View
from .tasks import send, send_messages


class IndexView(ListView):
    template_name = 'message.html'
    model = User
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['groups'] = Group.objects.all()
        return context


class SendMessage(View):

    def post(self, request, *args, **kwargs):
        scheduled_time = request.POST.get('date')
        if scheduled_time:
            striped_date = datetime.strptime(scheduled_time, '%m/%d/%Y %I:%M %p')
            now = datetime.now()
            total_seconds = (striped_date - now).total_seconds()
            if total_seconds > 0:
                message = request.POST.getlist('message')[0]
                if message:
                    users = request.POST.getlist('users')
                    groups = request.POST.getlist('groups')
                    if groups or users:
                        users = User.objects.filter(
                            Q(groups__name__in=groups) |
                            Q(username__in=users)
                        ).distinct()
                        users_devices = FCMDevice.objects.filter(user__in=users)
                        if users_devices:
                            send_messages.apply_async(args=[users_devices, message],
                                                      eta=datetime.utcnow() + timedelta(seconds=total_seconds))
                        else:
                            return HttpResponse('No Device is associated with this user')
                    else:
                        return HttpResponse('Please Select Some user or group to send message')
                else:
                    return HttpResponse('Write some message to send')
                return HttpResponse('Scheduled Message')
            else:
                return HttpResponse('Please Choose time from futue')
        else:
            return send(self)