from django.contrib import admin
from django.utils.safestring import mark_safe

from movies.models import Career, Category, Celebrity, Country, Genre, Movie


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    list_display_links = ("title",)
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("title",)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("title",)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("title",)


@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = ("position", "slug")
    prepopulated_fields = {"slug": ("position",)}
    ordering = ("position",)


@admin.register(Celebrity)
class CelebrityAdmin(admin.ModelAdmin):
    list_display = ("name", "display_image", "date_of_birth", "display_career")
    list_filter = ("career", "country")
    fields = (
        ("name", "slug"),
        "description",
        ("date_of_birth", "height"),
        ("country", "career"),
        ("image", "display_image"),
    )
    search_fields = ("name", "career__position", "country__title")
    readonly_fields = ("display_image",)
    prepopulated_fields = {"slug": ("name",)}
    raw_id_fields = ("career", "country")
    ordering = ("name",)

    def display_career(self, obj):
        return ", ".join(career.position for career in obj.career.all())

    def display_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="70"')

    display_career.short_description = "career"
    display_image.short_description = "image"


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "display_genre",
        "display_image",
        "display_directors",
        "status",
    )
    list_filter = ("category", "status")
    fields = (
        ("title", "tagline"),
        "description",
        ("poster", "link"),
        ("country", "year_of_production"),
        ("director", "actor"),
        ("category", "genre"),
        "slug",
        "status",
    )
    search_fields = ("title", "year_of_production", "category__title", "genre__title")
    readonly_fields = ("display_image",)
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ("category", "genre", "director", "actor", "country")
    ordering = ("status", "title", "year_of_production")

    def display_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="50" height="70"')

    def display_genre(self, obj):
        return ", ".join(genre.title for genre in obj.genre.all())

    def display_directors(self, obj):
        return ", ".join(director.name for director in obj.director.all())

    display_image.short_description = "poster"
    display_genre.short_description = "genre"
    display_directors.short_description = "directors"
