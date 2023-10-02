from typing import Any
from django.db.models.query import QuerySet
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from movies.models import Movie, Category


class IndexView(ListView):
    model = Movie
    template_name = "movies/index.html"
    queryset = Movie.published.select_related("category")
    context_object_name = "movies"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Movify"
        return context


class CategoryListView(ListView):
    model = Movie
    template_name = "movies/movie-list.html"
    context_object_name = "movies"
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.kwargs.get("category")
        context["title"] = Category.objects.get(slug=category).title
        return context

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        category = self.kwargs.get("category")
        return queryset.filter(category__slug=category)


class MovieDetailView(DetailView):
    model = Movie
    template_name = "movies/movie-detail.html"
    context_object_name = "movie"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.title
        return context
