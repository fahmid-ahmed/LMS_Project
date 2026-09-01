from django.contrib import admin

from .models import (
    StudentProfile,
    Course,
    Enrollment,
    LearningMaterial,
    Assignment,
    AssignmentSubmission
)

admin.site.register(StudentProfile)
admin.site.register(Course)
admin.site.register(Enrollment)
admin.site.register(LearningMaterial)
admin.site.register(Assignment)
admin.site.register(AssignmentSubmission)