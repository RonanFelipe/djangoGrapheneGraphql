import graphene
from graphene_django import DjangoObjectType
from .models import Movie, Actor, ActorFilms, Director, DirectorFilms
from django.db.models import Q


class MovieType(DjangoObjectType):
    class Meta:
        model = Movie


class ActorType(DjangoObjectType):
    class Meta:
        model = Actor


class ActorMovieType(DjangoObjectType):
    class Meta:
        model = ActorFilms


class DirectorType(DjangoObjectType):
    class Meta:
        model = Director


class DirectorMoviesType(DjangoObjectType):
    class Meta:
        model = DirectorFilms


class Query(graphene.ObjectType):
    movies = graphene.List(MovieType, search=graphene.String())
    actors = graphene.List(ActorType, search=graphene.String())
    actors_movies = graphene.List(ActorMovieType)
    directors = graphene.List(DirectorType, search=graphene.String())
    directors_movies = graphene.List(DirectorMoviesType)

    def resolve_movies(self, info, search=None, **kwargs):
        if search:
            filter = (
                Q(name__icontains=search) | Q(genre__icontains=search)
            )
            return Movie.objects.filter(filter)
        return Movie.objects.all()

    def resolve_actors(self, info, search=None, **kwargs):
        if search:
            filter = (
                Q(name__icontains=search)
            )
            return Actor.objects.filter(filter)
        return Actor.objects.all()

    def resolve_actors_movies(self, info, **kwargs):
        return ActorFilms.objects.all()

    def resolve_directors(self, info, search=None, **kwargs):
        if search:
            filter = (
                Q(name__icontains=search)
            )
            return Director.objects.filter(filter)
        return Director.objects.all()

    def resolve_directors_movies(self, info, **kwargs):
        return DirectorFilms.objects.all()


class CreateMovie(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()
    year = graphene.Int()
    note_imdb = graphene.Float()
    genre = graphene.String()
    duration = graphene.Int()

    class Arguments:
        name = graphene.String()
        year = graphene.Int()
        note_imdb = graphene.Float()
        genre = graphene.String()
        duration = graphene.Int()

    def mutate(self, info, name, year, note_imdb, genre, duration):
        movie = Movie(
            name=name,
            year=year,
            genre=genre,
            note_imdb=note_imdb,
            duration=duration
        )
        movie.save()

        return CreateMovie(
            id=movie.id,
            name=movie.name,
            note_imdb=movie.note_imdb,
            genre=movie.genre,
            duration=movie.duration,
            year=movie.year,
        )


class CreateActor(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()
    age = graphene.Int()
    sexo = graphene.String()

    class Arguments:
        name = graphene.String()
        age = graphene.Int()
        sexo = graphene.String()

    def mutate(self, info, name, age, sexo):
        actor = Actor(
            name=name,
            age=age,
            sexo=sexo
        )
        actor.save()

        return CreateActor(
            id=actor.id,
            name=actor.name,
            age=actor.age,
            sexo=actor.sexo,
        )


class CreateActorMovies(graphene.Mutation):
    actor_id = graphene.Field(ActorType)
    movie_id = graphene.Field(MovieType)

    class Arguments:
        actor_id = graphene.Int()
        movie_id = graphene.Int()

    def mutate(self, info, actor_id, movie_id):
        actor_id = Actor.objects.filter(id=actor_id).first()
        if not actor_id:
            raise Exception('Actor invalid')
        movie_id = Movie.objects.filter(id=movie_id).first()
        if not movie_id:
            raise Exception('Movie Invalid')

        ActorFilms.objects.create(
            actor_id=actor_id,
            movie_id=movie_id,
        )

        return CreateActorMovies(actor_id=actor_id, movie_id=movie_id)


class CreateDirector(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()
    is_alive = graphene.Boolean()

    class Arguments:
        name = graphene.String()
        is_alive = graphene.Boolean()

    def mutate(self, info, name, is_alive):
        director = Director(name=name, is_alive=is_alive)
        director.save()

        return CreateDirector(
            id=director.id,
            name=director.name,
            is_alive=director.is_alive,
        )


class CreateDirectorMovies(graphene.Mutation):
    director_id = graphene.Field(DirectorType)
    movie_id = graphene.Field(MovieType)

    class Arguments:
        director_id = graphene.Int()
        movie_id = graphene.Int()

    def mutate(self, info, director_id, movie_id):
        director_id = Director.objects.filter(id=director_id).first()
        if not director_id:
            raise Exception('Director Invalid')
        movie_id = Movie.objects.filter(id=movie_id).first()
        if not movie_id:
            raise Exception('Movie Invalid')

        DirectorFilms.objects.create(
            director_id=director_id,
            movie_id=movie_id
        )

        return CreateDirectorMovies( director_id=director_id, movie_id=movie_id)


class Mutation(graphene.ObjectType):
    create_movie = CreateMovie.Field()
    create_actor = CreateActor.Field()
    create_actor_movie = CreateActorMovies.Field()
    create_director = CreateDirector.Field()
    create_director_movie = CreateDirectorMovies.Field()
