from . import models
from django.contrib import admin
from author.models import Author
from django.contrib.admin import ModelAdmin, SimpleListFilter


class AuthorInlineAdmin(admin.TabularInline):
    model = Author.books.through


class AuthorsFilter(SimpleListFilter):
    title = "Authors"  # a label for our filter
    parameter_name = "authors"  # you can put anything here

    def lookups(self, request, model_admin):
        # This is where you create filter options; we have two:
        res = []
        for author in Author.books.through.objects.all():
            value_to_append = (str(author.author.id),
                               str(author.author.name + ' '
                               + author.author.surname))
            if value_to_append not in res:
                res.append(value_to_append)
        return res
        #     [
        #     (str(author.author.id), str(author.author.name + ' '
        #                                 + author.author.surname))
        #     for author in Author.books.through.objects.all()
        # ]

    def queryset(self, request, queryset):
        # This is where you process parameters selected by use via filter options:

        for item in Author.books.through.objects.all():
            if self.value() == str(item.author.id):
                # Get websites that have at least one page.
                return queryset.distinct().filter(authors__in=self.value())

        if self.value():
            # Get websites that don't have any pages.
            return queryset.distinct().filter(authors__isnull=True)





@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):

    list_display = ['pk', 'upper_case_name', 'count', ]
    list_display_links = ['upper_case_name']

    @admin.display(description='Name')
    def upper_case_name(self, obj):
        return ("%s" % (obj.name,)).upper()
    # list_display = ['pk', 'name', 'count']
    list_filter = ['id', 'name', AuthorsFilter]
    search_fields = ['name']
    list_editable = ['count']

    filter_vertical = ['authors']
    # fields = ('count',)
    fieldsets = (
        ('ToChange', {
            'fields': ('date_of_issue', )
        }),
        ('Don\'t change', {
            'fields': ('name', 'publication_year')
        })
    )
    ordering = ['pk']

    inlines = [AuthorInlineAdmin]




# admin.site.register(models.Book, BookAdmin)
