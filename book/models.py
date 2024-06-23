from django.db import models
from django.contrib.auth.models import User 
class Book(models.Model):
    AVAILABLE = 'available'
    BORROWED = 'borrowed'
    STATUS_CHOICES = [
        (AVAILABLE, 'Available'),
        (BORROWED, 'Borrowed'),
    ]   
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    itbook = models.CharField(max_length=100, unique=True)
    published_date = models.DateField()
    description = models.TextField()    
    quantity = models.IntegerField()
    image = models.ImageField(upload_to='book_images')
    category = models.CharField(max_length=255)  # Thể loại sách
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,
        default=AVAILABLE,
    )        
def __str__(self):
        return self.title   
class BorrowedBook(models.Model):   
    borrower = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)   
    def __str__(self):
        return f'{self.user.username} borrowed {self.book.title}'