from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
channel = get_channel_layer()

# Create your models here.



class Desk(models.Model):
    code = models.CharField(max_length=16, null=False, blank=False)
    title = models.CharField(max_length=64, null=False, blank=False)
    waiter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} - {self.title}"


class Category(models.Model):
    title = models.CharField(max_length=64, null=False, blank=False)

    def __str__(self):
        return f"{self.title}"


class Item(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    title = models.CharField(max_length=64, null=False, blank=False)
    description = models.CharField(max_length=255, blank=True, null=True)
    price = models.IntegerField(null=True, blank=True)
    thumbnail = models.ImageField(null=True, blank=True)


class Requests(models.Model):
    desk = models.ForeignKey(Desk, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, editable=False)


@receiver(post_save, sender=Requests)
def send_notif(sender, instance, **kwargs):
    async_to_sync(channel.group_send)(instance.desk.code, {'type': 'request_waiter', 'code': instance.desk.code})
