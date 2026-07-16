from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout

from django.shortcuts import render
from django.shortcuts import redirect

# Create your views here.
def login_usuario(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    mensaje = None

    if request.method == "POST":

        username = request.POST.get("username")

        password = request.POST.get("password")

        usuario = authenticate(
            request,
            username=username,
            password=password
        )

        if usuario is not None:

            login(request, usuario)

            return redirect("dashboard")

        mensaje = "Usuario o contraseña incorrectos."

    return render(
        request,
        "usuarios/login.html",
        {
            "mensaje": mensaje
        }
    )


def logout_usuario(request):

    logout(request)

    return redirect("login")