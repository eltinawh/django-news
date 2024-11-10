from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout

from .forms import CustomUserCreationForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = "registration/signup.html"
    
    
@login_required
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse("home"))
    