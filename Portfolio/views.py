from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from Portfolio.models import User


def main_page(request):
    return render(request, "main.html")


def signup(request):
    return render(request, "signup.html")


def signup_post(request):
    login = request.POST.get("login", "UNDEFINED_LOGIN")
    password = request.POST.get("password", "UNDEFINED_PASSWORD")
    user = User(login=login, password=hash(password))
    if login == "UNDEFINED_LOGIN" or login == "":
        return HttpResponse("login error", status=422)
    if len(login) > 20:
        return HttpResponse("login is too large", status=431)
    if password == "UNDEFINED_PASSWORD" or password == "":
        return HttpResponse("password error", status=422)
    if User.objects.filter(login=login):
        return HttpResponse("already exist", status=422)
    user.save()
    response = HttpResponse("success")
    response.set_cookie("GameCaseLogin", login)
    response.set_cookie("GameCasePasswordHash", hash(password))
    return response


def login(request):
    login = request.COOKIES.get("GameCaseLogin")
    if login is not None and User.objects.filter(login=login).exists():
        password_hash = request.COOKIES.get("GameCasePasswordHash")
        if int(password_hash) == User.objects.get(login=login).password:
            return HttpResponse("success")
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
    if hash(password) == User.objects.get(login=login).password:
        return HttpResponse("success")
    return HttpResponse("incorrect password", status=422)
