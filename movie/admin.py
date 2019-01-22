from django.contrib import admin
from .models import MyUser, Movie, Actor, Director, ActorFilms, DirectorFilms

# Register your models here.
admin.site.register(MyUser)
admin.site.register(Movie)
admin.site.register(Actor)
admin.site.register(Director)
admin.site.register(ActorFilms)
admin.site.register(DirectorFilms)
