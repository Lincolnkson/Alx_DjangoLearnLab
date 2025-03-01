from django.shortcuts import render
from .models import Book
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from .models import Library
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib import messages


from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
# LibraryProject/relationship_app/views.py doesn't contain: ["relationship_app/list_books.html"]

#create, update, or delete
def has_perms(*perms):
    def _has_perms(user):
        return all(user.has_perm(perm) for perm in perms)
    return _has_perms

#create view for adding book
@permission_required('relationship_app.add_book', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        title = request.POST['title']
        author = request.POST['author']
        library = request.POST['library']
        book = Book(title=title, author=author, library=library)
        book.save()
        return redirect('list_books')
    return render(request, 'relationship_app/add_book.html')

#create view for updating book
@permission_required('relationship_app.change_book', raise_exception=True)
def update_book(request, id):
        book = Book.objects.get(id=id)
        if request.method == 'POST':
            title = request.POST['title']
            author = request.POST['author']
            library = request.POST['library']
            book.title = title
            book.author = author
            book.library = library
            book.save()
            return redirect('list_books')
        return render(request, 'relationship_app/update_book.html', {'book': book})

#create view for deleting book
@permission_required('relationship_app.delete_book', raise_exception=True)
def delete_book(request, id):
    book = Book.objects.get(id=id)
    book.delete()
    return redirect('list_books')


@user_passes_test(User.has_perms('can_add_book', 'can_change_book', 'can_delete_book'))
@login_required
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

@permission_required([Book.can_add_book, Book.can_change_book, Book.can_delete_book], raise_exception=True)
class LibraryDetailView(ListView):
          model = Book
          template_name = 'relationship_app/library_detail.html'
          context_object_name = 'books'
          def get_queryset(self):
                      return Book.objects.filter(library=self.kwargs['pk'])
                   


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redirect if user is already logged in
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                # Get next parameter or default to home
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'relationship_app/login.html', {'form': form})



@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return render(request, 'relationship_app/logout.html')

# create a view for the registration form
# LibraryProject/relationship_app/views.py doesn't contain: ["UserCreationForm()"]
class register(FormView):
        template_name = 'relationship_app/register.html'
        form_class = UserCreationForm()
        success_url = reverse_lazy('login')
     
        def form_valid(self, form):
            form.save()
            return super().form_valid(form)
        


# Check if the user is an Admin
def is_admin(User):
    return User.userprofile.role == UserProfile.Admin

# Check if the user is a Librarian
def is_librarian(User):
    return User.userprofile.role == UserProfile.Librarian

# Check if the user is a Member
def is_member(User):
    return User.userprofile.role == UserProfile.Member

# Admin View
# @login_required
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

# Librarian View
@login_required
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

# Member View
@login_required
@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')