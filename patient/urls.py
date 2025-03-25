
from django.urls import path, include,re_path  
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),


    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path("register/", views.register, name="register"),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'), # Redirect to home page after logout

    path('profile/', views.profile, name='profile'),

    path('patient_profile/edit/', views.Patient_profile_edit, name='patient_profile_edit'),
    path('patient_profile/edit/<str:field>/', views.edit_patient_info, name='edit_patient_info'), 

    path('doctor_profile/edit/', views.doctor_profile_edit, name='doctor_profile_edit'),
    path('doctor_profile/edit/<str:field>/', views.edit_doctor_info, name='edit_doctor_info'),

    path("doctor_profile/photo/", views.update_profile_photo, name="update_profile_photo"),
    
    path('book_appointment/', views.book_appointment, name='book_appointment'),
    path('appointments/', views.patient_appointments, name='patient_appointments'),

    path("patientinformation/", views.patientinformation, name="patientinformation"),
    path("patientlist/", views.patientlist, name="patientlist"),

    path("doctorinformation/", views.doctorinformation, name="doctorinformation"),
    path("doctorlist/", views.doctorlist, name="doctorlist"),

    path("doctorlist/delete/<int:pk>", views.doctor_delete, name="doctor_delete"),
    path("patientlist/delete/<int:pk>", views.patient_delete, name="patient_delete"),
    path("hospitallist/delete/<int:pk>", views.hospital_delete, name="hospital_delete"),


    path('patientlist/update/<int:pk>', views.PatientUpdate.as_view(), name='patientlist_update'),
    path('doctorlist/update/<int:pk>', views.DoctorUpdate.as_view(), name='doctorlist_update'),
    path('hospitallist/update/<int:pk>', views.HospitalUpdate.as_view(), name='hospitallist_update'),


    path("hospitalinformation/", views.hospitalinformation, name="hospitalinformation"),
    path("hospitallist/", views.hospitallist, name="hospitallist"),

    path('appointment/', views.appointment_list, name='appointment_list'),
    
    path('update/<int:pk>/', views.appointment_update, name='appointment_update'),
    path('delete/<int:pk>/', views.appointment_delete, name='appointment_delete'),

    path('doctor_login/', auth_views.LoginView.as_view(template_name='registration/doctor_login.html'), name='doctor_login'),
    path("doctor_register/", views.register, name="doctor_register"),

    path('doctor_appointment_view/', views.doctor_appointment_view, name='doctor_appointment_view'),
    path('mes_rendezvous/', views.doctor_pending_appointments, name='doctor_pending_appointments'),
    path('rendezvous/<int:pk>/<str:action>/', views.update_appointment_status, name='update_appointment_status'),
    path('notifications/', views.notifications_list, name='notifications_list'),
    path('notifications/delete/<int:pk>/', views.delete_notification, name='delete_notification'),
    path('appointment/<int:appointment_id>/dossier/', views.view_patient_dossier, name='view_patient_dossier'),

    
]