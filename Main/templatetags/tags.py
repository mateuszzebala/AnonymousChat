from django import template
from Main.models import AnonymousUser, Chat


register = template.Library()



@register.simple_tag
def number_of_active_users():
    i = 0
    chats = Chat.objects.all()
    for chat in chats:
        if chat.user1 is not None:
            i += 1
        if chat.user2 is not None:
            i += 1
    return i