from django.shortcuts import render, get_object_or_404
from gyms.models import Gym, Route
from django.utils.timezone import now
from django.http import Http404
from django.views.generic import ListView, DetailView
from django.views.generic.detail import SingleObjectMixin

class GymFinderMixin(SingleObjectMixin):

    model = Gym
    slug_url_kwarg = "gym"

    def get(self, request, *args, **kwargs):
        self.object = get_object_or_404(Gym, slug=self.kwargs['gym'])
        return super(GymFinderMixin, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GymFinderMixin, self).get_context_data(**kwargs)
        context['gym'] = self.object
        return context

class GymPage(GymFinderMixin, DetailView):

    template_name="gym_page.html"

class GymAdmin(GymPage):

    def get_object(self, *args, **kwargs):
        obj = super(GymAdmin, self).get_object(*args, **kwargs)
        if self.request.user.is_anonymous() or (self.request.user.gym != obj and obj.owner != self.request.user):
            raise Http404 # maybe you'll need to write a middleware to catch 403's same way
        return obj

class RoutesPage(GymFinderMixin, ListView):

    paginate_by = 2
    template_name = "gym_routes.html"

    def get_queryset(self):
        return self.object.routes.all()

    def get_context_data(self, **kwargs):
        context = super(RoutesPage, self).get_context_data(**kwargs)
        context['named_routes'] = self.object.routes.exclude(name="").count()
        return context

class RoutePage(GymPage):

    template_name = "gym_route.html"

    def get_context_data(self, **kwargs):
        context = super(GymFinderMixin, self).get_context_data(**kwargs)
        context['route'] = get_object_or_404(self.object.routes, slug=self.kwargs['route'])
        return context

class GymDashboard(GymAdmin):

    template_name="gym_dashboard.html"

class GymAdminRouteAdd(GymAdmin):

	template_name="gym_route_add.html"