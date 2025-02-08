from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from . forms import CustomPasswordChangeForm


urlpatterns = [
    path('',views.index, name='index'),
    path('change_password/', auth_views.PasswordChangeView.as_view(
        template_name='index_files/change_password.html', 
        success_url='/',
    ), name='change_password'),
    path('signup/', views.signup, name='signup'),
    path('login/',auth_views.LoginView.as_view(template_name = 'index_files/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name = 'index_files/logout.html'), name='logout'),
    path('notice/<str:paper_code>/', views.notice, name='notice'),
    path('test/<str:paper_code>/', views.test, name='test'),
    path('result/<str:paper_code>/', views.result, name='result'),
]
