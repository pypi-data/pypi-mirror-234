import json

from django.http import HttpResponse
from . import service

def default_message_handler(request):
    sleep = 0
    try:
        service.handle_message()
    except service.NoMoreMessages:
        sleep = 3

    return HttpResponse(json.dumps({
        'sleep': sleep
    }), content_type='application/json')