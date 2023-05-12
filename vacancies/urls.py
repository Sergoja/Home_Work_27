from django.urls import path

import vacancies.views

urlpatterns = [
    path('', vacancies.views.VacancyListView.as_view()),
    path('<int:pk>', vacancies.views.VacancyDetailView.as_view()),
    path('create/', vacancies.views.VacancyCreateView.as_view()),
    path('<int:pk>/update/', vacancies.views.VacancyUpdateView.as_view()),
    path('<int:pk>/delete/', vacancies.views.VacancyDeleteView.as_view()),
    path('by_user/', vacancies.views.UserVacancyDetailView.as_view())
]