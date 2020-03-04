from django.conf.urls import url
from . import api

urlpatterns = [
    url('init', api.initialize),
    url('move', api.move),
    url('say', api.say),
    url('rooms', api.rooms),
    url('interact', api.interact),
    url(r'room/(?P<room_id>\d+)/$', api.single_room, name='single_room')
]
