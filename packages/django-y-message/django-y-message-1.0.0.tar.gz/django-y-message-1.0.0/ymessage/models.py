from django.db import models

from ool import VersionField, VersionedMixin

class Message(VersionedMixin, models.Model):
    STATUS_QUEUING = 'queuing'
    STATUS_PROCESSING = 'processing'
    STATUS_SENT = 'sent'
    STATUS_EXCEPTION = 'exception'
    STATUS_NO_HANDLER = 'no_handler'
    STATUS_CHOICE = (
        (STATUS_QUEUING, STATUS_QUEUING),
        (STATUS_PROCESSING, STATUS_PROCESSING),
        (STATUS_SENT, STATUS_SENT),
        (STATUS_EXCEPTION, STATUS_EXCEPTION),
        (STATUS_NO_HANDLER, STATUS_NO_HANDLER),
    )
    id = models.UUIDField(primary_key=True)
    type = models.CharField(max_length=50)
    content = models.JSONField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICE, default=STATUS_QUEUING)
    update_at = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)
    version = VersionField()

    class Meta:
        get_latest_by = 'create_at'
        ordering = ('-create_at',)
        indexes = [
            models.Index(fields=["create_at"], name='idx_message__create_at'),
        ]

    def log(self, content):
        return MessageLog.objects.create(content=content, message=self)


    def begin_processing(self):
        self.status = Message.STATUS_PROCESSING
        self.save()


    def sent(self):
        self.status = self.STATUS_SENT
        self.save()

    def catch_exception(self, reason):
        self.log({
            'exception': reason
        })
        self.status = self.STATUS_EXCEPTION
        self.save()

    def no_handler(self):
        self.status = self.STATUS_NO_HANDLER
        self.save()

    def is_processing(self):
        return self.status == self.STATUS_PROCESSING

    def __str__(self):
        return f"{self.create_at} {self.type}:{self.id} {self.status}"


class MessageLog(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    content = models.JSONField(null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('id', )