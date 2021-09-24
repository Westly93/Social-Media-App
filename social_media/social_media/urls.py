from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from users.views import UserProfileView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('landing.urls')),
    path('post/', include('post.urls')),
    path('accounts/', include('users.urls')),
    path('accounts/profile/', UserProfileView.as_view(), name= 'profile'),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)