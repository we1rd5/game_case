from django.db import models


class User(models.Model):
    login = models.CharField(max_length=20)
    email = models.CharField(max_length=128)
    password = models.CharField(max_length=64)


class UserDesc(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=95)
    about = models.CharField(max_length=350)
    photo = models.ImageField(upload_to="user_photos")


class Game(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=112)
    repo = models.CharField(max_length=128, default="")
    rating = models.FloatField()


class GamePhoto(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="game")
    photo = models.ImageField(upload_to=f"game_photos/")


class Rate(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user_login = models.CharField(max_length=20)
    value = models.IntegerField()