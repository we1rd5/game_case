from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from Portfolio.models import User
import hashlib


def main_page(request):
    return render(request, "main.html")


def signup(request):
    return render(request, "signup.html")


def signup_post(request):
    login = request.POST.get("login", "UNDEFINED_LOGIN")
    password = request.POST.get("password", "UNDEFINED_PASSWORD")
    user = User(login=login, password=hashlib.sha256(bytes(password, encoding="utf-8")).hexdigest())
    if login == "UNDEFINED_LOGIN" or login == "":
        return HttpResponse("login error", status=422)
    if len(login) > 20:
        return HttpResponse("login is too large", status=431)
    if password == "UNDEFINED_PASSWORD" or password == "":
        return HttpResponse("password error", status=422)
    if User.objects.filter(login=login):
        return HttpResponse("already exist", status=422)
    user.save()
    response = HttpResponseRedirect("/profile")
    response.set_cookie("GameCaseLogin", login)
    response.set_cookie("GameCasePasswordHash", hashlib.sha256(bytes(password, encoding="utf-8")).hexdigest())
    return response


def login(request):
    login = request.COOKIES.get("GameCaseLogin")
    if login is not None and User.objects.filter(login=login).exists():
        password_hash = request.COOKIES.get("GameCasePasswordHash")
        if password_hash == User.objects.get(login=login).password:
            return HttpResponseRedirect("/profile")
    return render(request, "login.html")


def login_post(request):
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
    if name == None or name == request.COOKIES.get("GameCaseLogin"):
        login = request.COOKIES.get("GameCaseLogin")
        if login is not None:
            password_hash = request.COOKIES.get("GameCasePasswordHash")
            if password_hash == User.objects.get(login=login).password:
                return HttpResponse(login + " " + "your account")
        else:
            return HttpResponseRedirect("/login", status=303)
    else:
        return HttpResponse(name)