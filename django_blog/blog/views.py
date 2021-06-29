from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .models import Post
from .forms import CommentForm, BlogSearchForm



# Create your views here.

# def home(request):
#     context = {
#         'posts': Post.objects.filter(date_published__isnull=False)  
#     }
#     return render(request, 'blog/home.html', context)



class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_published',]
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(
            date_published__isnull=False
        ).order_by('-date_published')


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(
            author=user, 
            date_published__isnull=False
        ).order_by('-date_published')



class UserDraftListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/user_drafts.html'
    context_object_name = 'drafts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(
            author=user, 
            date_published__isnull=True
        ).order_by('-date_drafted')



class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    form = CommentForm

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(approved=True)
        context['form'] = self.form
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)

        if form.is_valid():
            post = self.get_object()
            form.instance.post = post
            form.save() 
            return redirect('post_detail', pk=post.pk)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    # set the author
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)



class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    redirect_field_name = 'blog/post_detail.html'

    # set the author
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # only let author make changes to the post
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author



class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    # only let author make changes to the post
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


@login_required
def publish_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('user_posts', post.author.username)

@login_required
def like_post(request):
    if request.POST.get('action') == 'POST':
        
        id = request.POST.get('postid')
        post = get_object_or_404(Post, id=id)

        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        post.save()

        return JsonResponse({'updated_count': post.likes.count()})


def search_blog(request):
    form = BlogSearchForm()
    query = ''
    results = []
    if 'query' in request.GET:
        form = BlogSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            post_results = Post.objects.filter(
                Q(title__contains=query) |
                Q(content__contains=query) |
                Q(author__contains=query)
            )
            comment_results = Comment.objects.filter(
                Q(text__contains=query) |
                Q(author__contains=query)
            )
            results = post_results + comment_results 

    return render(request, 'blog/search.html', {'form': form, 'query': query, 'results':results})



 

 


