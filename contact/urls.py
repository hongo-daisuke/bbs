from django.urls import path
from . import views

app_name = 'contact'

urlpatterns = [
    path('', views.ContactHomeView.as_view(), name='home'),
    path('confirm/', views.ContactConfirmView.as_view(), name='confirm'),
    path('complete/', views.ContactCompleteView.as_view(), name='complete'),
]
