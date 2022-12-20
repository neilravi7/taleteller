from rest_framework import viewsets
from ..serializers.serializers import ArticleSerializers
from rest_framework import generics
from post.models.post_models import Article
from rest_framework.response import Response

class ArticleList(viewsets.ViewSet):

    def list(self, request):
        queryset = Article.objects.filter(status='PUBLISHED')
        serializer = ArticleSerializers(queryset, many=True)
        return Response(serializer.data)
