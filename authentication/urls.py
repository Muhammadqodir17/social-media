from django.conf.urls.static import static
from django.urls import path

from config import settings
from config.settings import STATIC_ROOT, MEDIA_ROOT
from .views import login_view, logout_view

urlpatterns = [
    path('login/', login_view),
    path('logout/', logout_view),

]

urlpatterns += static(settings.STATIC_URL, document_root=STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=MEDIA_ROOT)