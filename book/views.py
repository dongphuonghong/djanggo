from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils import timezone
from django.contrib import messages
from .models import Book, BorrowedBook
from .forms import BorrowedBookForm, CreationFormUser, emailAuthenticationForm
def home(request):
    return render(request, 'home.html')
def book_list(request):
    query = request.GET.get('q')
    if query:
        books = Book.objects.filter(title__icontains=query) | Book.objects.filter(author__icontains=query)
    else:
        books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    user_has_borrowed_book = book.borrowedbook_set.filter(borrower=request.user, return_date__isnull=True).exists()
    return render(request, 'book_detail.html', {'book': book, 'user_has_borrowed_book': user_has_borrowed_book})
@login_required
def borrow_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if book.quantity <= 0:
        messages.error(request, 'Book is not available now!')
        return redirect('book_detail', book_id=book.id)
    if request.method == 'POST':
        form = BorrowedBookForm(request.POST)
        if form.is_valid():
            borrowed_book = form.save(commit=False)
            borrowed_book.book = book
            borrowed_book.borrower = request.user
            borrowed_book.borrowed_date = timezone.now()
            borrowed_book.save()
            book.quantity -= 1
            book.save()
            messages.success(request, 'Book borrowed successfully!')
            return redirect('home')
    else:
        form = BorrowedBookForm()
    return render(request, 'borrow_book.html', {'form': form, 'book': book})
@login_required
def return_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    borrowed_book = BorrowedBook.objects.filter(book=book, borrower=request.user, return_date__isnull=True).first()
    if borrowed_book:
        borrowed_book.return_date = timezone.now()
        borrowed_book.save()
        book.quantity += 1
        book.save()
        messages.success(request, 'Book returned successfully!')
    else:
        messages.error(request, 'You have not borrowed this book.')
    return redirect('book_detail', book_id=book.id)
def register(request):
    if request.method == 'POST':
        form = CreationFormUser(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, 'Register successfully!')
            return redirect('home')
    else:
        form = CreationFormUser()
    return render(request, 'register/register.html', {'form': form})
def login(request):
    if request.method == 'POST':
        form = emailAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, 'Login successfully!')
            return redirect('home')
    else:
        form = emailAuthenticationForm()
    return render(request, 'register/login.html', {'form': form})
def logout(request):
    auth_logout(request)
    return redirect('home')