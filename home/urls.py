from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('add_review/', views.add_review, name='add_review'),
    path('edit_review/<int:review_id>/', views.edit_review, name='edit_review'),
    path('delete_review/<int:review_id>/',
         views.delete_review, name='delete_review'),
    path('approve_review/<int:review_id>/',
         views.approve_review, name='approve_review'),
    path('reviews/', views.all_reviews, name='all_reviews'),
]
