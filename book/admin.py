from django.contrib import admin
from .models import Book,BorrowedBook   
class BookAdmin(admin.ModelAdmin):  
    list_display = ('itbook', 'title', 'author', 'published_date', 'quantity', 'status')
    search_fields = ('itbook', 'title', 'author', 'published_date', 'quantity', 'status')
admin.site.register(Book, BookAdmin)       
admin.site.register(BorrowedBook)   
# Register your models here.