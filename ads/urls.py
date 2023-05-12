from django.urls import path

import ads.views

urlpatterns = [
    path('cat/', ads.views.CategoryView.as_view()),
    path('ad/', ads.views.AdView.as_view()),
    path('cat/<int:pk>', ads.views.CategoryDetailView.as_view()),
    path('ad/<int:pk>', ads.views.AdsDetailView.as_view())
]
