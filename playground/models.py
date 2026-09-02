# Import Django's database module
from django.db import models

# Import Django's built-in User model
from django.contrib.auth.models import User


# ==========================================
# Student Profile Model
# ==========================================

class StudentProfile(models.Model):

    # Connect one StudentProfile to one User
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    # Student ID
    student_id = models.CharField(
        max_length=20,
        unique=True
    )

    # Department
    department = models.CharField(
        max_length=100
    )

    # Semester
    semester = models.IntegerField()

    # Phone Number
    phone = models.CharField(
        max_length=20
    )

    def __str__(self):
        return self.user.username


# ==========================================
# Course Model
# ==========================================

class Course(models.Model):

    # Course Code
    course_code = models.CharField(
        max_length=20,
        unique=True
    )

    # Course Name
    course_name = models.CharField(
        max_length=200
    )

    # Teacher Name
    instructor = models.CharField(
        max_length=100
    )

    # Credit Hours
    credit = models.IntegerField()

    # Semester
    semester = models.IntegerField()

    # Course Description
    description = models.TextField()

    def __str__(self):
        return f"{self.course_code} - {self.course_name}"


# ==========================================
# Enrollment Model
# ==========================================

class Enrollment(models.Model):

    # Student
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    # Course
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )

    # Enrollment Date
    enrolled_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ("student", "course")

    def __str__(self):
        return f"{self.student.username} - {self.course.course_name}"


# ==========================================
# Learning Material Model
# ==========================================

class LearningMaterial(models.Model):

    # Course
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )

    # Material title
    title = models.CharField(
        max_length=200
    )

    # Material type
    material_type = models.CharField(
        max_length=50
    )

    # Uploaded file
    file = models.FileField(
        upload_to="course_materials/"
    )

    # Upload date
    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title


# ==========================================
# Assignment Model
# ==========================================

class Assignment(models.Model):

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )

    title = models.CharField(
        max_length=200
    )

    description = models.TextField()

    due_date = models.DateField()

    file = models.FileField(
        upload_to="assignments/"
    )

    def __str__(self):
        return self.title


# ==========================================
# Assignment Submission
# ==========================================

class AssignmentSubmission(models.Model):

    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE
    )

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    submission_file = models.FileField(
        upload_to="submissions/"
    )

    submitted_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.student.username} - {self.assignment.title}"