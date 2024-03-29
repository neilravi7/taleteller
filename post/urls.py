from django.urls import path, re_path
from . import views

app_name = 'post'
urlpatterns = [
    # =================== Article views ========================================================== 
    path('errors/', views.error_500_pages, name="errors"),
    # re_path(r'^.*$', views.error_404_pages, name="errors"),
    path('', views.ArticleListView.as_view(), name='home'),
    path('search/', views.ArticleSearchListView.as_view(), name='search'),
    path('create/', views.ArticleView.as_view(), name='article_create'),
    path('details/<str:slug>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('delete/<str:slug>/', views.ArticleDeleteView.as_view(), name='article_delete'),
    path('update/<str:slug>/', views.ArticleUpdateView.as_view(), name='article_update'),

    # =================== Category views ==========================================================
    path('category/', views.CategoryView.as_view(), name="create_category"),

    # =================== Comments views ==========================================================
    path('comment/<str:slug>', views.CommentView.as_view(), name='create_comment'),
]