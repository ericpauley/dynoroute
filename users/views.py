from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from django.contrib import messages
from django.contrib import auth
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse
from users.models import User
from django.utils.decorators import method_decorator

def landing(request):
    if request.user.is_authenticated():
        if request.user.gym is not None:
            return redirect("gym_dashboard", gym=request.user.gym.slug)
        else:
            return redirect("dashboard")
    else:
        return redirect("home")

def home(request):
    return render(request, "launch.html")

@login_required
def dashboard(request):
    if request.user.gym is not None:
        return redirect("gym_dashboard", gym=request.user.gym.slug)
    context = {
        "favorites":request.user.favorite_set.order_by("-created")[:10],
        "sends":request.user.send_set.order_by("-created")[:10],
        "logout_next":reverse("home"),
    }
    return render(request, "user_dashboard.html", context)

@login_required
def favorites(request):
    if request.user.gym is not None:
        return redirect("gym_dashboard", gym=request.user.gym.slug)
    context = {
        "routes":request.user.favorite_set.order_by("-created")[:10],
        "title":"Favorite Routes",
        "logout_next":reverse("home"),
    }
    return render(request, "user_routes.html", context)

@login_required
def sends(request):
    if request.user.gym is not None:
        return redirect("gym_dashboard", gym=request.user.gym.slug)
    context = {
        "routes":request.user.send_set.order_by("-created")[:10],
        "title":"Sent Routes",
        "logout_next":reverse("home"),
    }
    return render(request, "user_routes.html", context)

class ProfileEditView(UpdateView):

    model = User
    fields = ["name", "nickname"]
    template_name = "users/profile_form.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfileEditView, self).dispatch(*args, **kwargs)

    def get_object(self):
        return self.request.user
