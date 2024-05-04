from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class Course(models.Model):
    name = models.CharField(max_length=255, unique=True)
    acronym = models.CharField(max_length=20, unique=True, blank=True, null=True)
    semester = models.CharField(max_length=20, choices=[('Winter', 'Winter'), ('Monsoon', 'Monsoon')], blank=True, null=True)
    codes = models.CharField(max_length=255)
    institute = models.CharField(max_length=255, default='IIITD')
    
    @property
    def avg_rating(self):
        reviews = self.reviews.exclude(course_rating=None)
        if reviews.count() == 0:
            return
        return reviews.aggregate(models.Avg('course_rating'))['course_rating__avg']

    @property
    def avg_difficulty(self):
        reviews = self.reviews.exclude(difficulty=None)
        if reviews.count() == 0:
            return
        return round(reviews.aggregate(models.Avg('difficulty'))['difficulty__avg'], 2)

    @property
    def avg_workload(self):
        # print("workload", self.reviews.all())
        reviews = self.reviews.exclude(workload=None)
        if reviews.count() == 0:
            return
        return round(reviews.aggregate(models.Avg('workload'))['workload__avg'], 2)

    @property
    def avg_class_size(self):
        reviews = self.reviews.exclude(class_size=None)
        if reviews.count() == 0:
            return
        return round(reviews.aggregate(models.Avg('class_size'))['class_size__avg'], 2)

    @property
    def avg_grade(self):
        reviews = self.reviews.exclude(grade=None)
        if reviews.count() == 0:
            return
        return round(reviews.aggregate(models.Avg('grade'))['grade__avg'], 2)
    
    @property
    def get_instructors(self):
        instructors = self.instructors.all()
        if instructors.count() == 0:
            return
        # return instructors and their avg_ratings
        return {instructor.name: instructor.avg_rating for instructor in instructors}
    
    @property
    def get_comments(self):
        reviews = self.reviews.exclude(comment=None)
        if reviews.count() == 0:
            return
        return [{   'id': review.id,
                    'user': review.get_user,
                    'comment': review.comment,
                    'likes': review.get_likes_count,
                    'reports': review.get_reports_count,
                } for review in reviews]
    
    def __str__(self):
        return self.name        

class Instructor(models.Model):
    name = models.CharField(max_length=255)
    courses = models.ManyToManyField(Course, related_name='instructors', blank=True)
    
    @property
    def avg_rating(self):
        reviews = self.reviews.exclude(instructor_rating=None)
        if reviews.count() == 0:
            return
        return reviews.aggregate(models.Avg('instructor_rating'))['instructor_rating__avg']
    
    def __str__(self):
        return self.name

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='reviews', blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    instructor = models.ForeignKey(Instructor, on_delete=models.SET_NULL, related_name='reviews', blank=True, null=True)
    course_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    instructor_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], blank=True, null=True)
    difficulty = models.IntegerField(choices=[(1, 'Very Easy'), (2, 'Easy'), (3, 'Medium'), (4, 'Hard'), (5, 'Very Hard')])
    workload = models.IntegerField(choices=[(1, 'Very Low'), (2, 'Low'), (3, 'Medium'), (4, 'High'), (5, 'Very High')])
    class_size = models.IntegerField(choices=[(1, 'Small'), (2, 'Medium'), (3, 'Large')])
    grade = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    comment = models.TextField(blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='liked_reviews', blank=True)
    reports = models.ManyToManyField(User, related_name='reported_reviews', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    
    @property
    def get_user(self):
        return self.user.username if self.user else 'Anonymous'
    
    @property
    def get_likes_count(self):
        return self.likes.count()
    
    @property
    def get_reports_count(self):
        return self.reports.count()
        
    def __str__(self):
        return f'{self.user.username if self.user else "Anonymous"}\'s review of {self.course.name}'
    