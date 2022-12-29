from django.contrib import admin
from .models import Chat, Text, AnonymousUser

admin.site.register(Chat)
admin.site.register(Text)
admin.site.register(AnonymousUser)
