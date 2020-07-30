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

from Ac_Admin import views
from Ac_Citizen.models import Complaint_Table

urlpatterns = [
    # admin urls
    path('admin_login/', TemplateView.as_view(template_name='ac_admin/admin_login.html'), name='admin_login'),
    path('admin_home/',views.admin_home, name='admin_home'),
    path('admin_login_check/',views.admin_login_check, name='admin_login_check'),
    path('logout/',views.logout_view,name='admin_logout'),
    # path('contact_us/',TemplateView.as_view(template_name='ac_admin/contact_us.html'),name='contact_us'),

    # Department urls
    path('add_department/',views.add_department, name='admin_add_department'),
    path('update_department/',views.update_department, name='admin_update_department'),
    path('delete_department/', views.delete_department, name='admin_delete_department'),

    # complaints url
    path('admin_complaints_list/',views.admin_complaints_list,name='admin_complaints_list'),
    path('admin_pending_complaints/',views.admin_pending_complaints,name='admin_pending_complaints'),
    path('complaints_assign/',views.complaints_assign, name='complaints_assign'),
    path('assigned_complaints/',views.admin_assigned_complaints,name='assigned_complaints'),
    path('closed_complaints/',views.admin_closed_complaints,name='admin_closed_complaints'),

    # feedbacks urls
    path('admin_feedback_list/',views.admin_feedbacks_list,name='admin_feedback_list'),
    path('admin_feed_replay/',views.admin_feedback_replay,name='admin_feedback_replay'),
    path('delete_feedback/', views.delete_feedbacks, name='delete_feedback'),

    # admin suggestions urls
    path('admin_suggestions_list/',views.admin_suggestions_list,name='admin_suggestions_list'),

    # Contact Us Url
    path('contact_us/',views.contact_us,name='contact_us'),
    path('notification_list/',views.notification_list,name='notification_list'),
    path('delete_notification/',views.delete_notification,name='delete_notification'),

    path('about_us/',TemplateView.as_view(template_name='ac_admin/about_active_city.html'),name='about_us'),
]

urlpatterns += (
    static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT))
