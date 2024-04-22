from django.urls import path
from blog.views import home_view, follow, like, sighup_view, settings_view, upload_view, profile_view, search_view

urlpatterns = [
    path('', home_view),
    path('follow/', follow),
    path('like/', like),
    path('signup/', sighup_view),
    path('setting/', settings_view),
    path('upload', upload_view),
    path('search/', search_view),
    path('profile/<int:pk>', profile_view),
]