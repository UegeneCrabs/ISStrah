from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views.generic import FormView
from django.urls import reverse_lazy


def register_client(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'users'
            user.save()
            login(request, user)
            return redirect('personal_account_client')
    else:
        form = CustomUserCreationForm()
    return render(request, 'main/registration.html', {'form': form})


class LoginUser(SuccessMessageMixin, FormView):
    form_class = AuthenticationForm
    template_name = 'main/login.html'
    success_message = 'Успешная авторизация'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        return context

    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка аутентификации')
        return super().form_invalid(form)

    def get_success_url(self):
        user = self.request.user
        if user.user_type == 'agent':
            return reverse_lazy('users:personal_account_agent')
        elif user.user_type == 'appraiser':
            return reverse_lazy('users:personal_account_appraiser')
        else:
            return reverse_lazy('users:personal_account_client')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


def main_layout(request):
    return render(request, 'main/main_layout.html', {"title": "main_layout"})
