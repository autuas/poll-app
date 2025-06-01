from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
    path('', views.poll_list, name='poll_list'),
    path('<int:pk>/', views.poll_detail, name='poll_detail'),
    path('<int:pk>/poll_vote/', views.poll_vote, name='poll_vote'),
    path('poll_create/', views.poll_create, name='poll_create'),
    path('<int:pk>/poll_delete/', views.poll_delete, name='poll_delete'),
    path('<int:pk>/poll_end/', views.poll_end, name='poll_end'),
    path('<int:poll_id>/poll_add_choice/', views.poll_add_choice, name='poll_add_choice'),
    path("poll_search/", views.poll_sql_search_form, name="poll_sql_search_form"),
    path("poll_search/results/", views.poll_search_results, name="poll_search_results"),
]
