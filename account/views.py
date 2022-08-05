from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.views.generic import View, ListView
from django.views.generic.edit import CreateView
from django.contrib.auth import views as auth_view
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse
from .forms import UserRegisterForm, UserLoginForm, ProfileForm
from django.contrib import messages
from post.models.author_models import Profile
from post.models.post_models import Article
from django.core.paginator import Paginator

# Create your views here.

class UserCreationView(SuccessMessageMixin, CreateView):
    """Author Creation.
    """
    template_name = 'account/register.html'
    success_message = "Your Profile Created Successfully"
    form_class = UserRegisterForm

    def form_valid(self, form):
        self.object = form.save()
        Profile.objects.create(user = self.object)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('account:login')

# Custom login view inheriting View.
class UserLoginView(View):
    """Logs user(Author) into dashboard 
    """
    template_name = 'account/login.html'
    success_message = "Logged In Successfully"
    context = {
        "form":UserLoginForm
    }

    def get(self, request, *args, **kwargs):
        return render(self.request, self.template_name, self.context)
    
    def post(self, request, *args, **kwargs):
        form = UserLoginForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Authenticating User.
            user = authenticate(request, username=username, password=password)
            
            #  Creating Session for active user
            if user:
                login(request, user)
                messages.success(
                    request, f"Login Successful ! "
                    f"Welcome {user.username}."
                )
                return HttpResponseRedirect(reverse('account:dashboard'))
            else:
                messages.error(
                    request,
                    f"Invalid Login details: {username}, {password} "
                    f"are not valid username and password !!! Please "
                    f"enter a valid username and password."
                )
                return render(request, self.template_name, self.context)
        else:
            messages.error(request, f"Invalid username and password")
            return render(request, self.template_name, self.context)      


# Simple login Using inherit LoginView
#  THIS VIEW NOT IN USE
class UserLogin(SuccessMessageMixin, auth_view.LoginView):
    template_name = 'account/login.html'
    success_message = "Logged in successfully"

    form_class = UserLoginForm

    def get_success_url(self):
        return reverse('post:home')


class UserLogout(SuccessMessageMixin, auth_view.LogoutView):
    success_message = "User logout successfully"

    def get_success_url(self):
        return reverse('account:login')

# Author Dashboard View 
class AuthorDashboardView(LoginRequiredMixin, ListView):
    model = Article
    template_name = "author/dashboard.html"
    paginate_by = 5
    queryset = Article.objects.all()
    
    def get_context_data(self, *args, **kwargs):
        context = super(AuthorDashboardView, self).get_context_data(**kwargs)
        articles = self.queryset.filter(author=self.request.user)
        context["articles"] = articles
        context["published_articles"] = articles.filter(status=Article.PUBLISHED, deleted=False)
        context["drafted_articles"] = articles.filter(status=Article.DRAFTED)
        context["deleted_articles"] = articles.filter(deleted=True)
        return context


# Profile Update View
# Contain Profile Form
class AuthorProfile(LoginRequiredMixin, View):
    """
    User Update View
    """
    template_name = 'author/profile_update.html'
    context_object = {}
    
    def get(self, request):
        profile_form = ProfileForm(instance = self.request.user.authors_profile)
        
        self.context_object['form'] = profile_form
        
        return render(request, self.template_name, self.context_object)
    
    def post(self, request):
        profile_form = ProfileForm(
            data=request.POST,
            instance=self.request.user.authors_profile
        )
        
        if profile_form.is_valid():
            profile_form.save()
            
            messages.success(
                request, 
                f"Your Account has successfully been updated"
            )
            return HttpResponseRedirect(reverse('account:dashboard'))
        else:
            profile_form = ProfileForm(
                instance = self.request.user.authors_profile
            )
            self.context_object['form'] = profile_form
            messages.error(request, f"Invalid data. Please provide valid data")