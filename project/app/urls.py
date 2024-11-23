from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.render_combined_charts, name='combined_charts'),
    path('customize', views.generate_custom_chart1_data, name='customize_chart'),  
] 
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)