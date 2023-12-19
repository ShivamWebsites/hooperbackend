from django.db import models
# from chatapp.models import GroupMessage
from authentication.models import CustomUser

class GroupMessage(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='group_messages_sent')
    message = models.CharField(max_length=1000, null=False, blank=False, default=None)
    is_seen = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.sender.username}: {self.message}'
    

class PlayerInformation(models.Model):
    user= models.ForeignKey(GroupMessage, on_delete=models.CASCADE, related_name='group_messages_sent')
    height=models.IntegerField(default=0.0)
    weight=models.IntegerField(default=0.0)


