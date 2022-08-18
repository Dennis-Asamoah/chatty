from django.db import models
from  django.contrib.auth.models import AbstractUser
from django.db.models import Max


# Create your models here.
class User(AbstractUser):
    name  = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username+self.email


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='user',null=True)
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='sender', null=True)
    receipient = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='receipient', null=True)
    date  = models.DateTimeField(auto_now_add=True)
    body = models.TextField(null=True, blank=True)
    is_read = models.BooleanField(default=False)

    def send_message(sender, receipient, msg):
        sent_by  = Message(
            user=sender,
            sender=sender,
            receipient=receipient,
            body=msg, 
            is_read=True
        )
        sent_by.save()

        sent_to = Message(
            user=receipient,
            sender=sender,
            receipient=sender,
            is_read=True
        )
        sent_to.save()
    
    def get_message(user):
        users = []
        messages = Message.objects.filter(user=user).values('receipient').annotate(last=Max('date'))\
            .order_by('-date')
        for message in messages:
            users.append(
                {
                'user': User.objects.get(id=message['receipient']),
                'last': message['last'],
                'unread': Message.objects.filter(user=user, receipient__id=message['receipient'], \
                    is_read=False).count()
                }
            )
            return users

     