from django.urls import path
from WebsiteApp import views

urlpatterns = [
    path('',views.report_results_EN, name='report_results_en'),
]
