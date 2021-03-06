from django.contrib.auth import logout
from django.contrib import messages
from django.http import Http404
from django.urls import reverse
from django.utils.translation import gettext as _

from . import utils


def user_management_middleware(get_response):
    """User Management Middleware.

    - Logs out user having an account pending deletion. All other sessions of
    the user should rather be cleared when the user requests the account
    deletion, but the way to do that is not obvious.
    - Set the session language to the preferred user language
    - Prevent non-staff users to see the admin interface.
    """

    def middleware(request):
        if request.path.startswith(reverse('admin:index')):
            if not request.user.is_staff:
                raise Http404()

        if request.user.is_authenticated:

            # Set session language
            utils.set_session_language_if_necessary(request, request.user)

            # Logout user pending deletion
            if request.user.um_profile.deletion_pending:
                messages.info(
                    request,
                    _('This account is about to be permanently deleted, sign '
                      'in again to reactivate it.')
                )
                logout(request)

        return get_response(request)

    return middleware
