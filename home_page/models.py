from django.contrib.auth.models import User
from django.db import models
# from django.contrib.auth import get_user_model
from django.utils import timezone


class Comment(models.Model):
    id_image = models.IntegerField(verbose_name='id image')
    user = models.ForeignKey(User, verbose_name='author')
    text = models.TextField(verbose_name='comment', max_length=512)
    history = models.TextField(verbose_name='history', max_length=4096, blank=True)
    created_at = models.DateTimeField(verbose_name='created at', default=timezone.now, editable=False)
    updated_at = models.DateTimeField(verbose_name='updated at', default=timezone.now)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Comment for image'
        verbose_name_plural = 'Comments for image'


class Like(models.Model):
    id_image = models.IntegerField(verbose_name='id image')
    user = models.ForeignKey(User, verbose_name='author')

    class Meta:
        verbose_name = 'Like for image'
        verbose_name_plural = 'Likes for image'
