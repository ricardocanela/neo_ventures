from rest_framework import viewsets

from .models import Company, Demand, Solution
from .serializers import CompanySerializer, DemandListSerializer, DemandCreateSerializer, SolutionListSerializer, SolutionCreateSerializer
from .serializers import RegisterSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework import filters, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def create(self, request, *args, **kwargs):
        company = Company(user=self.request.user)
        serializer = self.serializer_class(company, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class DemandViewSet(viewsets.ModelViewSet):
    queryset = Demand.objects.all()
    permission_classes = (IsAuthenticated,) 
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return DemandListSerializer
        return DemandCreateSerializer
    
class SolutionViewSet(viewsets.ModelViewSet):
    queryset = Solution.objects.all()
    permission_classes = (IsAuthenticated,) 
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SolutionListSerializer
        return SolutionCreateSerializer

class UserDetailAPI(APIView):
  permission_classes = (IsAuthenticated,)
  def get(self,request,*args,**kwargs):
    user = User.objects.get(id=request.user.id)
    serializer = UserSerializer(user)
    return Response(serializer.data)

class RegisterUserAPIView(generics.CreateAPIView):
  permission_classes = (AllowAny,)
  serializer_class = RegisterSerializer