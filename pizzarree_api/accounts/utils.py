import re
from urllib.parse import urljoin

import six
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.profile.email_verified)
        )


account_activation_token = AccountActivationTokenGenerator()


class APIPasswordResetTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.last_login) + six.text_type(user.password)
        )


password_reset_token = APIPasswordResetTokenGenerator()


def get_referer_base_url(referer):
    if referer is not None:
        try:
            base_url = re.match(r"(?:[^\/]*\/){3}", referer)
            return base_url.group()
        except Exception:
            pass
    return referer


def send_verification_email(request, user, token_generator=account_activation_token,
                            template_name='post_office/accounts/api/activation_email.html'):

    current_site = get_current_site(request)
    subject = _('{} Team').format(current_site)
    request_referer = request.headers.get('referer')
    base_referer = get_referer_base_url(request_referer)

    message = render_to_string(template_name, {
        'protocol': 'https' if request.is_secure() else 'http',
        'user': user,
        'domain': request.headers.get("HOST", current_site.domain),
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': token_generator.make_token(user),
        'referer': base_referer
        # 'referer': request_referer
    })

    user.email_user(subject, message, from_email=settings.DEFAULT_FROM_EMAIL, html_message=message)


class BuildRedirectionUrl(object):
    message = ""
    enforce_json_response = False
    enforce_redirect = False
    url_extension = settings.API_WEBHOOK_REDIRECT_EXTENSION

    @property
    def REDIRECT_URL(self):
        referer, exists = self.get_referer()
        if exists:
            self.enforce_redirect = True
            return urljoin(referer, self.url_extension)
        else:
            if self.enforce_redirect:
                return urljoin(settings.FRONTEND_URL, self.url_extension)
            self.enforce_json_response = True

    def get_referer(self):
        referer = False
        exists = True
        if self.request.query_params.get('referer') is not None:
            referer = self.request.query_params.get('referer').removesuffix('%20').strip()
        elif self.request.headers.get('referer') is not None:
            referer = self.request.headers.get('referer')
        else:
            exists = False
        return get_referer_base_url(referer), exists

    def predict_http_response(self, **kwargs):
        message = kwargs.get('message') if kwargs.get('message') else self.message
        if self.enforce_json_response or not self.REDIRECT_URL or not self.enforce_redirect:
            return JsonResponse({'message': message}, content_type='application/json')
        if self.REDIRECT_URL or self.enforce_redirect:
            return HttpResponseRedirect(self.REDIRECT_URL + message, content_type='application/json')


