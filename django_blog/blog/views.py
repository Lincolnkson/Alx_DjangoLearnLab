from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, UserUpdateForm
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment, Tag
from .forms import PostForm, CommentForm
from django.db.models import Q


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
    
    context = {
        'u_form': u_form,
    }
    
    return render(request, 'blog/profile.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 5
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Get the search query from URL parameters
        query = self.request.GET.get('q')
        tag_slug = self.request.GET.get('tag')
        
        if tag_slug:
            # Filter by tag if tag parameter is provided
            queryset = queryset.filter(tags__slug=tag_slug).distinct()
            
        if query:
            # Filter by title, content, author username, or tag name
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(author__username__icontains=query) |
                Q(tags__name__icontains=query)
            ).distinct()
            
        return queryset.order_by('-published_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add search query to context to maintain in pagination links
        context['query'] = self.request.GET.get('q', '')
        context['tag'] = self.request.GET.get('tag', '')
        # Add all tags for sidebar filtering
        context['all_tags'] = Tag.objects.all()
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        context['comment_form'] = CommentForm()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = '/posts/'
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


# Homepage view
def home(request):
    return render(request, 'blog/home.html', {'title': 'Home'})


# Search view
def search_posts(request):
    query = request.GET.get('q', '')
    tag = request.GET.get('tag', '')
    
    posts = Post.objects.all().order_by('-published_date')
    
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__username__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
    
    if tag:
        posts = posts.filter(tags__slug=tag).distinct()
    
    context = {
        'posts': posts,
        'query': query,
        'tag': tag,
        'all_tags': Tag.objects.all(),
        'title': 'Search Results'
    }
    
    return render(request, 'blog/search_results.html', context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post-detail', pk=post.id)
    
    return redirect('post-detail', pk=post.id)


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    
    
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
    
    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.id})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
    
    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.id})


# Tag detail view
class TagDetailView(DetailView):
    model = Tag
    template_name = 'blog/tag_detail.html'
    context_object_name = 'tag'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.object.posts.all().order_by('-published_date')
        return context