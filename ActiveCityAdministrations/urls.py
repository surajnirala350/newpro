"""ActiveCityAdministrations URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from Ac_Admin import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('index/',TemplateView.as_view(template_name='main_index.html'),name='index'),
    path('index/',views.display_feedbacks,name='index'),
    path('',views.display_feedbacks,name='index'),

    # Application urls
    path('Ac_Admin/', include('Ac_Admin.urls')),
    path('Ac_Citizen/', include('Ac_Citizen.urls')),
    path('Ac_Ngo/', include('Ac_Ngo.urls')),
    path('Ac_Officer/', include('Ac_Officer.urls')),

]

urlpatterns += (
    static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT))
