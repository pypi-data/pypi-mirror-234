from django.http import JsonResponse
from django.urls import path


def profile(request):
    return JsonResponse({"email": request.user.email})


urlpatterns = [
    path("profile/", profile, name="profile"),
]
