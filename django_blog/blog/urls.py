from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import PostListView,PostDetailView,PostCreateView,PostUpdateView,PostDeleteView, CommentUpdateView, CommentDeleteView,CommentCreateView,TagDetailView

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    path('', views.home, name='blog-home'),
    path('home/', views.home, name='home'),
    path('post/', PostListView.as_view(), name='posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/comments/new/', CommentCreateView.as_view(), name='add-comment'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='update-comment'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='delete-comment'),
    path('search/', views.search_posts, name='search-posts'),
    # path('tag/<slug:slug>/', TagDetailView.as_view(), name='tag-detail'),
    # add for the following ["tags/<slug:tag_slug>/", "PostByTagListView.as_view()"]
    path('tags/<slug:tag_slug>/', views.PostByTagListView.as_view(), name='post-by-tag'),

]
