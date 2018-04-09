from django.http import HttpResponse
from django.views.generic.list import ListView
from django.contrib.auth.models import User, Group
from fcm_django.models import FCMDevice
from django.db.models import Q


class IndexView(ListView):
    template_name = 'message.html'
    model = User
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['groups'] = Group.objects.all()
        return context


def send_message(request):
    import ipdb
    ipdb.set_trace()
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

