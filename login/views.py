from django.shortcuts import render, redirect
from django.views.generic import FormView, UpdateView
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .forms import JoinForm
from .models import User


class Join(FormView):
    """Show form and create user if valid."""

    form_class = JoinForm
    success_url = reverse_lazy('login:mypage')
    template_name = 'registration/join.html'

    def form_valid(self, form):
        """ if form is valid """

        form.save()
        email = form.cleaned_data.get('email')
        _password = form.cleaned_data.get('password1')
        user = authenticate(email=email, password=_password)
        if user:
            login(self.request, user)
        return super().form_valid(form)


@login_required
def mypage(request):
    """ Account profile """
    if 'save' in request.session.keys():
        (product, substitute) = request.session['save']
        return redirect('product:save')

    return render(request, "registration/mypage.html")


class UpdateProfile(LoginRequiredMixin, UpdateView):
    """ Change the first and last name. """
    model = User
    fields = ["first_name", "last_name"]
    template_name = 'registration/update_profile.html'
    success_url = reverse_lazy('login:mypage')

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.request.user.pk)
