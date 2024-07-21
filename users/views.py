from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetCompleteView, PasswordResetView, \
    PasswordResetConfirmView, PasswordChangeView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

from users.forms import UserCreateForm


class SignUpView(View):
    def get(self, request):
        create_form = UserCreateForm()
        context = {
            "form": create_form
        }
        return render(request, "users/register.html", context)

    def post(self, request):
        create_form = UserCreateForm(data=request.POST)
        if create_form.is_valid():
            create_form.save()
            return redirect("users:login")
        else:
            context = {
                "form": create_form
            }
            return render(request, "users/register.html", context)


class LoginView(View):
    def get(self, request):
        login_form = AuthenticationForm()
        context = {
            "login_form": login_form
        }
        return render(request, "users/login.html", context)

    def post(self, request):
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            messages.info(request, "You have successfully login.")
            return redirect("landing_page")
        else:
            context = {
                "login_form": login_form
            }
            return render(request, "users/login.html", context)



class LogOutView(LoginRequiredMixin,View):
    def get(self, request):
        logout(request)
        messages.info(request, "You have successfully logged out.")
        return redirect("users:login")


class CustomPasswordResetView(LoginRequiredMixin,PasswordResetView):
    success_url = reverse_lazy('users:password_reset_done')


class CustomPasswordResetConfirmView(LoginRequiredMixin, PasswordResetConfirmView):
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        messages.success(self.request, "Parolingiz muvaffaqiyatli o'zgartirildi")
        return super().form_valid(form)

class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        messages.success(self.request, "Parolingiz muvaffaqiyatli alamashtirildi")
        return super().form_valid(form)
