from django.db import models

class Section(models.Model):
    STATUS_CHOICES = (
        ('guest', 'Guest')
        ('member', 'Member'),
        ('admin', 'Admin')
    )
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='created')
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=250,
                              choices=STATUS_CHOICES,
                              default='member')

    def __str__(self):
        return self.title