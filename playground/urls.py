from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # Home page
    path('', views.home, name='home'),

    # Login page
    path('login/', views.login, name='login'),

    # Register page
    path('register/', views.register, name='register'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Logout
    path('logout/', views.logout_view, name='logout'),

    # ==========================
    # Student Profile
    # ==========================
    path('profile/', views.profile, name='profile'),

    # ==========================
    # Courses
    # ==========================
    path('courses/', views.courses, name='courses'),

    path('enroll/<int:course_id>/',
         views.enroll,
         name='enroll'),

    path('my-courses/',
         views.my_courses,
         name='my_courses'),

    path('course/<int:course_id>/',
         views.course_detail,
         name='course_detail'),

    # ==========================
    # Assignments
    # ==========================
    path(
        'course/<int:course_id>/assignments/',
        views.assignments,
        name='assignments'
    ),

    path(
    "teacher/add-course/",
    views.teacher_add_course,
    name="teacher_add_course"
),

]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )