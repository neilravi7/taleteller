from rest_framework.routers import DefaultRouter
from ..views.views import ArticleList

router = DefaultRouter()

router.register(r'article/v1/list', ArticleList, basename='article_list_api')