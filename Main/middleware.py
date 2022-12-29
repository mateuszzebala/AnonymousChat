from .models import AnonymousUser

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

class MainMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.session.get('AnonymousUserId') is None:
            user = AnonymousUser(name="", ip=get_client_ip(request))
            user.save()
            request.session['AnonymousUserId'] = user.id
            
        request.anon = AnonymousUser.objects.filter(id=request.session.get('AnonymousUserId')).first()

        response = self.get_response(request)
        return response