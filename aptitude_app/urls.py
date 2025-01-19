from django.urls import path 
from . import views

urlpatterns = [
    path('', views.index , name ='home'),
    path('test/',views.test, name ='test'),
    path('login/',views.login, name='login'),
    path('question_paper/<int:id>/preview/', views.question_paper_preview, name='question_paper_preview'),
]