
from django.urls import path
from . import views, admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   path('', views.index, name="home"),
   path('register/', views.register, name='register'),
   path('logout/', auth_views.LogoutView.as_view(), name='logout'),
   path('login/', views.login_view, name='login'),
   path('profile/', views.profile, name='profile'),  # Путь для отображения профиля
   path('edit_profile/', views.edit_profile, name='edit_profile'),  # Путь для редактирования профиля
   path('delete_profile/', views.delete_profile, name='delete_profile'),
   path('polls/', views.poll_list, name='poll_list'),  # Список голосований
   path('polls/<int:poll_id>/', views.poll_detail, name='poll_detail'),  # Страница конкретного голосования
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)