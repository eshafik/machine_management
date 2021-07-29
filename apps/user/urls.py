from django.urls import path

from apps.user.views_internal import UserToken, UserRefreshToken

# Put here views here
urlpatterns = [
]

internal_urls = [
    path('token/', UserToken.as_view()),
    path('refresh-token/', UserRefreshToken.as_view()),
]

urlpatterns += internal_urls
