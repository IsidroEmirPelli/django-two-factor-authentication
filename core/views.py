from django.core.cache import cache
from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required


from .utils import (
    generate_code,
    send_email_two_factor,
    encode_token_info,
    decode_token_info,
)

# Create your views here.


class Login(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse("dashboard"))
        return render(request, "login.html")

    def post(self, request):
        user = authenticate(
            username=request.POST.get("username"), password=request.POST.get("password")
        )
        token = encode_token_info(user.email, user.pk)
        if user:
            cache.set(token, True, 120)
            return redirect(reverse("two_factor", kwargs={"token": token}))
        else:
            return render(
                request, "login.html", {"message": "Username or password is incorrect "}
            )


class TwoFactor(View):
    def get(self, request, token):
        if request.user.is_authenticated:
            return redirect(reverse("dashboard"))
        if not cache.get(token):
            return redirect(reverse("login"))
        code = generate_code()
        decoded = decode_token_info(token)
        print(decoded)
        pk = decoded["user"]
        cache.set(f"token_{pk}", code, 60)
        send_email_two_factor(decoded["email"], code)
        return render(request, "2fa.html")

    def post(self, request, token):
        pk = decode_token_info(token)["user"]
        code = request.POST.get("code")
        code_cache = cache.get(f"token_{pk}")
        cache.delete(token)
        if code == code_cache:
            User = get_user_model()  # Obtener el modelo de usuario de Django
            user = User.objects.get(
                pk=pk
            )  # Obtener el objeto de modelo de Django correspondiente al valor de pk
            login(
                request, user
            )  # Pasar el objeto de modelo de Django a la función login
            cache.delete(f"token_{pk}")
            return redirect(reverse("dashboard"))
        else:
            print("Error")
            return redirect(reverse("login"), {"msg": "Error"})


class Dashboard(LoginRequiredMixin, TemplateView):

    template_name = "dashboard.html"
    login_url = "login"
    redirect_field_name = ""
