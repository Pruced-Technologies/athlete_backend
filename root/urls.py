from django.contrib import admin
from django.urls import include,path
from django.conf import settings
from django.conf.urls.static import static
# from football.views import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('football/', include('football.urls')),
    path('football/api/', include('football.api.urls')),
    # path('chat/', include('chat.urls')),
    path('api/auth/', include('social_accounts.urls'))
    # path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
