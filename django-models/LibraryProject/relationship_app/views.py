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
@user_passes_test(User.userprofile.role == UserProfile.Admin)
def admin_view(request):
    return render(request, 'relationship_app/Admin.html')

# Librarian View
@login_required
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/Librarian.html')

# Member View
@login_required
@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/Member.html')




# # Check if the user is a Librarian
# def is_librarian(user):
#     return user.userprofile.role == UserProfile.Adm

# # Check if the user is a Librarian
# def is_librarian(user):
#     return user.userprofile.role == UserProfile.Librarians

# # View for Librarians
# @login_required
# @user_passes_test(is_librarian)
# def librarian_view(request):
#     return render(request, 'relationship_app/librarian_view.html')

# # Check if the user is a Member
# def is_member(user):
#     return user.userprofile.role == UserProfile.Members





# # View for Members

# # @login_required
# @user_passes_test(lambda u: u.get_group_permissions(UserProfile.ROLE_CHOICES[0].role))

# def Admin(request):
#     return render(request, 'relationship_app/admin.html')
# @user_passes_test(is_member)
# def Admin(request):
#     return render(request, 'relationship_app/admin.html')




# # @login_required
# @user_passes_test(lambda u: u.get_group_permissions(UserProfile.ROLE_CHOICES[1].role))
# def Librarian(request):
#     return render(request, 'relationship_app/librarian.html')

# # @login_required
# @user_passes_test(lambda u: u.get_group_permissions(UserProfile.ROLE_CHOICES[2].role))
# def Member(request):
#     return render(request, 'relationship_app/member.html')

