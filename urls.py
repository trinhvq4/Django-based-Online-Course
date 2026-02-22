from django.urls import path
from . import views

# Setting the application namespace so you can use 'onlinecourse:submit' in templates and views
app_name = 'onlinecourse'

urlpatterns = [
    # (Assuming you already have paths for your index and course details)
    # path('', views.course_list, name='index'),
    # path('<int:course_id>/', views.course_details, name='course_details'),

    # Route for submitting the exam
    # Example URL: /onlinecourse/5/submit/
    path('<int:course_id>/submit/', views.submit, name='submit'),

    # Route for showing the exam result
    # Example URL: /onlinecourse/5/submission/12/
    path('<int:course_id>/submission/<int:submission_id>/', views.show_exam_result, name='show_exam_result'),
]
