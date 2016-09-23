from django.conf import settings
from django.db import models

from random import randint

def random_unique_id():
    # give conversations random ids so they can't easily be guessed
    existing_ids = PrivateConversation.objects.all().values_list('id', flat=True)
    unique_id = randint(100000, 999999)
    if unique_id not in existing_ids:
        return unique_id
    else:
        return random_unique_id()

class PrivateConversation(models.Model):
    id = models.IntegerField(default=random_unique_id,
                             unique=True,
                             primary_key=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name='pconvs_started')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 related_name='pconvs_received')
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def random_unique(self):
        return int(randint(10000, 99999))

    class Meta:
        get_latest_by = ('created')


class PrivateMessage(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name='pmsgs_sent')
    conversation = models.ForeignKey(PrivateConversation,
                                     related_name='pconv_messages')
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)