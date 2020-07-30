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
from django.views.generic import TemplateView, ListView

from Ac_Ngo import views
from Ac_Ngo.models import Suggestion_Table

urlpatterns = [
    # ngos urls
    path('ngo_home/',views.article_home,name='ngo_home'),
    path('ngo_login/', TemplateView.as_view(template_name='ac_ngo/ngo_login.html'), name='ngo_login'),
    path('ngo_login_check/', views.ngo_login_check, name='ngo_login_check'),
    path('ngo_register/', views.ngo_registration,name='ngo_register'),
    path('update_ngos/', views.update_ngos, name='update_ngos'),
    path('delete_ngos/', views.delete_ngos, name='delete_ngos'),
    path('ngo_logout/',views.ngo_logout,name='ngo_logout'),

    #suggestions urls
    path('suggestion/', views.ngo_suggestion_view, name='suggestion'),
    path('suggestions_list/',views.suggestions_list, name='suggestions_list'),
    path('delete_suggestions/', views.delete_suggestions, name='delete_suggestions'),

    # Article urls
    path('ngo_article/',views.ngo_article,name='ngo_article'),


]

urlpatterns += (
    static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT))
