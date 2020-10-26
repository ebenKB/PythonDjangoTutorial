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

# Create your views here.
class SnippetList(APIView):
   
      """
      List all code snippets or create a new snippet
      """
      def get(self, request, format=None):
        snippets = Snippet.objects.all() # return all snippets in the database
        serializer = SnippetSerializer(snippets, many=True) # serialize the data
        return JsonResponse(serializer.data, safe=False) # return the serialized data
      
      def post(self, request, format=None):
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
          serializer.save()
          return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SnippetDetail(APIView):
    def get_object(self, pk):
        """
        Retrieve, update or delete a code snippet
        """
        try:
          return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
          raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
      snippet = self.get_object(pk)
      serializer = SnippetSerializer(snippet, data=request.data)
      if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data)
      return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
      snippet = self.get_object(pk)
      snippet.delete()
      return Response(status = status.HTTP_204_NO_CONTENT)
