from django.urls import path

from . import views

app_name = "oauth2"

urlpatterns = [
    path(
        "/oauth2/redirect-params",
        views.OAuthRedirectsParamsView,
        name="redirect-params",
    ),
]
