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
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta
#create User import
from django.contrib.auth.models import User


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
    
    # Show user's posts using Post.objects.filter
    user_posts = Post.objects.filter(author=request.user).order_by('-published_date')
    
    context = {
        'u_form': u_form,
        'user_posts': user_posts,
    }
    
    return render(request, 'blog/profile.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 5
    
    def get_queryset(self):
        # Start with all posts
        queryset = Post.objects.all()
        
        # Get filter parameters from URL
        query = self.request.GET.get('q')
        tag_slug = self.request.GET.get('tag')
        time_filter = self.request.GET.get('time')
        author_id = self.request.GET.get('author')
        
        # Filter by search query
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(author__username__icontains=query) |
                Q(tags__name__icontains=query)
            ).distinct()
        
        # Filter by tag
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug).distinct()
        
        # Filter by author
        if author_id:
            queryset = queryset.filter(author_id=author_id)
            
        # Filter by time period
        if time_filter:
            now = timezone.now()
            if time_filter == 'today':
                queryset = queryset.filter(published_date__gte=now.replace(hour=0, minute=0, second=0))
            elif time_filter == 'week':
                queryset = queryset.filter(published_date__gte=now - timedelta(days=7))
            elif time_filter == 'month':
                queryset = queryset.filter(published_date__gte=now - timedelta(days=30))
            elif time_filter == 'year':
                queryset = queryset.filter(published_date__gte=now - timedelta(days=365))
        
        # Order by published date
        return queryset.order_by('-published_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add search query and filters to context
        context['query'] = self.request.GET.get('q', '')
        context['tag'] = self.request.GET.get('tag', '')
        context['time_filter'] = self.request.GET.get('time', '')
        context['author_filter'] = self.request.GET.get('author', '')
        
        # Add all tags with post count for sidebar
        context['all_tags'] = Tag.objects.annotate(post_count=Count('posts')).order_by('-post_count')
        
        # Add popular posts
        context['popular_posts'] = Post.objects.annotate(comment_count=Count('comments')).order_by('-comment_count')[:5]
        
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        
        # Get comments for this post
        context['comments'] = post.comments.all()
        context['comment_form'] = CommentForm()
        
        # Get related posts by tag using Post.objects.filter
        post_tags_ids = post.tags.values_list('id', flat=True)
        if post_tags_ids:
            related_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id).distinct()
            context['related_posts'] = related_posts.order_by('-published_date')[:3]
        
        # Get posts from same author
        context['author_posts'] = Post.objects.filter(author=post.author).exclude(id=post.id).order_by('-published_date')[:3]
        
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
    # Get popular and recent posts for homepage
    recent_posts = Post.objects.all().order_by('-published_date')[:5]
    popular_posts = Post.objects.annotate(comment_count=Count('comments')).order_by('-comment_count')[:5]
    
    # Get trending tags (most used in the past week)
    week_ago = timezone.now() - timedelta(days=7)
    trending_posts = Post.objects.filter(published_date__gte=week_ago)
    trending_tags = Tag.objects.filter(posts__in=trending_posts).annotate(
        post_count=Count('posts')
    ).order_by('-post_count')[:10]
    
    context = {
        'title': 'Home',
        'recent_posts': recent_posts,
        'popular_posts': popular_posts,
        'trending_tags': trending_tags,
    }
    return render(request, 'blog/home.html', context)


# Search view with advanced filtering
def search_posts(request):
    query = request.GET.get('q', '')
    tag = request.GET.get('tag', '')
    time_filter = request.GET.get('time', '')
    author_id = request.GET.get('author', '')
    sort_by = request.GET.get('sort', 'recent')  # Default sort by recent
    
    # Start with base queryset
    posts = Post.objects.all()
    
    # Apply filters using Post.objects.filter
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__username__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
    
    if tag:
        posts = posts.filter(tags__slug=tag).distinct()
    
    if author_id:
        posts = posts.filter(author_id=author_id)
    
    # Apply time filter
    if time_filter:
        now = timezone.now()
        if time_filter == 'today':
            posts = posts.filter(published_date__gte=now.replace(hour=0, minute=0, second=0))
        elif time_filter == 'week':
            posts = posts.filter(published_date__gte=now - timedelta(days=7))
        elif time_filter == 'month':
            posts = posts.filter(published_date__gte=now - timedelta(days=30))
        elif time_filter == 'year':
            posts = posts.filter(published_date__gte=now - timedelta(days=365))
    
    # Apply sorting
    if sort_by == 'recent':
        posts = posts.order_by('-published_date')
    elif sort_by == 'comments':
        posts = posts.annotate(comment_count=Count('comments')).order_by('-comment_count')
    elif sort_by == 'alphabetical':
        posts = posts.order_by('title')
    
    # Get all tags for sidebar
    all_tags = Tag.objects.annotate(post_count=Count('posts')).order_by('-post_count')
    
    context = {
        'posts': posts,
        'query': query,
        'tag': tag,
        'time_filter': time_filter,
        'author_filter': author_id,
        'sort_by': sort_by,
        'all_tags': all_tags,
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


# Get posts by specific tag
class TagDetailView(DetailView):
    model = Tag
    template_name = 'blog/tag_detail.html'
    context_object_name = 'tag'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = self.get_object()
        
        # Get posts with this tag using Post.objects.filter
        context['posts'] = Post.objects.filter(tags=tag).order_by('-published_date')
        
        # Get related tags (tags that appear together with this tag)
        tag_posts = Post.objects.filter(tags=tag)
        related_tags = Tag.objects.filter(posts__in=tag_posts).exclude(id=tag.id).annotate(
            post_count=Count('posts')
        ).order_by('-post_count')[:10]
        context['related_tags'] = related_tags
        
        return context


# View for author profile and their posts
def author_posts(request, author_id):
    author = get_object_or_404(User, id=author_id)
    posts = Post.objects.filter(author=author).order_by('-published_date')
    
    # Get author's most used tags
    author_tags = Tag.objects.filter(posts__author=author).annotate(
        post_count=Count('posts')
    ).order_by('-post_count')[:10]
    
    context = {
        'author': author,
        'posts': posts,
        'author_tags': author_tags,
        'title': f'Posts by {author.username}'
    }
    
    return render(request, 'blog/author_posts.html', context)



