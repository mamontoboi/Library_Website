from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import FormView
from .forms import *
from . import models
from author.serializers import AuthorSerializer
from rest_framework import viewsets


class AuthorAPIView(viewsets.ModelViewSet):
    serializer_class = AuthorSerializer
    queryset = models.Author.objects.all()



def create_author(request):
    if request.method == 'POST':
        data = request.POST
        author = models.Author.create(data['name'],
                                      data['surname'],
                                      data['patronymic'])
        return render(request, 'author/create_author.html', {'author': author})
    return render(request, 'author/create_author.html')


# show information about all authors (librarian)
def show_authors(request):
    authors = models.Author.get_all()
    return render(request, 'author/show_authors.html', {'authors': authors})


# provide the ability to remove the author if he is not attached to
# any book (librarian)
def remove_author(request):
    authors = models.Author.get_all()
    if request.method == 'POST':
        author_id = request.POST['authors']
        if author_id != 'False':
            author = models.Author.objects.get(id=author_id)
            if not len(author.books.all()):
                models.Author.delete_by_id(author_id)
                authors = models.Author.get_all()
            return render(request, 'author/remove_author.html',
                      {'authors': authors,
                       'deleted_author': author})

    return render(request, 'author/remove_author.html', {'authors': authors})


class AuthorFormView(FormView):
    """Serves for transition of information from front-end into form of model Author"""
    form_class = AuthorFormModel
    template_name = 'author/create_author.html'
    success_url = '/author/create_author/success/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


def success_author_creation(request):
    """Notification in case of successful creation of a new author."""
    return HttpResponse("<script>alert ('Congratulations! The author was successfully created!'); "
                        "window.location = '/author/show_authors/';</script>")


def update_author(request, author_id=None):
    if author_id:
        try:
            author = Author.objects.get(pk=author_id)
        except:
            return redirect('/author/show_authors/')
        else:
            form = UpdateAuthorFormModel(initial=
                                        {'name': author.name,
                                         'surname': author.surname,
                                         'patronymic': author.patronymic,
                                         # 'books': author.books,
                                         })

            if request.method == 'POST':
                form = UpdateAuthorFormModel(request.POST)

                if form.is_valid():
                    data = form.cleaned_data
                    author.name = data.get('name')
                    author.surname = data.get('surname')
                    # Check added due to not null constraint
                    if data.get('patronymic'):
                        author.patronymic = data.get('patronymic')
                    else:
                        author.patronymic = ''
                    author.save()
                    print("cleaned data:", form.cleaned_data)
                    return redirect('/author/show_authors/')

            else:
                return render(request, 'author/update_author.html', {'form': form})
    else:
        return redirect('/author/show_authors/')