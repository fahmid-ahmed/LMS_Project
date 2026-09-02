from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required

from .models import (
    StudentProfile,
    Course,
    Enrollment,
    LearningMaterial,
    Assignment,
    AssignmentSubmission
)


# ==========================================
# Home Page
# ==========================================
def home(request):
    return render(request, "home.html")


# ==========================================
# Login
# ==========================================
def login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            auth_login(request, user)

            messages.success(request, "Login Successful!")

            return redirect("dashboard")

        else:

            messages.error(request, "Invalid Username or Password!")

            return redirect("login")

    return render(request, "login.html")


# ==========================================
# Register
# ==========================================
def register(request):

    if request.method == "POST":

        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():

            messages.error(request, "Username already exists!")

            return redirect("register")

        if User.objects.filter(email=email).exists():

            messages.error(request, "Email already exists!")

            return redirect("register")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.first_name = full_name
        user.save()

        messages.success(request, "Registration Successful!")

        return redirect("login")

    return render(request, "register.html")


# ==========================================
# Dashboard
# ==========================================
@login_required
def dashboard(request):

    profile = StudentProfile.objects.filter(
        user=request.user
    ).first()

    return render(
        request,
        "dashboard.html",
        {
            "profile": profile
        }
    )


# ==========================================
# Student Profile
# ==========================================
@login_required
def profile(request):

    profile = StudentProfile.objects.filter(
        user=request.user
    ).first()

    if request.method == "POST":

        student_id = request.POST.get("student_id")
        department = request.POST.get("department")
        semester = request.POST.get("semester")
        phone = request.POST.get("phone")

        if profile:

            profile.student_id = student_id
            profile.department = department
            profile.semester = semester
            profile.phone = phone
            profile.save()

        else:

            profile = StudentProfile.objects.create(
                user=request.user,
                student_id=student_id,
                department=department,
                semester=semester,
                phone=phone
            )

        messages.success(request, "Profile saved successfully!")

        return redirect("dashboard")

    return render(
        request,
        "profile.html",
        {
            "profile": profile
        }
    )
    
# ==========================================
# Courses Page
# ==========================================

@login_required
def courses(request):

    # Fetch all courses from the database
    courses = Course.objects.all()

    return render(
        request,
        "courses.html",
        {
            "courses": courses
        }
    )
    
# ==========================================
# Enroll in Course
# ==========================================

@login_required
def enroll(request, course_id):

    # Find the selected course
    course = Course.objects.get(id=course_id)

    # Check if the student is already enrolled
    already_enrolled = Enrollment.objects.filter(
        student=request.user,
        course=course
    ).exists()

    if already_enrolled:

        messages.warning(
            request,
            "You are already enrolled in this course."
        )

    else:

        Enrollment.objects.create(
            student=request.user,
            course=course
        )

        messages.success(
            request,
            "Course enrolled successfully!"
        )

    return redirect("courses")

# ==========================================
# My Courses
# ==========================================

@login_required
def my_courses(request):

    # Get only the logged-in student's enrollments
    enrollments = Enrollment.objects.filter(
        student=request.user
    )

    return render(
        request,
        "my_courses.html",
        {
            "enrollments": enrollments
        }
    )

# ==========================================
# Course Details
# ==========================================

@login_required
def course_detail(request, course_id):

    # Get selected course
    course = Course.objects.get(id=course_id)

    # Get all materials of this course
    materials = LearningMaterial.objects.filter(
        course=course
    )

    return render(
        request,
        "course_detail.html",
        {
            "course": course,
            "materials": materials
        }
    )
    
# ==========================================
# Assignment List
# ==========================================

@login_required
def assignments(request, course_id):

    # Get selected course
    course = Course.objects.get(id=course_id)

    # Get all assignments of this course
    assignments = Assignment.objects.filter(course=course)

    return render(
        request,
        "assignments.html",
        {
            "course": course,
            "assignments": assignments
        }
    )


# ==========================================
# Logout
# ==========================================
@login_required
def logout_view(request):

    logout(request)

    messages.success(request, "Logged out successfully!")

    return redirect("login")



# ==========================================
# Teacher Dashboard
# ==========================================

@login_required
def teacher_dashboard(request):

    # Only staff users can access teacher dashboard
    if not request.user.is_staff:

        messages.error(
            request,
            "You do not have permission to access the teacher panel."
        )

        return redirect("dashboard")


@login_required
def teacher_add_course(request):

    if not request.user.is_staff:
        messages.error(
            request,
            "You do not have permission to access the teacher panel."
        )
        return redirect("dashboard")

    if request.method == "POST":

        course_code = request.POST.get("course_code")
        course_name = request.POST.get("course_name")
        credit = request.POST.get("credit")
        semester = request.POST.get("semester")
        description = request.POST.get("description")

        if Course.objects.filter(course_code=course_code).exists():
            messages.error(
                request,
                "Course code already exists!"
            )
            return redirect("teacher_add_course")

        Course.objects.create(
            course_code=course_code,
            course_name=course_name,
            instructor=request.user.username,
            credit=credit,
            semester=semester,
            description=description
        )

        messages.success(
            request,
            "Course added successfully!"
        )

        return redirect("teacher_dashboard")

    return render(
        request,
        "teacher_add_course.html"
    )

    # Get all courses
    courses = Course.objects.all()

    return render(
        request,
        "teacher_dashboard.html",
        {
            "courses": courses
        }
    )