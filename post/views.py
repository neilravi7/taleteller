#  Django Core Import
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import View, CreateView, ListView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q

# apps form and models and utility imports
from post.forms import CategoryForm, ArticleForm, ArticleSearchForm, CommentForm
from post.models import Category, Article, Comment
from .utils import text_to_paragraph

# Third party import
from taggit.models import Tag

# Create your views here.

#Just Demo views for template testing
"""=========================================================================="""


def error_pages(request):
    return render(request, 'errors/errors.html')


def template_testing_view(request):
    return render(request, 'post/post_list.html')


"""=========================================================================="""


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
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(approved=True)
        context['tags'] = Tag.objects.filter()
        context['form'] = ArticleSearchForm()
        return context


class ArticleSearchListView(ListView):
    model = Article
    template_name = 'post/article_home.html'
    paginate_by = 5
    context_object_name = 'articles'

    def get_context_data(self, *args, **kwargs):
        context = super(ArticleSearchListView, self).get_context_data(**kwargs)
        
        search_text = self.request.GET.get('search')
        search_type = self.request.GET.get('search_type')

        lookups = Q()

        if search_type:
            
            if search_type == "categories":

                lookups = lookups | Q(category__name=search_text)
                print("it's category lookup")

            elif search_type == 'tags':

                lookups = lookups | Q(tags__name=search_text)
                print("it's tags lookup")
        else:
            
            lookups = lookups | Q(title__icontains=search_text) | Q(
                body__icontains=search_text) | Q(slug__icontains=search_text)
            print("it's search lookups")

        # Building Context Data Dict
        context['articles'] = Article.objects.filter(lookups)
        context['form'] = ArticleSearchForm()
        context['categories'] = Category.objects.filter(approved=True)
        context['tags'] = Tag.objects.filter()
        return context


class ArticleDeleteView(DeleteView):

    def get(self, request, *args, **kwargs):
        article = get_object_or_404(Article, slug=self.kwargs.get('slug'))
        if request.user.username != article.author.username:
            messages.warning(
                request, f"You do not have permission to delete this article.")
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

        article.deleted = True
        article.status = 'DRAFT'
        article.save()

        messages.success(request=self.request,
                         message="Article Deleted Successfully")
        return redirect(to='account:dashboard')


class ArticleUpdateView(LoginRequiredMixin, View):
    """
    Article Update View
    """
    template_name = 'post/article_update.html'
    context_object = {}

    def get(self, request, *args, **kwargs):
        article_form = ArticleForm(
            instance=Article.objects.get(slug=self.kwargs.get('slug')))

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
            return HttpResponseRedirect(
                reverse(
                    'post:article_detail',
                    kwargs={
                        'slug': self.kwargs['slug']
                    }
                )
            )
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
        )[:3]  # limit by three article

        context['comments'] = self.object.comments.filter(approved=True)
        context['recent_articles'] = Article.objects.filter(
            status=Article.PUBLISHED).exclude(id=self.object.id)[:3]
        context['search_form'] = ArticleSearchForm()
        context['comment_form'] = CommentForm()
        context['categories'] = Category.objects.filter(approved=True)
        context['tags'] = Tag.objects.filter()
        # down in to small paragraphs from one large paragraph
        # something like markups
        # (for some reasons we can't use rich text)
        context['text_to_paragraph'] = text_to_paragraph(self.object.body)
        return super().get_context_data(**context)


class CommentView(View):

    def post(self, *args, **kwargs):
        comment_form = CommentForm(data=self.request.POST)
        print(comment_form)
        if comment_form.is_valid():
            comment_form.save(commit=False)
            comment_form.instance.article = Article.objects.get(
                slug=self.kwargs['slug'])
            comment_form.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return render(self.request, 'errors/errors.html', {"response_code": "500", "response_message": "Opps!! some error occurred."})

    def get_success_url(self, *args, **kwargs):
        return reverse('post:article_detail', kwargs={'slug': self.kwargs['slug']})
