from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from snippets.models import Snippet 
from snippets.serializers import SnippetSerializer
from django.http import JsonResponse, HttpResponse

# Create your views here.
@csrf_exempt
def snippet_list(request):
  """
  List all code snippets or create a new snippet
  """
  if request.method == 'GET':
    snippets = Snippet.objects.all() # return all snippets in the database
    serializer = SnippetSerializer(snippets, many=True) # serialize the data
    return JsonResponse(serializer.data, safe=False) # return the serialized data
  
  elif request.mdthod == 'POST':
    data = JSONParser().parse(request)
    serializer = SnippetSerializer(data=data)
    if serializer.is_valid():
      serializer.save()
      return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def snippet_detail(request, pk):
    """
    Retrieve, update or delete a code snippet
    """
    try:
      snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
      return HttpResponse(status= 404)

    if request.method == 'GET':
      serializer = SnippetSerializer(snippet)
      return JsonResponse(serializer.data)
    
    elif request.method == 'PUT':
      data = JSONParser().parse(request)
      serializer = SnippetSerializer(snippet, data=data)
      if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data)
      return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
      snippet.delete()
      return HttpResponse(status = 204)