from django.shortcuts import render
from .models import Book
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from .models import Library
from django.contrib.auth.forms import UserCreationForm


# LibraryProject/relationship_app/views.py doesn't contain: ["relationship_app/list_books.html"]
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})


class LibraryDetailView(ListView):
          model = Book
          template_name = 'relationship_app/library_detail.html'
          context_object_name = 'books'
          def get_queryset(self):
                      return Book.objects.filter(library=self.kwargs['pk'])
                   

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib import messages


from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin


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
        
"""
Step 2: Set Up Role-Based Views
Create three separate views to manage content access based on user roles:

Views to Implement:

An ‘Admin’ view that only users with the ‘Admin’ role can access, the name of the file should be admin_view
A ‘Librarian’ view accessible only to users identified as ‘Librarians’. The file should be named librarian_view
A ‘Member’ view for users with the ‘Member’ role, the name of the file should be member_view
Access Control:

Utilize the @user_passes_test decorator to check the user’s role before granting access to each view.
"""
# Constants for role names to avoid typos and ensure consistency
ROLE_ADMIN = 'ADMIN'
ROLE_LIBRARIAN = 'LIBRARIAN'
ROLE_MEMBER = 'MEMBER'

# Role check functions
def is_admin(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == ROLE_ADMIN

def is_librarian(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == ROLE_LIBRARIAN

def is_member(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == ROLE_MEMBER

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """
    Admin dashboard view - accessible only to users with Admin role
    """
    context = {
        # 'title': 'Admin Dashboard',
        # 'user_count': User.objects.count(),
        # 'librarian_count': UserProfile.objects.filter(role=ROLE_LIBRARIAN).count(),
        # 'member_count': UserProfile.objects.filter(role=ROLE_MEMBER).count(),
    }
    return render(request, 'admin_dashboard.html', context)

@login_required
@user_passes_test(is_librarian)
def librarian_dashboard(request):
    """
    Librarian dashboard view - accessible only to users with Librarian role
    """
    context = {
        'title': 'Librarian Dashboard',
        'books': Book.objects.all(),
        # 'pending_requests': BookRequest.objects.filter(status='PENDING'),
    }
    return render(request, 'librarian_view.html', context)

@login_required
@user_passes_test(is_member)
def member_dashboard(request):
    """
    Member dashboard view - accessible only to users with Member role
    """
    context = {
        # 'title': 'Member Dashboard',
        # 'borrowed_books': Book.objects.filter(borrower=request.user),
        # 'reading_history': ReadingHistory.objects.filter(user=request.user),
    }
    return render(request, 'member_dashboard.html', context)
