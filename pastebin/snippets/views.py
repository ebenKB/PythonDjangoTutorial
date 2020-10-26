from django.shortcuts import render
from rest_framework import status 
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from snippets.models import Snippet 
from snippets.serializers import SnippetSerializer
from django.http import JsonResponse
from rest_framework.decorators import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import mixins, generics

# Create your views here.
class SnippetList(generics.ListCreateAPIView):
  queryset = Snippet.objects.all()
  serializer_class = SnippetSerializer
  # def get(self, request, *args, **kwargs):
  #   return self.list(request, *args, **kwargs)
  
  # def post(self, request, *args, **kwargs):
  #   return self.create(request, *args, **kwargs)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
