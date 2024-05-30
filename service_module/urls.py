from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('search-lessons', views.SearchLessonsPageView.as_view(), name='search_lessons'),
    path('search-query', views.search_lessons_queries, name='search_query'),
    path('change-semester', views.change_semester, name='change_semester'),
    path('change-semester-to-default', views.change_semester_to_default, name='change_semester_to_default'),

    path('select-unit', views.SelectUnitPage.as_view(), name='select_unit'),
    path('search-query-units', views.select_unit_search_lessons_queries, name='search_query_units'),

    path('select-unit-action', views.select_unit_action, name='select_unit_action'),
    path('remove-unit-action', views.remove_unit_action, name='remove_unit_action'),

    # ZarinPal Payment
    path('request-payment/', views.send_request, name='request_payment'),
    path('verify-payment/', views.verify, name='verify_payment'),

    path('send-bill', views.task_issuance_variable_tuition_billing, name='task_issuance_variable_billing'),

]
