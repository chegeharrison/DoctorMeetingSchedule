from django.urls import path
from .views import home, admin_login,admin_logout,doctor_page,meeting_manager,save_meeting,checkout,dashboard,edit_profile,edit_delete,meeting_history

urlpatterns = [
    path('',home, name='home'),
    path('login/',admin_login, name='login' ),
    path('logout/', admin_logout, name='logout'),
    path('doctor/', doctor_page, name='doctor'),
    path('dashboard/', dashboard, name='dashboard'),

    path('dashboard/meeting_manager/', meeting_manager, name='meeting_manager'),
    path('dashboard/save_meeting/', save_meeting, name='save_meeting'),
    path('meeting_history/', meeting_history, name='meeting_history'),


    path('dashboard/checkout/', checkout, name='checkout'),
    path('dashboard/profile_manager/', dashboard, name='profile_manager'),
    path('dashboard/edit_profile/', edit_profile, name='edit_profile'),
    path('dashboard/edit_delete/', edit_delete, name='edit_delete'),
    

]
