from django.db import models
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(max_length=128, unique=True)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self) -> str:
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse("movies:category", kwargs={"category": self.slug})


class Genre(models.Model):
    title = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(max_length=128, unique=True)

    class Meta:
        verbose_name = "genre"
        verbose_name_plural = "genres"

    def __str__(self) -> str:
        return f"{self.title}"


class Country(models.Model):
    title = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(max_length=128, unique=True)

    class Meta:
        verbose_name = "country"
        verbose_name_plural = "countries"

    def __str__(self) -> str:
        return f"{self.title}"


class Career(models.Model):
    position = models.CharField(max_length=32, unique=True)
    slug = models.SlugField(max_length=128, unique=True)

    class Meta:
        verbose_name = "career"
        verbose_name_plural = "career"

    def __str__(self) -> str:
        return f"{self.position}"


class Celebrity(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    height = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to="celebrities/")
    career = models.ManyToManyField(Career, related_name="celebrities")
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="celebrities")
    slug = models.SlugField(max_length=128, unique=True)

    class Meta:
        verbose_name = "celebrity"
        verbose_name_plural = "celebrities"

    def __str__(self) -> str:
        return f"{self.name}"


class PublishManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(status=Movie.Status.PUBLISHED)


class Movie(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    title = models.CharField(max_length=128)
    tagline = models.CharField(max_length=255, default="")
    description = models.TextField()
    poster = models.ImageField(upload_to="movies/")
    link = models.URLField(max_length=128, unique=True)
    year_of_production = models.PositiveSmallIntegerField()
    country = models.ManyToManyField(Country, related_name="movies")
    director = models.ManyToManyField(Celebrity, related_name="directors")
    actor = models.ManyToManyField(Celebrity, related_name="actors")
    genre = models.ManyToManyField(Genre, related_name="movies")
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="movies"
    )
    slug = models.SlugField(max_length=155, unique=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)

    objects = models.Manager()
    published = PublishManager()

    class Meta:
        verbose_name = "movie"
        verbose_name_plural = "movies"

    def __str__(self) -> str:
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse("movies:movie", kwargs={"slug": self.slug})
