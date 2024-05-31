from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.home, name='home'),
    path('submit_measurements/<int:dress_id>/', views.submit_measurements, name='submit_measurements'),
    path('tailor_work/<int:tailor_id>/', views.tailor_work, name='tailor_work'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
]

# URL patterns to serve media files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)