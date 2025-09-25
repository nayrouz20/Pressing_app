
from django.http import JsonResponse
from .models import BlacklistedToken

class CheckBlacklistMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if auth_header:
            token = auth_header.split()[1]
            if BlacklistedToken.objects.filter(token=token).exists():
                return JsonResponse({'error': 'Token is blacklisted'}, status=401)
        response = self.get_response(request)
        return response
