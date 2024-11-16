from django.contrib import admin
import django.urls

urlpatterns = [
    django.urls.path('admin/', admin.site.urls),
    django.urls.path('api/v1/', django.urls.include(('price_benchmarking.accounts.api.urls', 'accounts_api'), namespace='accounts_api_v1')),
    django.urls.path('api/v1/', django.urls.include(('price_benchmarking.benchmarking.api.urls', 'benchmarking_api'), namespace='benchmarking_v1'))
]
