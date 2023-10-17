from django.urls import path

from . import views

app_name: str = "hunting"

urlpatterns = [
    path("", views.index, name="index"),
    path('char/add', views.add_char, name="add_char"),
    path('target/<int:target_id>/', views.target_details, name='target_details'),
    path('alt/<int:alt_id>/', views.alt_details, name='alt_details'),
    path('ajax/locate_history', views.locate_history, name='locate_history'),

]
