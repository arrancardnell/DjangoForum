from django.conf import settings
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.text import slugify

import datetime


class MemberManager(models.Manager):
    def get_queryset(self):
        return super(MemberManager,
                     self).get_queryset().filter(status='member')

class Section(models.Model):
    STATUS_CHOICES = (
        ('guest', 'Guest'),
        ('member', 'Member'),
        ('admin', 'Admin'),
    )
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=250,
                                   blank=True)
    slug = models.SlugField(max_length=250,
                            unique_for_date='created')
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=250,
                              choices=STATUS_CHOICES,
                              default='member')
    objects = models.Manager()
    members = MemberManager()

    class Meta:
        unique_together = ('title', 'status',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('forum:section_detail',
                       args=['self.slug'])


class Topic(models.Model):
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('hidden', 'Hidden'),
    )
    title = models.CharField(max_length=250,
                             unique=True)
    description = models.CharField(max_length=250,
                                   blank=True)
    slug = models.SlugField(max_length=250,
                            unique_for_date='created')
    created = models.DateTimeField(auto_now_add=True)
    section = models.ForeignKey(Section,
                                related_name='forum_topics')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name='forum_topics')
    status = models.CharField(max_length=250,
                              choices=STATUS_CHOICES,
                              default='open')

    class Meta:
        ordering = ['created']
        unique_together = ('title', 'section')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('forum:topic_detail',
                       args=['self.section.slug',
                             'self.slug'])

    def save(self, *args, **kwargs):
        super(Topic, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.title)
            self.save()


class Post(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('hidden', 'Hidden'),
    )
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                   related_name='posts_liked',
                                   blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='topic_posts')
    topic = models.ForeignKey(Topic,
                              related_name='topic_posts')
    status = models.CharField(max_length=250,
                             choices=STATUS_CHOICES,
                             default='active')

    class Meta:
        ordering = ['created']
        get_latest_by = ('created')

class Message(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='chat_messages')
    content = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.content


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)

    def last_seen(self):
        return cache.get('seen_{}'.format(self.user.username))

    def online(self):
        if self.last_seen():
            now = datetime.datetime.now()
            if now > self.last_seen() + datetime.timedelta(
                seconds=settings.USER_ONLINE_TIMEOUT):
                return False
            else:
                return True
        else:
            return False

class Inbox(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title