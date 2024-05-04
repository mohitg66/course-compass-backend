from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from courses import views as courses_views
from rest_framework_simplejwt import views as jwt_views

router = DefaultRouter()
router.register(r'courses', courses_views.CourseViewSet, basename='courses')  # Use 'courses' as the basename
router.register(r'instructors', courses_views.InstructorViewSet, basename='instructors')  # Use 'instructors' as the basename
router.register(r'reviews', courses_views.ReviewViewSet, basename='reviews')  # Use 'reviews' as the basename
router.register(r'users', courses_views.UserViewSet, basename='users')  # Use 'users' as the basename

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', include('courses.urls')),
    
    path('token/', 
          jwt_views.TokenObtainPairView.as_view(), 
          name ='token_obtain_pair'),
    path('token/refresh/', 
          jwt_views.TokenRefreshView.as_view(), 
          name ='token_refresh')
]
