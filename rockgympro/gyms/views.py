from django.shortcuts import render, get_object_or_404
from gyms.models import Gym, Route
from django.utils.timezone import now
from django.http import Http404
from django.views.generic import ListView, DetailView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, UpdateView
from gyms.forms import RouteForm, GymSettingsForm
from django.core import urlresolvers
from django import shortcuts
from django.utils.http import urlquote

class GymFinderMixin(SingleObjectMixin):

    model = Gym
    slug_url_kwarg = "gym"
    context_object_name="gym"
    perms = 0

    def dispatch(self, request, *args, **kwargs):
        self.object = get_object_or_404(Gym, slug=self.kwargs['gym'])
        self.gym = self.object
        if self.perms > 0:
            if request.user.is_anonymous():
                return shortcuts.redirect("%s?next=%s" % (urlresolvers.reverse("login"), urlquote(request.path)))
            elif not (self.gym.owner == request.user or (request.user.gym == self.gym and request.user.level >= self.perms)):
                raise Http404()
        return super(GymFinderMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GymFinderMixin, self).get_context_data(**kwargs)
        context['gym'] = self.gym
        return context

    def get_object(self):
        return get_object_or_404(Gym, slug=self.kwargs['gym'])

class GymPage(GymFinderMixin, DetailView):

    template_name="gym_page.html"

class RoutesPage(GymFinderMixin, ListView):

    template_name = "gym_routes.html"

    def get_queryset(self):
        return self.object.routes.all()

class RoutePage(GymPage):

    template_name = "gym_route.html"

    def get_context_data(self, **kwargs):
        context = super(GymFinderMixin, self).get_context_data(**kwargs)
        context['route'] = get_object_or_404(self.object.routes, slug=self.kwargs['route'])
        return context

class GymDashboard(GymPage):

    perms = 500

    template_name="gym_dashboard.html"

class GymAdminRouteAdd(GymFinderMixin, CreateView):

    perms = 1000

    form_class = RouteForm

    def get_form_kwargs(self):
        kwargs = super(GymAdminRouteAdd, self).get_form_kwargs()
        kwargs['gym'] = self.gym
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return urlresolvers.reverse("gym_routes", kwargs=dict(gym=self.kwargs['gym']))

class GymAdminRouteEdit(GymFinderMixin, UpdateView):

    perms = 1000
    template_name_suffix = '_update_form'

    form_class = RouteForm

    def get_form_kwargs(self):
        kwargs = super(GymAdminRouteEdit, self).get_form_kwargs()
        kwargs['gym'] = self.gym
        kwargs['user'] = self.request.user
        return kwargs

    def get_object(self):
        route = get_object_or_404(Route, slug=self.kwargs['route'])
        if route.gym != self.gym:
            raise Http404
        return route

    def get_success_url(self):
        return urlresolvers.reverse("gym_routes", kwargs=dict(gym=self.kwargs['gym']))

class GymSettings(UpdateView):

    perms = 100000
    
    template_name="gym_settings.html"
    form_class = GymSettingsForm
    model = Gym
    slug_url_kwarg = "gym"

    def get_success_url(self):
        return urlresolvers.reverse("gym_dashboard", kwargs=dict(gym=self.kwargs['gym']))

def redirect(request, to, *args, **kwargs):
    return shortcuts.redirect(to, *args, **kwargs)
