from django.conf import settings

from .service import compose, message_handler, handle_message

def init():
    for app in settings.INSTALLED_APPS:
        try:
            __import__(app + '.ymessage_handlers')
        except ImportError:
            pass

init()