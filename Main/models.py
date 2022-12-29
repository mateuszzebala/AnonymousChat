from django.db import models
from django.contrib.auth.models import User
import datetime


class AnonymousUser(models.Model):
    name = models.CharField(max_length=32)
    ip = models.CharField(max_length=32, default="")
    active = models.BooleanField(default=True)
    def __str__(self) -> str:
        return f"{self.id} {self.name}"

class Chat(models.Model):
    user1 = models.ForeignKey(AnonymousUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="user1")
    user2 = models.ForeignKey(AnonymousUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="user2")
    user1_typeing = models.BooleanField(default=False)
    user2_typeing = models.BooleanField(default=False)
    datetime = models.DateTimeField(auto_now_add=True, null=True)
    disconnected = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user1} vs {self.user2}"
    
    def is_connected(self):
        return self.user1 is not None and self.user2 is not None

class Text(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    user = models.ForeignKey(AnonymousUser, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField(default="")