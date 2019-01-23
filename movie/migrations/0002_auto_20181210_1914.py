# Generated by Django 2.1.4 on 2018-12-10 21:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='nome')),
                ('age', models.IntegerField(blank=True, null=True, verbose_name='idade')),
            ],
        ),
        migrations.CreateModel(
            name='ActorFilms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actor_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie.Actor')),
            ],
        ),
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='nome do diretor')),
                ('is_alive', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='DirectorFilms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('director_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie.Director')),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Nome do filme')),
                ('year', models.IntegerField(verbose_name='ano do filme')),
                ('note_imdb', models.FloatField(blank=True, null=True, verbose_name='nota IMDB')),
                ('genre', models.CharField(blank=True, max_length=255, null=True, verbose_name='Genero do filme')),
                ('duration', models.IntegerField(verbose_name='duração do filme')),
            ],
        ),
        migrations.AddField(
            model_name='directorfilms',
            name='movie_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie.Movie'),
        ),
        migrations.AddField(
            model_name='actorfilms',
            name='movie_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie.Movie'),
        ),
    ]