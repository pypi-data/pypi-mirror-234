import traceback
import ool

all_handlers = {}

types_for_all_handlers = []

def add_handler(type, handler):
    all_handlers[type] = handler
    types_for_all_handlers.append(type)


def message_handler(type):
    def add_handler_of_type(func):
        add_handler(type, func)
        return func 
    return add_handler_of_type


def compose(type, id, content=None):
    from .models import Message
    return Message.objects.create(type=type,
                                  id=id,
                                  content=content,
                                  status=Message.STATUS_QUEUING)


class NoMoreMessages(Exception):
    pass


def get_next_message_for_processing(types):
    from .models import Message

    message = None
    while message is None:
        message = Message.objects.filter(status=Message.STATUS_QUEUING, type__in=types).order_by('create_at').first()
        if message is not None:
            try:
                message.begin_processing()
            except ool.ConcurrentUpdate:
                message = None
        else:
            raise NoMoreMessages()
    return message


def handle_message():
    message = get_next_message_for_processing(types_for_all_handlers)
    try:
        handler = all_handlers.get(message.type, None)
        if handler == None:
            message.no_handler()
        else:
            handler(message)
    except:
        message.catch_exception({
            'trace': traceback.format_exc()
        })

        
