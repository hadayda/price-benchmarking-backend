import django.urls

from . import views

app_name = 'accounts_api'
urlpatterns = [
    django.urls.path('auth/login/', views.LoginAPIView.as_view(), name='login'),
]