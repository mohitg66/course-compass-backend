from rest_framework import viewsets
from .models import Course, Instructor, Review, User
from .serializers import CourseSerializer, InstructorSerializer, ReviewSerializer, UserSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.
class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    
class InstructorViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer
    
class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    # def post(self, request):
    #     serializer = ReviewSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        try:
            review = self.get_object()
            user = User.objects.get(id=request.data['user_id'])
            review.likes.add(user) if request.data['like'] else review.likes.remove(user)
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=['post'])
    def report(self, request, pk=None):
        try:
            review = self.get_object()
            user = User.objects.get(id=request.data['user_id'])
            review.reports.add(user)
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class HomeView(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self, request):
        content = {'message': f'Hi {request.user}, Welcome to the JWT Authentication page using React Js and Django!'}
        return Response(content)

class LogoutView(APIView):
     permission_classes = (IsAuthenticated,)
     def post(self, request):
          try:
               refresh_token = request.data["refresh_token"]
               token = RefreshToken(refresh_token)
               token.blacklist()
               return Response(status=status.HTTP_205_RESET_CONTENT)
          except Exception as e:
               return Response(status=status.HTTP_400_BAD_REQUEST)

class LogInView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        user = User.objects.filter(username=username).first()
        if user is None:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        if not user.check_password(password):
            return Response({'message': 'Incorrect password'}, status=status.HTTP_403_FORBIDDEN)
        refresh = RefreshToken.for_user(user)
        print(f"username: {username}, password: {password}, user: {user}, refresh: {refresh}")
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'id': user.id,
        })
        
class RegisterView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        email = request.data['email']
        if User.objects.filter(username=username).exists():
            return Response({'message': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({'message': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=username, password=password, email=email)
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'id': user.id,
        })