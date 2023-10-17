from django.http.response import HttpResponse


def silent_sso_check(request):
    return HttpResponse("<html><body><script>parent.postMessage(location.href, location.origin)</script></body></html>")
