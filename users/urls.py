from django.urls import path, include

from users.views import UserAPIView, UserListAPIView, get_user_id, is_admin, is_authenticated

urlpatterns = [path("users/", UserListAPIView.as_view()),
               path("create-user/", UserAPIView.as_view()),
               path("user/<int:pk>", UserAPIView.as_view()),
               path("get-user-id/", get_user_id),
               path("is_admin/", is_admin),
               path("is_authenticated/", is_authenticated),
               path("auth/", include('djoser.urls')),
               ]
