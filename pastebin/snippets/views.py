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
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework.decorators import action
from rest_framework import viewsets


# Create your views here.
# class SnippetList(generics.ListCreateAPIView):
#   permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#   queryset = Snippet.objects.all()
#   serializer_class = SnippetSerializer   

#   def perform_create(self, serializer):
#     serializer.save(owner = self.request.user)


# class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve actions`
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class SnippetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides 'list', 'create', 'retrieve', 'update' and 'destroy' actions.

    Additionally we also provide an extra 'highlight' action.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    @action(detail = True, renderer_classes = [renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)
    
    def perform_create(self, serializer):
      serializer.save(owner= self.request.user)

@api_view(['GET'])
def api_root(request, format=None):
  return Response({
    'users': reverse('user-list', request=request, format=format),
    'snippets': reverse('snippet-list', request=request, format=format)
  })
