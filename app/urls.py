from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='home'),  # Homepage shows login
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    # Notes CRUD
    path('notes/', views.note_list, name='note_list'),
    path('notes/create/', views.create_note, name='create_note'),
    path('notes/<int:pk>/edit/', views.update_note, name='update_note'),
    path('notes/<int:pk>/delete/', views.delete_note, name='delete_note'),
]
