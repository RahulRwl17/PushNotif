from django.contrib import admin
from . import views
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path("Home/",views.Home, name="LocaterHome"),
    path("About/",views.About, name="LocaterAbout"),
    path("send_push",views.send_push,name="pusn_notif"),
    path('sw.js', TemplateView.as_view(template_name='sw.js', content_type='application/x-javascript'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)