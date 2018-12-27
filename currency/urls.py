from django.urls import path
from currency import views

urlpatterns = [
                path('currency/', views.CurrencyConvert.as_view()),
            ]