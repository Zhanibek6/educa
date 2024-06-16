from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register("courses", views.CourseViewSet)

app_name = "courses"

urlpatterns = [
    path("subjects/", views.SubjectListView.as_view(), name="subject_list"),
    path("subjects/<int:pk>/", views.SubjectDetailView.as_view(), name="subject_detail"),
    path("courses/<int:pk>/", views.CourseDetailView.as_view(), name="course_detail"),
    path('modules/<int:pk>/', views.ModuleDetailView.as_view(), name='module_list'),
    path('my-courses/', views.StudentCourseListView.as_view(), name="my_courses"),
    path('enroll/', views.StudentEnrollCourseView.as_view(), name='student-enroll-course'),
    path('courses/<int:course_pk>/unsubscribe/', views.UnsubscribeCourseAPIView.as_view(), name='unsubscribe_course'),
    path("", include(router.urls)),
]
