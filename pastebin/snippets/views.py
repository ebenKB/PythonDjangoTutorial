from django.shortcuts import render
from rest_framework import status, permissions
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from snippets.models import Snippet 
from snippets.serializers import SnippetSerializer
from snippets.serializers import UserSerializer
from django.http import JsonResponse
from rest_framework.decorators import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import mixins, generics
from django.contrib.auth.models import User
from snippets.permissions import IsOwnerOrReadOnly

# Create your views here.
class SnippetList(generics.ListCreateAPIView):
  permission_classes = [permissions.IsAuthenticatedOrReadOnly]
  queryset = Snippet.objects.all()
  serializer_class = SnippetSerializer   

  def perform_create(self, serializer):
    serializer.save(owner = self.request.user)
  # def get(self, request, *args, **kwargs):
  #   return self.list(request, *args, **kwargs)
  
  # def post(self, request, *args, **kwargs):
  #   return self.create(request, *args, **kwargs)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

class UserList(generics.ListAPIView):
  queryset= User.objects.all()
  serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer