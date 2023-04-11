from django.urls import path

from .views import Login, TwoFactor, Dashboard


urlpatterns = [
    path("login/", Login.as_view(), name="login"),
    path(r"two_factor/<str:token>/", TwoFactor.as_view(), name="two_factor"),
    path("dashboard/", Dashboard.as_view(), name="dashboard"),
]
