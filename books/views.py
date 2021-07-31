from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from .models import Books
from .forms import BooksForm
from django.views import View


class BookListView(View):
    template_name = 'books/books_list.html'
    queryset = []

    def get(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect('/login')

        filtr = {"user" : request.user}

        temp = request.GET

        for k, v in temp.items():
            if v:
                filtr[k + "__contains"] = v

        if filtr:
            self.queryset = Books.objects.filter(**filtr)

        books_counter = len(self.queryset)

        content = {
            "object_list" : self.queryset,
            "books_counter" : books_counter,
        }

        return render(request, self.template_name, content)


    def post(self, request, *args, **kwargs):

        filtr = {"user" : request.user}

        if request.POST.get("create"):

            form = BooksForm(request.POST)

            if form.is_valid():
                form.instance.user = request.user
                form.save()
                self.queryset = Books.objects.filter(**filtr)

        elif request.POST.get("update"):

            filtr = {"user" : request.user}

            id = request.POST.get("update")

            obj = get_object_or_404(Books, id=id)

            form = BooksForm(request.POST, instance=obj)

            if form.is_valid():
                form.instance.user = request.user
                form.save()
                self.queryset = Books.objects.filter(**filtr)

        elif request.POST.get("delete"):

            filtr = {"user" : request.user}

            id  = request.POST.get("delete")

            obj = get_object_or_404(Books, id=id)

            if obj:
                obj.delete()
                self.queryset = Books.objects.filter(**filtr)

        books_counter = len(self.queryset)

        content = {
            "object_list" : self.queryset,
            "books_counter" : books_counter,
        }

        return render(request, self.template_name, content)





