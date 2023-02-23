from django.contrib import admin
from .models import Author
from book.models import Book

class AuthorInlineAdmin(admin.TabularInline):
    model = Book.authors.through
    # model = Author.books.through


@admin.register(Author)
class AdminAuthor(admin.ModelAdmin):
    # exclude = ('id',)
    list_display = [field.name for field in Author._meta.fields]
    ordering = ['id']
    list_filter = [field.name for field in Author._meta.fields]
    search_fields = [field.name for field in Author._meta.fields]
    # prepopulated_fields = {"patronymic": ("name",)}
    # save_as = True
    # save_as_continue = True
    # save_on_top = True
    fieldsets = (
        (None, {
            'fields': ['name', 'surname', 'patronymic']
        }),
    )

    inlines = [AuthorInlineAdmin]

    # fields = [field for field in Author._meta.fields]