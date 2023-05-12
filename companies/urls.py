from django.urls import path

import companies.views

urlpatterns = [
    path('<pk>/image/', companies.views.CompanyImageView.as_view()),
]