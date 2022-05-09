from django.urls import path

from accounts.api.views import login, register, UserProfileEditView

urlpatterns = [
    path('login/', login, name="login"),
    path('register/', register, name="register"),
    path('edit-profile/', UserProfileEditView.as_view(), name="edit-profile"),
]
