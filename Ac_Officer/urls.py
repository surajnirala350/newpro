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
from django.urls import path
from django.views.generic import TemplateView, ListView

from Ac_Citizen.models import Complaint_Table
from Ac_Officer import views

urlpatterns = [
    path('off_home/',views.officer_home,name='off_home'),
    path('officer_login/', TemplateView.as_view(template_name='ac_officer/officer_login.html'), name='officer_login'),
    path('officer_register/', views.officer_register, name='officer_register'),
    path('delete_officer/', views.delete_officer, name='delete_officer'),
    path('update_officer/', views.update_officer, name='update_officer'),
    path('officeer_otp_check/',views.officer_otp_check,name='officer_otp_check'),


    # path('officer_login/', TemplateView.as_view(template_name='ac_officer/officer_login.html'), name='officer_login'),
    path('officer_logout/',views.officer_logout,name='officer_logout'),
    path('officer_login_check/', views.officer_login_check, name='officer_login_check'),

    # complaints url
    path('officer_complaints_list/',TemplateView.as_view(template_name='ac_officer/officer_complaints_index.html'),name='officer_complaints_list'),
    path('officer_pending_complaints/',views.officer_pending_complaints, name='officer_pending_complaints'),
    path('officer_assigned_complaints/',views.officer_assigned_complaints,name='officer_assigned_complaints'),
    path('closed_complaints/',views.closed_complaint,name='closed_complaints'),
    path('closed_complaints_list/',views.closed_complaints_list,name='closed_complaints_list'),

    # suggestion url
    path('officer_suggestions_list/',views.officer_suggestions,name='officer_suggestions_list'),

]

urlpatterns += (
    static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT))
