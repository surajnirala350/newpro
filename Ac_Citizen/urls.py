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

from Ac_Citizen import views

urlpatterns = [
    path('citizen_home',TemplateView.as_view(template_name='ac_citizen/citizen_index.html'),name='citizen_home'),
    path('citizen_login/',TemplateView.as_view(template_name='ac_citizen/citizen_login.html'),name='citizen_login'),
    path('citizen_logout/', views.citizen_logout, name='citizen_logout'),
    path('citizen/', views.citizen_login, name='citizen'),
    path('citizen_register/', views.citizen_registration, name='register'),
    path('citizen_otp_check/',views.citizen_otp_check,name='citizen_otp_check'),

    # Complaints urls
    path('complaints/', views.complaints_view, name='complaints'),
    path('view_complaints_status/',views.view_complaints_status,name='view_complaints_status'),

    path('delete_complaints/', views.delete_complaints, name='delete_complaints'),

    # feedback urls
    path('feedback/', views.feedback_view, name='feedback'),
    # path('feedback_list/', views.feedbacks_list, name='feedback_list'),


    path('replay_list/',views.feedbacks_list,name='replay_list'),
    path('citizen_replay_list/',views.citizen_replay_list,name='citizen_replay_list'),
    path('citizen_suggestion/',views.citizen_suggestion_view,name='citizen_suggestion'),



]

urlpatterns += (
    static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT))
