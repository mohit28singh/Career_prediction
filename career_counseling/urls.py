from django.contrib import admin
from django.urls import path, include
from careers import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage),
    path('course/', views.course, name='course'),
    path('services/', views.careerprediction, name='careerprediction'),
    path('about/', views.about, name='about'),
    path('signup/', views.SignUpPage, name='signup'),
    path('login/', views.LoginPage, name='login'),
    path('accounts/login/', views.LoginPage, name='login'),
    path('accounts/logout/', views.LogoutPage, name='logout'),
    path('contact/', views.contact, name='contact'),
    path('home/', views.home, name='home'),
    path('logout/', views.LogoutPage, name='logout'),
    path('knowledge/', views.knowledge, name='knowledge'),
    path('AIML/', views.AIML, name='AIML'),
     path('API/', views.APIs, name='API'),
    path('PenTest/', views.PenTest, name='PenTest'),
     path('AppSup/', views.AppSupport, name='Support'),
    path('BusinessAnalyst/', views.Business, name='Analyst'),
    path('CustomerService/', views.Customer_service_executive, name='CSA'),
    path('CyberSecurity/', views.Cyber_Security, name='CSS'),
    path('DataBAse/', views.Databaseadmin, name='DBA'),
     path('Datascien/', views.Datasci, name='DScience'),
    path('HardwareEngineer/', views.Hardware_Engineer, name='HardEngin'),
     path('Helpdesk/', views.Helpdesk_Engineer, name='Helpdesk'),
     path('InformationSecurity/', views.Information_security, name='infosec'),
    path('Network/', views.Networking_engineer, name='neten'),
    path('PrjMan/', views.Project_Manager, name='projman'),
    path('Softdev/', views.Software_developer, name='softdev'),
    path('Softtester/', views.Software_tester, name='softtes'),
    path('TechnicalWriter/', views.Technical_wri, name='TW'),
    path('GraphicDesigner/', views.Graphic_Designer, name='GD'),
    path('TermsCondition/', views.TermsConditons, name='Terms'),
]

# Redirecting to login page if user not authenticated
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]

