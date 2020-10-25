from django.shortcuts import render
from rest_framework import status 
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from snippets.models import Snippet 
from snippets.serializers import SnippetSerializer
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
@api_view(['GET', 'POST'])
def snippet_list(request, format=None):
  """
  List all code snippets or create a new snippet
  """
  if request.method == 'GET':
    snippets = Snippet.objects.all() # return all snippets in the database
    serializer = SnippetSerializer(snippets, many=True) # serialize the data
    return JsonResponse(serializer.data, safe=False) # return the serialized data
  
  elif request.mdthod == 'POST':
    serializer = SnippetSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk, format=None):
    """
    Retrieve, update or delete a code snippet
    """
    try:
      snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
      return Response(status= status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
      serializer = SnippetSerializer(snippet)
      return JsonResponse(serializer.data)
    
    elif request.method == 'PUT':
      serializer = SnippetSerializer(snippet, data=request.data)
      if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data)
      return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
      snippet.delete()
      return Response(status = status.HTTP_204_NO_CONTENT)