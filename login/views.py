from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import JoinForm


class Join(FormView):
    """Show form and create user if valid."""

    form_class = JoinForm
    success_url = '/'
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
