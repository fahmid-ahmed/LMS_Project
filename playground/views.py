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

    # Get all courses
    courses = Course.objects.all()

    return render(
        request,
        "teacher_dashboard.html",
        {
            "courses": courses
        }
    )


# ==========================================
# Teacher Add Course
# ==========================================

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