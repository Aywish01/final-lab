from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('HR/', include('HR.urls')),  # Assuming your HR app has its own urls.py
    path('', TemplateView.as_view(template_name='HR/home.html'), name='home'),
   
    # Other paths...
]
