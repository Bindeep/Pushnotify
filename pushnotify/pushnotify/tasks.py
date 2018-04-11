import celery
from fcm_django.models import FCMDevice
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import HttpResponse

@celery.task()
def send(self):
    request = self.request
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
                users_devices.send_message(title='message', body=message)
                return HttpResponse('Message Send Successfully')
            else:
                return HttpResponse('No Device is associated with this user')
        else:
            return HttpResponse('Please Select Some user or group to send message')
    else:
        return HttpResponse('Write some message to send')

@celery.task()
def send_messages(users_devices, message):
    users_devices.send_message(title='message', body=message)
    return HttpResponse('Message Send Successfully')