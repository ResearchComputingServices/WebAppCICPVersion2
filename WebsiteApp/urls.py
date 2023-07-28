from django.urls import path,include
from WebsiteApp import views

urlpatterns = [
    path('',views.landingPageView, name='landingPageView'),
    path('latestreport',views.latest_report, name='latest_report'),
    path('theme',views.landingPageView, name='themereports'),
    path('date',views.landingPageView, name='datereports'),
    path('print',views.printReport,name="printreport"),
    
]
