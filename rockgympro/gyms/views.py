from django.shortcuts import render, get_object_or_404
from gyms.models import Gym, Route, Send, Favorite
from django.utils.timezone import now
from django.http import Http404
from django.views.generic import ListView, DetailView, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from gyms.forms import *
from django.core import urlresolvers
from django import shortcuts
from django.utils.http import urlquote
import json
from django.http import HttpResponse
from django.db import IntegrityError

#Auth imports
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, QueryDict
from django.template.response import TemplateResponse
from django.utils.http import is_safe_url, urlsafe_base64_decode
from django.utils.translation import ugettext as _
from django.utils.six.moves.urllib.parse import urlparse, urlunparse
from django.shortcuts import resolve_url
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

# Avoid shadowing the login() and logout() views below.
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site

class GymFinderMixin(SingleObjectMixin):

    model = Gym
    slug_url_kwarg = "gym"
    context_object_name="gym"
    perms = None

    def dispatch(self, request, *args, **kwargs):
        self.object = get_object_or_404(Gym, slug=self.kwargs['gym'])
        self.gym = self.object
        if self.perms is not None:
            if request.user.is_anonymous():
                return shortcuts.redirect("%s?next=%s" % (urlresolvers.reverse("gym_login", kwargs={'gym':self.gym.slug}), urlquote(request.path)))
            elif not (request.user.gym == self.gym and request.user.level >= self.perms):
                raise Http404()
        return super(GymFinderMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GymFinderMixin, self).get_context_data(**kwargs)
        context['gym'] = self.gym
        return context

    def get_object(self):
        return get_object_or_404(Gym, slug=self.kwargs['gym'])

class JSONResponseMixin(object):
    """
    A mixin that can be used to render a JSON response.
    """
    def render_to_json_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        return HttpResponse(
            self.convert_context_to_json(context),
            content_type='application/json',
            **response_kwargs
        )

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return json.dumps(context)

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)

class GymPage(GymFinderMixin, DetailView):

    template_name="gym_page.html"

class RoutesPage(GymFinderMixin, ListView):

    template_name = "gym_routes.html"

    def get_queryset(self):
        return self.object.routes.filter(status="complete")

class AdminRoutesPage(GymFinderMixin, ListView):

    perms = 500

    template_name = "gym_routes_admin.html"

    def get_queryset(self):
        return self.object.routes.all()

class RouteFinderMixin(GymFinderMixin):

    def get_route(self):
        return get_object_or_404(self.gym.routes, slug=self.kwargs['route'])

    def get_context_data(self, **kwargs):
        context = super(GymFinderMixin, self).get_context_data(**kwargs)
        context['route'] = self.get_route()
        context['sent'] = bool(context['route'].sends.filter(id=self.request.user.id).count())
        context['favorited'] = bool(context['route'].favorites.filter(id=self.request.user.id).count())
        return context

class RoutePage(RouteFinderMixin, DetailView):

    template_name = "gym_route.html"

class RouteAJAX(JSONResponseMixin, RouteFinderMixin, View):
    
    #TODO: Remove!
    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        route = self.get_route()
        user = request.user
        if user.is_anonymous():
            raise Http404
        elif user.gym != self.gym:
            raise Http404
        elif kwargs['action'] == "send":
            try:
                Send(route=route, user=user).save()
            except IntegrityError:
                return self.render_to_response(dict(success=True, new=False))
            return self.render_to_response(dict(success=True, new=True))
        elif kwargs['action'] == "unsend":
            Send.objects.filter(user=user, route=route).delete()
            return self.render_to_response(dict(success=True))
        elif kwargs['action'] == "favorite":
            try:
                Favorite(route=route, user=user).save()
                return self.render_to_response(dict(success=True))
            except IntegrityError:
                return self.render_to_response(dict(success=True, new=False))
            return self.render_to_response(dict(success=True, new=True))
        elif kwargs['action'] == "unfavorite":
            Favorite.objects.filter(user=user, route=route).delete()
            return self.render_to_response(dict(success=True))

class GymDashboard(GymPage):

    perms = 500

    template_name="gym_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(GymDashboard, self).get_context_data(**kwargs)
        context['routes'] = self.gym.routes.order_by("-created")[:5]
        return context

