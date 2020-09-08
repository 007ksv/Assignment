"""Leave_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from . import settings
from user_handling import views as user_handling_view
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user_handling_view.register, name='register'),
    path('login/', user_handling_view.login, name='login'),
    path('profile/', user_handling_view.profile, name='profile'),
    path('logout/', user_handling_view.logout, name='logout'),
    path('leave_application/<str:usrname>/', user_handling_view.leave_application, name='leave_application'),
    path('employee_dashboard/', user_handling_view.employee_dashborad, name='employee_dashboard'),
    path('home', user_handling_view.home, name='home'),
    path('manager_dashboard/', user_handling_view.manager_dashboard, name='manager_dashboard'),
    path('handle_app_staadmintus/<int:id>/', user_handling_view.handle_app_status, name='handle_app_status'),
    path('admin_dashboard/', user_handling_view.admin_dashboard, name='admin_dashboard'),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)