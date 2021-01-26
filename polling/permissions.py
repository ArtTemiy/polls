from django.contrib.auth import authenticate
from django.http import JsonResponse, HttpResponseForbidden


def has_permition(func):
    # args: self, request, ...
    def wrapper(*args, **kwargs):
        request = args[1]

        username, password = request.GET.get('username', None), request.GET.get('password', None)
        if not (username and password):
            return HttpResponseForbidden()
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            return func(*args, **kwargs)
        return JsonResponse({
                "detail": "Permission denied"
            },
            status=403
        )
    return wrapper