class GymStats(JSONResponseMixin, GymFinderMixin, DetailView):

    perms = 500

    def split(self, d):
        return [dict(label=k, data=v) for k,v in d.items()]

    def get_context_data(self, **kwargs):
        context = {}
        d = {}
        for k,v in self.gym.grades(type="top_rope").items():
            d[round(k)] = d.get(round(k), 0)+v
        context['top_rope_grades'] = self.split({Route(grade=k).get_grade_display():v for k,v in d.items()})
        d = {}
        for k,v in self.gym.grades(type="bouldering").items():
            d[round(k)] = d.get(round(k), 0)+v
        context['bouldering_grades'] = self.split({Route(grade=k).get_grade_display():v for k,v in d.items()})
        context['types'] = self.split(self.gym.types())
        context['setters'] = self.split(self.gym.setters())
        context['locations'] = self.split(self.gym.locations())
        return context

class AdminRouteAdd(GymFinderMixin, CreateView):

    perms = 1000

    form_class = RouteForm
    template_name="gyms/route_form.html"

    def get_form_kwargs(self):
        kwargs = super(AdminRouteAdd, self).get_form_kwargs()
        kwargs['gym'] = self.gym
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return urlresolvers.reverse("gym_routes", kwargs=dict(gym=self.kwargs['gym']))

class AdminRouteEdit(RouteFinderMixin, UpdateView):

    perms = 1000
    template_name_suffix = '_update_form'

    form_class = RouteForm

    def get_form_kwargs(self):
        kwargs = super(AdminRouteEdit, self).get_form_kwargs()
        kwargs['gym'] = self.gym
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return urlresolvers.reverse("gym_routes_admin", kwargs=dict(gym=self.kwargs['gym']))

class GymSettings(UpdateView):

    perms = 10000
    
    template_name="gym_settings.html"
    form_class = GymSettingsForm
    model = Gym
    slug_url_kwarg = "gym"

    def get_success_url(self):
        return urlresolvers.reverse("gym_dashboard", kwargs=dict(gym=self.kwargs['gym']))

class AdminStaffPage(GymFinderMixin, ListView):

    perms = 10000

    template_name = "gym_staff_admin.html"

    def get_queryset(self):
        return self.object.staff.order_by("-level")

class EmployeeFinderMixin(GymFinderMixin):

    no_owner = False

    def get_employee(self):
        user = get_object_or_404(self.gym.staff, username=self.kwargs['user'])
        if self.no_owner and user.level == 10000:
            raise Http404
        return user

    def get_context_data(self, **kwargs):
        context = super(GymFinderMixin, self).get_context_data(**kwargs)
        context['employee'] = self.get_employee()
        context['gym'] = context['employee'].gym
        return context

    def get_object(self):
        return self.get_employee()

class AdminEmployeeAdd(GymFinderMixin, CreateView):

    perms = 10000

    form_class = EmployeeCreationForm
    template_name="gyms/employee_form.html"

    def get_form_kwargs(self):
        kwargs = super(AdminEmployeeAdd, self).get_form_kwargs()
        kwargs['gym'] = self.gym
        return kwargs

    def get_success_url(self):
        return urlresolvers.reverse("gym_staff_admin", kwargs=dict(gym=self.kwargs['gym']))

class AdminEmployeeUpdate(EmployeeFinderMixin, UpdateView):

    perms = 10000

    form_class = EmployeeUpdateForm
    template_name="gyms/employee_update_form.html"

    def get_success_url(self):
        return urlresolvers.reverse("gym_staff_admin", kwargs=dict(gym=self.kwargs['gym']))

class AdminEmployeeDelete(EmployeeFinderMixin, DeleteView):

    no_owner = True

    perms = 10000

    template_name = "gyms/employee_confirm_delete.html"

    def get_success_url(self):
        return urlresolvers.reverse("gym_staff_admin", kwargs=dict(gym=self.kwargs['gym']))

def redirect(request, to, *args, **kwargs):
    return shortcuts.redirect(to, *args, **kwargs)

@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request, gym, template_name='registration/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=GymAuthForm,
          current_app=None, extra_context=None):
    """
    Displays the login form and handles the login action.
    """

    gym = get_object_or_404(Gym, slug=gym)
    redirect_to = request.POST.get(redirect_field_name,
                                   request.GET.get(redirect_field_name, ''))

    if request.method == "POST":
        form = authentication_form(request, data=request.POST, gym=gym)
        if form.is_valid():

            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            # Okay, security check complete. Log the user in.
            auth_login(request, form.get_user())

            return HttpResponseRedirect(redirect_to)
    else:
        form = authentication_form(request)

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
        'gym': gym,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)
