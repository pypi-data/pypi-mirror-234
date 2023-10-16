from django.views.generic.base import View
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class NightModeRedirectView(View):
    SESSION_VAR = "NIGHT_MODE"

    def get(self, request, *args, **kwargs):
        request.session[self.SESSION_VAR] = not self.night_mode_state(request)
        if not request.user.is_anonymous:
            try:
                request.user.profile.night_mode = request.session[self.SESSION_VAR]
                request.user.profile.save()
            except Exception as e:
                logger.exception(e)

        return HttpResponseRedirect(request.GET.get("next", "/"))

    @classmethod
    def night_mode_state(cls, request):
        try:
            return request.session.get(cls.SESSION_VAR, False)
        except AttributeError:
            # Session is middleware
            # Sometimes request wont have a session attribute
            return False


class ThemeRedirectView(View):

    def post(self, request, *args, **kwargs):
        theme = request.POST.get('theme', settings.DEFAULT_THEME)
        if not request.user.is_anonymous:
            try:
                request.user.profile.theme = theme
                request.user.profile.save()
            except Exception as e:
                logger.exception(e)

        return HttpResponseRedirect(request.GET.get("next", "/"))


def Generic500Redirect(request):  # TODO Real view

    title = _(
        "Internal Server Error"
    )
    message = _(
        "Auth encountered an error processing your request, please try again. "
        "If the error persists, please contact the administrators."
    )

    return render(request, "allianceauth/error.html", context={"error_title": title, "error_message": message})


def Generic404Redirect(request, exception):  # TODO Real view
    title = _(
        "Page Not Found"
    )
    message = _(
        "Page does not exist. If you believe this is in error please contact the administrators. "
    )

    return render(request, "allianceauth/error.html", context={"error_title": title, "error_message": message})


def Generic403Redirect(request, exception):  # TODO Real view
    title = _(
        "Permission Denied"
    )
    message = _(
        "You do not have permission to access the requested page. "
        "If you believe this is in error please contact the administrators."
    )

    return render(request, "allianceauth/error.html", context={"error_title": title, "error_message": message})


def Generic400Redirect(request, exception):  # TODO Real view
    title = _(
        "Bad Request"
    )
    message = _(
        "Auth encountered an error processing your request, please try again. "
        "If the error persists, please contact the administrators."
    )

    return render(request, "allianceauth/error.html", context={"error_title": title, "error_message": message})
