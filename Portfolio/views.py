from django.shortcuts import render, HttpResponse
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
        return HttpResponse("login error")
    if password == "UNDEFINED_PASSWORD" or password == "":
        return HttpResponse("password error")
    if User.objects.filter(login=login):
        return HttpResponse("already exist")
    user.save()
    return HttpResponse("success")