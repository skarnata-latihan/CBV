from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect
from django.views.generic import ListView, FormView, CreateView, UpdateView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from books.models import Books
from .forms import AddForm
from django.db.models import F
from django.utils import timezone
from django.contrib.auth.mixins import PermissionRequiredMixin


# class AddBookView(FormView):
#     template_name = 'add.html'
#     form_class = AddForm
#     success_url = '/books/'
#
#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)

class UserAccessMixin(PermissionRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if (not self.request.user.is_authenticated):
            return redirect_to_login(self.request.get_full_path(),
                                     self.get_login_url(), self.get_redirect_field_name())
        if not self.has_permission():
            return redirect('/books')
        return super(UserAccessMixin, self).dispatch(request, *args, **kwargs)


class BookEditView(UserAccessMixin, UpdateView):
    raise_exception = False
    permission_required = ('books.change_books', 'books.add_books', 'books.view_books')
    permission_denied_message = ""
    login_url = '/books/'
    redirect_field_name = 'next'
    model = Books
    form_class = AddForm
    template_name = 'add.html'
    success_url = '/books/'


class AddBookView(CreateView):
    model = Books
    form_class = AddForm
    template_name = 'add.html'
    success_url = '/books/'

    def get_initial(self, *args, **kwargs):
        initial = super().get_initial(**kwargs)
        initial['title'] = 'Enter Title'
        return initial


class IndexView(ListView):
    model = Books
    template_name = 'home.html'
    context_object_name = 'books'
    paginate_by = 3  # Pagination over-write

    # queryset = Books.objects.all()[:2]
    # queryset = Books.objects.filter(title='')

    # Alturnative override class methods.
    # def get_queryset(self):
    # return Books.objects.all()[:3]

    # Alturnative override class methods.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time'] = timezone.now()
        return context


class GenreView(ListView):
    model = Books
    template_name = 'home.html'
    context_object_name = 'books'
    paginate_by = 2  # Pagination over-write

    def get_queryset(self, *args, **kwargs):
        return Books.objects.filter(genre__icontains=self.kwargs.get('genre'))


# class IndexView(TemplateView):
#     template_name = "home.html"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['books'] = Books.objects.all()
#         return context


class BookDetailView(DetailView):
    model = Books
    template_name = 'book-detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        post = Books.objects.filter(slug=self.kwargs.get('slug'))
        post.update(count=F('count') + 1)

        context['time'] = timezone.now()

        return context
