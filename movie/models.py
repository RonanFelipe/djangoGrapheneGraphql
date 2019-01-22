from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

# Create your models here.


class MyUserManager(BaseUserManager):
    def create_user(
            self,
            cpf,
            first_name,
            last_name,
            password=None
    ):
        """
        Cria e salva um usuário com o cpf, primeiro nome, último nome, data de nascimento e senha.
        """
        if not cpf:
            raise ValueError("Número de CPF será usado para login.")

        user = self.model(
            cpf=cpf,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
            self,
            cpf,
            first_name,
            last_name,
            password
    ):
        """
        Cria e salva superuser, com cpf, primeiro nome, último nome, data de nascimento e senha.
        """
        user = self.create_user(
            cpf,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    cpf = models.BigIntegerField(verbose_name="CPF", unique=True)
    first_name = models.CharField(verbose_name="Primeiro nome", max_length=255)
    last_name = models.CharField(verbose_name="Sobrenome", max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "cpf"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.first_name + " " + self.last_name

    def get_full_name(self):
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        """Método para tratar se o usuário possui permissões especiais"""
        return True

    def has_module_perms(self, app_label):
        """Método para tratar se o usuário possui permissão para ver a label app"""
        return True

    @property
    def is_staff(self):
        """Se o usuário for um membro do staff?"""
        return self.is_admin


class Movie(models.Model):
    name = models.CharField(verbose_name='Nome do filme', max_length=50)
    year = models.IntegerField(verbose_name='ano do filme')
    note_imdb = models.FloatField(verbose_name='nota IMDB', blank=True, null=True)
    genre = models.CharField(verbose_name='Genero do filme', max_length=255, blank=True, null=True)
    duration = models.IntegerField(verbose_name='duração do filme')

    def __str__(self):
        return self.name


class Actor(models.Model):
    name = models.CharField(verbose_name='nome', max_length=50)
    age = models.IntegerField(verbose_name='idade', blank=True, null=True)
    sexo = models.CharField(verbose_name='Sexo', blank=True, null=True, max_length=1)

    def __str__(self):
        return self.name


class ActorFilms(models.Model):
    actor_id = models.ForeignKey(Actor, on_delete=models.CASCADE)
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)


class Director(models.Model):
    name = models.CharField(verbose_name='nome do diretor', max_length=50)
    is_alive = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class DirectorFilms(models.Model):
    director_id = models.ForeignKey(Director, on_delete=models.CASCADE)
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
