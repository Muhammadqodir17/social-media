from django.urls import path
from blog.views import home_view, follow, like

urlpatterns = [
    path('', home_view),
    path('follow/', follow),
    path('like/', like),
]