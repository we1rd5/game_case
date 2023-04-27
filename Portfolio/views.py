from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from Portfolio.models import User, Game, UserDesc, GamePhoto
import hashlib


def main_page(request):
    return render(request, "main.html")


def signup(request):
    if request.method == "GET":
        return render(request, "signup.html")
    if request.method == "POST":
        login = request.POST.get("login", "UNDEFINED_LOGIN")
        email = request.POST.get("email", "UNDEFINED_EMAIL")
        password = request.POST.get("password", "UNDEFINED_PASSWORD")
        repeat_password = request.POST.get("repeat_password", "UNDEFINED_PASSWORD")
        user = User(login=login, email=email, password=hashlib.sha256(bytes(password, encoding="utf-8")).hexdigest())
        if login == "UNDEFINED_LOGIN" or login == "":
            return HttpResponse("login error", status=422)
        if len(login) > 20:
            return HttpResponse("login is too large", status=431)
        if password == "UNDEFINED_PASSWORD" or password == "":
            return HttpResponse("password error", status=422)
        if email == "UNDEFINED_EMAIL" or email == "":
            return HttpResponse("email error", status=422)
        if password != repeat_password:
            return HttpResponse("Passwords does not match. Try again", status=431)
        if User.objects.filter(login=login):
            return HttpResponse("login already exists", status=422)
        if User.objects.filter(email=email):
            return HttpResponse("email already exists", status=422)
        user.save()
        response = HttpResponseRedirect("/profile")
        response.set_cookie("GameCaseLogin", login)
        response.set_cookie("GameCasePasswordHash", hashlib.sha256(bytes(password, encoding="utf-8")).hexdigest())
        return response


def login(request):
    if request.method == "GET":
        login = request.COOKIES.get("GameCaseLogin")
        if login is not None and User.objects.filter(login=login).exists():
            password_hash = request.COOKIES.get("GameCasePasswordHash")
            if password_hash == User.objects.get(login=login).password:
                return HttpResponseRedirect("/profile")
        return render(request, "login.html")
    if request.method == "POST":
        login = request.POST.get("login", "UNDEFINED_LOGIN")
        password = request.POST.get("password", "UNDEFINED_PASSWORD")
        if login == "UNDEFINED_LOGIN" or login == "":
            return HttpResponse("login error", status=422)
        if password == "UNDEFINED_PASSWORD" or password == "":
            return HttpResponse("password error", status=422)
        if not User.objects.filter(login=login).exists():
            return HttpResponse("no account", status=422)
        if hashlib.sha256(bytes(password, encoding="utf-8")).hexdigest() == User.objects.get(login=login).password:
            response = HttpResponseRedirect("/profile")
            response.set_cookie("GameCaseLogin", login)
            response.set_cookie("GameCasePasswordHash", hashlib.sha256(bytes(password, encoding="utf-8")).hexdigest())
            return response
        return HttpResponse(f"incorrect password {hashlib.sha256(bytes(password, encoding='utf-8')).hexdigest()}", status=422)


def profile(request, name=None):
    if name is None or name == request.COOKIES.get("GameCaseLogin"):
        login = request.COOKIES.get("GameCaseLogin")
        if login is not None:
            password_hash = request.COOKIES.get("GameCasePasswordHash")
            if password_hash == User.objects.get(login=login).password:
                return HttpResponse(login + " " + "your account")
        else:
            return HttpResponseRedirect("/login", status=303)
    else:
        return HttpResponse(name)


def game(request, id=0):
    if id == 0 or not Game.objects.filter(id=id).exists():
        return HttpResponseRedirect('/')
    game = Game.objects.get(id=id)
    return HttpResponse(f"{game.name}, {game.description}, {game.author.login}")


def load_game(request):
    if request.method == "GET":
        login = request.COOKIES.get("GameCaseLogin")
        if login is not None and User.objects.filter(login=login).exists():
            password_hash = request.COOKIES.get("GameCasePasswordHash")
            if password_hash == User.objects.get(login=login).password:
                return render(request, "game_load.html")
            return HttpResponse("Password error. Clean cookies and try again", status=422)
        return HttpResponseRedirect("/login", status=303)
    if request.method == "POST":
        login = request.COOKIES.get("GameCaseLogin")
        if login is None or not User.objects.filter(login=login).exists():
            return HttpResponse("Error. Clean cookies and try again", status=422)
        user = User.objects.get(login=login)
        game = Game(author=user,
                    name=request.POST.get("name", "UNDEFINED_NAME"),
                    description=request.POST.get("desc", "UNDEFINED_DESCRIPTION"),
                    rating=0.0)
        game.save()
        for e in request.FILES.getlist("photos"):
            picture = GamePhoto(game=game, photo=e)
            picture.save()
        return HttpResponseRedirect(f"/game/{game.id}")