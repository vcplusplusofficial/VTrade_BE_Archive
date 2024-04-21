from django.urls import path
from .views import *

urlpatterns = [
    path("get_user/", get_user, name="get_user"),
    path("add_user/", add_user, name="add_user"),
    path("forgot_password/", forgot_password, name="forgot_password"),
    path("reset_password/", reset_password, name="reset_password"),
    path("update_user/<int:user_id>/", update_user, name="update_user"),
    path("remove_user/<int:user_id>/", remove_user, name="remove_user"),
]
