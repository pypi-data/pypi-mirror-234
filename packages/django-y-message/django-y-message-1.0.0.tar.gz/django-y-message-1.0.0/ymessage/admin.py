from django.contrib import admin

from .models import Message, MessageLog

class MessageLogInline(admin.StackedInline):
    model = MessageLog
    extra = 0

class MessageAdmin(admin.ModelAdmin):
    inlines = [MessageLogInline,]

admin.site.register(Message, MessageAdmin)