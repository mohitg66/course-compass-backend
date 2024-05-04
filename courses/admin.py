from django.contrib import admin

# Register your models here.
from .models import Course, Instructor, Review

class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'codes', 'institute', 'avg_rating', 'avg_difficulty', 'avg_workload', 'avg_class_size', 'avg_grade')
    
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('name', 'avg_rating')
    
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'instructor', 'course_rating', 'instructor_rating', 'difficulty', 'workload', 'class_size', 'grade', 'comment')
    
admin.site.register(Course, CourseAdmin)
admin.site.register(Instructor, InstructorAdmin)
admin.site.register(Review, ReviewAdmin)