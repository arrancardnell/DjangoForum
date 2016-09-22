from django.conf import settings
from django.db import models


class PrivateConversation(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name='pconvs_started')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 related_name='pconvs_received')
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ('owner', 'recipient', 'created',)
        get_latest_by = ('created')


class PrivateMessage(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name='pmsgs_sent')
    conversation = models.ForeignKey(PrivateConversation,
                                     related_name='pconv_messages')
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)