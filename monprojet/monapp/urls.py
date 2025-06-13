from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('services/', views.services_list, name='services_list'),
    path('services/new/', views.services_create, name='services_create'),
    path('services/<int:pk>/edit/', views.services_update, name='services_update'),
    path('services/<int:pk>/delete/', views.services_delete, name='services_delete'),
    path('services/affiche/', views.services_affiche, name='services_affiche'),

    path('applications/', views.applications_list, name='applications_list'),
    path('applications/new/', views.applications_create, name='applications_create'),
    path('applications/<int:pk>/edit/', views.applications_update, name='applications_update'),
    path('applications/<int:pk>/delete/', views.applications_delete, name='applications_delete'),
    path('applications/affiche/', views.applications_affiche, name='applications_affiche'),
    path('applications/import/', views.import_applications, name='import_application'),

    path('usageressources/', views.usageressource_list, name='usageressource_list'),
    path('usageressources/new/', views.usageressource_create, name='usageressource_create'),
    path('usageressources/<int:pk>/edit/', views.usageressource_update, name='usageressource_update'),
    path('usageressources/<int:pk>/delete/', views.usageressource_delete, name='usageressource_delete'),
    path('usageressource/affiche/', views.usageressource_affiche, name='usageressource_affiche'),

    path('serveurs/', views.serveurs_list, name='serveurs_list'),
    path('serveurs/new/', views.serveurs_create, name='serveurs_create'),
    path('serveurs/<int:pk>/edit/', views.serveurs_update, name='serveurs_update'),
    path('serveurs/<int:pk>/delete/', views.serveurs_delete, name='serveurs_delete'),
    path('serveurs/affiche/', views.serveurs_affiche, name='serveurs_affiche'),

    path('type_de_serveurs/', views.type_de_serveurs_list, name='type_de_serveurs_list'),
    path('type_de_serveurs/new/', views.type_de_serveurs_create, name='type_de_serveurs_create'),
    path('type_de_serveurs/<int:pk>/edit/', views.type_de_serveurs_update, name='type_de_serveurs_update'),
    path('type_de_serveurs/<int:pk>/delete/', views.type_de_serveurs_delete, name='type_de_serveurs_delete'),

    path('utilisateurs/', views.utilisateurs_list, name='utilisateurs_list'),
    path('utilisateurs/new/', views.utilisateurs_create, name='utilisateurs_create'),
    path('utilisateurs/<int:pk>/edit/', views.utilisateurs_update, name='utilisateurs_update'),
    path('utilisateurs/<int:pk>/delete/', views.utilisateurs_delete, name='utilisateurs_delete'),
]

