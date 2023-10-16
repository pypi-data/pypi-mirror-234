=========
Y Message
=========

Purpose
-------
Ymessage is a Django app to implement **Transactional Outbox** pattern
(https://microservices.io/patterns/data/transactional-outbox.html).

Quick start
-----------

1. Add "ymessage" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...,
        "ymessage",
    ]

2. Include the ymessage URLconf in your project urls.py like this::

    path("", include("ymessage.urls")),

3. Run ``python manage.py migrate`` to create the ymessage models.

4. Create a ymessage_handlers module in your app. See ymessage_example for ymessage's usage.

5. POST http://127.0.0.1:8000/ymessage/default_message_handler/ to relay  or process the message.
6. 