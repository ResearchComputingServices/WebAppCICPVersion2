from django.urls import path,include
from WebsiteApp import views

urlpatterns = [
    path('',views.report_results_EN, name='report_results_EN'),
    path('home',views.landingPageView, name='landingPageView'),
    path('theme',views.landingPageView, name='themereports'),
    path('date',views.landingPageView, name='datereports'),
    # path("select2/", include("django_select2.urls")),
    
]
