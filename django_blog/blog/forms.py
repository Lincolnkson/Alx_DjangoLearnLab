from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment, Tag

# Custom Tag Widget
class TagWidget(forms.TextInput):
    """
    Custom widget for handling tags with autocomplete functionality
    """
    class Media:
        css = {
            'all': ('css/tagwidget.css',)
        }
        js = ('js/tagwidget.js',)
    
    def __init__(self, attrs=None):
        default_attrs = {'class': 'form-control tag-input', 'data-role': 'tagsinput'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email']


# class ProfileUpdateForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['image']


class PostForm(forms.ModelForm):
    tags_input = forms.CharField(
        label='Tags', 
        required=False,
        widget=TagWidget(),
        help_text='Enter tags separated by commas.'
    )
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags_input']
    
    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)
        
        # If we're editing a post with existing tags, prefill the tags_input field
        if instance and instance.pk:
            self.initial['tags_input'] = ', '.join([tag.name for tag in instance.tags.all()])
    
    def save(self, commit=True):
        post = super().save(commit=False)
        
        if commit:
            post.save()
            
            # Clear existing tags if any
            post.tags.clear()
            
            # Process tags input
            tags_input = self.cleaned_data.get('tags_input', '')
            if tags_input:
                tag_names = [t.strip() for t in tags_input.split(',') if t.strip()]
                
                for tag_name in tag_names:
                    # Create or get existing tag
                    from django.utils.text import slugify
                    tag, created = Tag.objects.get_or_create(
                        name=tag_name,
                        defaults={'slug': slugify(tag_name)}
                    )
                    post.tags.add(tag)
                    
        return post       


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Add a comment...'}),
        }