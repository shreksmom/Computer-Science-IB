from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='login.html',next_page="inventory"), name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('inventory/', views.inventory, name='inventory'),
    path('add-equipment/', views.add_equipment, name='add_equipment'),
    path('delete-equipment/<int:equipment_id>/', views.delete_equipment, name='delete_equipment'),
    path('ai-experiment/', views.ai_experiment_view, name='ai_experiment'),
    path('ai-experiment/<int:conversation_id>/', views.ai_experiment_view, name='ai_experiment_detail'),
    path('ai-experiment/<int:conversation_id>/send-message/', views.send_message, name='send_message'),
    path('ai-experiment/add-conversation/', views.add_conversation, name='add_conversation'),
    path('ai-experiment/<int:conversation_id>/delete/', views.delete_conversation, name='delete_conversation'),
]