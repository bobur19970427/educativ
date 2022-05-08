from django.urls import path

from accounts.api.views import login, register, UserProfileEditView

urlpatterns = [
    path('login/', login, name="login"),
    path('register/', register, name="register"),
    path('edit-profile/<int:value_from_url>', UserProfileEditView.as_view(), name="edit-profile"),
]
