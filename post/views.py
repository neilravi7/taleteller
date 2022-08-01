from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import View, CreateView, ListView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from post.forms import CategoryForm, ArticleForm, ArticleSearchForm
from post.models import Category, Article
from django.db.models import Q
from taggit.models import Tag

# Create your views here.

#Just Demo views for template testing
#'''=========================================================================='''
def home_view(request):
    return render(request, 'post/post_list.html')


def profile_view(request):
    return render(request, 'account/profile.html')
#
#'''=========================================================================='''

#Meaningful view here

    
#    def get_success_url(self):
#        return HttpResponseRedirect(reverse('post:home'))
        

class CategoryView(LoginRequiredMixin, CreateView):
    template_name = 'post/category.html'
    success_message = "Category Added Successfully."
    form_class = CategoryForm

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        context['all_category'] = Category.objects.filter(active=True)
        return context

    def get_success_url(self):
        return reverse('post:create_category')


# ===================================== Article Views ======================================================================
class ArticleView(LoginRequiredMixin, CreateView):
    template_name = 'post/article_create.html'
    success_message = "Post Added Successfully"
    form_class = ArticleForm
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super(ArticleView, self).form_valid(form)

    def get_success_url(self):
        return reverse('post:home')


class ArticleListView(ListView):
    context_object_name = 'articles'
    queryset = Article.objects.filter(status=Article.PUBLISHED, deleted=False)
    template_name = "post/article_home.html"
    # print("This fucking view called")
    # print(dir())

    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(approved=True)
        context['tags'] = Tag.objects.filter()
        context['form'] = ArticleSearchForm()
        # print("context", context)
        return context


class ArticleSearchListView(ListView):
    model = Article
    template_name = 'post/article_home.html'
    # paginate_by = 12
    context_object_name = 'articles'
    
    def get_context_data(self, *args, **kwargs):
        context = super(ArticleSearchListView, self).get_context_data(**kwargs)
        search_text = self.request.GET.get('search')
        context['articles'] = Article.objects.filter(
            Q(title__icontains=search_text) | Q(body__icontains=search_text) | Q(slug__icontains=search_text)
        )
        context['form'] = ArticleSearchForm()
        context['categories'] = Category.objects.filter(approved=True)
        context['tags'] = Tag.objects.filter()
        return context


class ArticleDeleteView(DeleteView):

    def get(self, request, *args, **kwargs):
        article = get_object_or_404(Article, slug=self.kwargs.get('slug'))
        if request.user.username != article.author.username:
            messages.warning(request, f"You do not have permission to delete this article.")
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        
        article.deleted = True
        article.save()

        messages.success(request=self.request, message="Article Deleted Successfully")
        return redirect(to='post:profile')


class ArticleUpdateView(LoginRequiredMixin, View):
    """
    Article Update View
    """
    template_name = 'post/article_update.html'
    context_object = {}
    
    def get(self, request, *args, **kwargs):
        article_form = ArticleForm(instance = Article.objects.get(slug=self.kwargs.get('slug')))
        
        self.context_object['form'] = article_form
        
        return render(request, self.template_name, self.context_object)
    
    def post(self, request, *args, **kwargs):
        article_form = ArticleForm(
            data=request.POST,
            instance=Article.objects.get(slug=self.kwargs.get('slug'))
        )
        
        if article_form.is_valid():
            article_form.save()
            
            messages.success(
                request, 
                f"Article has successfully been updated"
            )
            return HttpResponseRedirect(reverse('post:profile'))
        else:
            article_form = ArticleForm(
                instance=Article.objects.get(slug=self.kwargs.get('slug'))
            )
            self.context_object['form'] = article_form
            messages.error(request, f"Invalid data. Please provide valid data")
        

class ArticleDetailView(DetailView):
    model = Article
    template_name = "post/article_details.html"

    def get_context_data(self, **kwargs):
        """Insert the single object into the context dict."""
        context = {}
        if self.object:
            context['object'] = self.object
            print(self.object.author)
            context_object_name = self.get_context_object_name(self.object)
            if context_object_name:
                context[context_object_name] = self.object
        context.update(kwargs)
        context['author_articles'] = Article.objects.filter(
            author=self.object.author, 
            status=Article.PUBLISHED
        )[:3] # limit by three article

        context['recent_articles'] = Article.objects.filter(status=Article.PUBLISHED).exclude(id=self.object.id)[:3] 
        context['form'] = ArticleSearchForm()
        context['categories'] = Category.objects.filter(approved=True)
        context['tags'] = Tag.objects.filter()
        return super().get_context_data(**context)