from rest_framework import serializers
from .models import Course, Instructor, Review
from django.contrib.auth.models import User

class CourseSerializer(serializers.ModelSerializer):
    avg_rating = serializers.FloatField(read_only=True)
    avg_difficulty = serializers.FloatField(read_only=True)
    avg_workload = serializers.FloatField(read_only=True)
    avg_class_size = serializers.FloatField(read_only=True)
    avg_grade = serializers.FloatField(read_only=True)
    get_instructors = serializers.DictField(child=serializers.FloatField(), read_only=True)
    get_comments = serializers.ListField(child=serializers.DictField(), read_only=True)
    
    class Meta:
        model = Course
        fields = '__all__'
        

class InstructorSerializer(serializers.ModelSerializer):
    avg_rating = serializers.FloatField(read_only=True)
    
    class Meta:
        model = Instructor
        fields = '__all__' 
        
class ReviewSerializer(serializers.ModelSerializer):
    get_user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Review
        fields = '__all__'
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')