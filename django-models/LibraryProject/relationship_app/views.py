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
from django.contrib.auth.decorators import login_required
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