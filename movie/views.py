from rest_framework import viewsets
from djangoMovies import settings
from .models import Movie, Actor, Director
from .serializers import MovieSerializer, ActorSerializer, DirectorSerializer

# Create your views here.


class MovieSet(viewsets.ModelViewSet):
    print('Im here')
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class ActorSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class DirectorSet(viewsets.ModelViewSet):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
