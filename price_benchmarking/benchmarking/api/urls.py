import django.urls

from . import views

app_name = 'accounts_api'
urlpatterns = [
    django.urls.path('benchmarking/upload-user-rates/', views.UploadUserRatesAPIView.as_view(), name='upload_user_rates'),
    django.urls.path('benchmarking/user-potential-savings/', views.UserPotentialSavingAPIVIew.as_view(), name='user_potential_savings'),
]