from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import NotAcceptable
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _

from .utils import send_verification_email, account_activation_token, BuildRedirectionUrl, password_reset_token

User = get_user_model()
from . import serializers


class AuthRegister(CreateAPIView):
    model = User
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.RegisterUserSerializer
    email_template_name = 'post_office/accounts/api/activation_email.html'

    def dispatch(self, request, *args, **kwargs):
        response = super(AuthRegister, self).dispatch(request, args, kwargs)
        if response.status_code == 201:
            user = User.objects.filter(id=response.data.get('id'))
            if user.exists() and not user.get().profile.email_verified:
                send_verification_email(request, user.get(), token_generator=account_activation_token,
                                        template_name=self.email_template_name)
        return response


class AuthTokenLogin(ObtainAuthToken):
    serializer_class = serializers.LoginSerializer
    throttle_classes = [AnonRateThrottle]

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
        return Response({
            'token': token.key,
            'is_active': user.is_active,
            'user_id': user.pk,
            'username': user.username,
            'avatar': user.profile.photo.url if user.profile.photo and user.profile.photo.url else '',
            'phone_verified': user.profile.phone_verified,
            'email_verified': user.profile.email_verified,
            'preference': user.profile.preference
        })


class AuthLoginStep(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        serializer = serializers.LoginFirstStep(self.request, data={**request.data})
        serializer.is_valid(raise_exception=True)
        return Response({'checks': 'true', 'username': request.data.get('username')},
                        status=status.HTTP_207_MULTI_STATUS)


class PasswordAPIView(APIView, BuildRedirectionUrl):
    permission_classes = [AllowAny]

    def get_user(self, uidb64):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist, Exception):
            user = None
        return user


class AccountActivation(PasswordAPIView):

    def get(self, request, uidb64, token, format=None):
        user = self.get_user(uidb64)

        # print(self.FRONT_END_URL)
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profile.email_verified = True
            user.save()
            self.message = "?level=success&message=" + _('Your account is now active')
            return self.predict_http_response()

        self.message = "?level=error&message=" + _('Link is invalid or has been already used')
        return self.predict_http_response()


class ActivationRequest(APIView, BuildRedirectionUrl):
    permission_classes = [AllowAny]
    email_template_name = 'post_office/accounts/api/activation_email.html'

    def get(self, request, format=None, **kwargs):
        user = get_object_or_404(User, pk=kwargs.get('pk'))
        if not user.profile.email_verified:
            send_verification_email(request, user)
        self.message = "?level=success&message=" + \
                       _('Verification email has been sent to {}, please click the activation link').format(user.email)
        self.url_extension = "done"
        return self.predict_http_response()


class AuthUserProfile(APIView):
    def get(self, request, format=None):
        user = get_object_or_404(User, pk=request.user.id)
        serializer = serializers.ProfileUserSerializer(user)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = serializers.ProfileUserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AuthPasswordChange(APIView):

    def post(self, request, format=None):
        serializer = serializers.UserPasswordChangeSerializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def patch(self, request, format=None):
        serializer = serializers.UserPasswordSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class PasswordResetRequest(APIView):
    permission_classes = []
    email_template_name = 'post_office/accounts/api/password_reset_email.html'

    def post(self, request, format=None):
        # refuse API without referer
        if not (self.request.query_params.get('referer') or self.request.headers.get('referer')):
            raise(NotAcceptable(detail=_("Reset passwords only valid through a web form")))
        user = User.objects.filter(email=request.data.get('email'))
        if user.exists():
            send_verification_email(request, user[0],
                                    token_generator=password_reset_token,
                                    template_name=self.email_template_name)
        return Response({'data': _("Reset password email has been sent to %s, please check your email.") % request.data
                        .get('email')}, status.HTTP_202_ACCEPTED)


class ResetPasswordConfirm(PasswordAPIView):
    enforce_redirect = True

    def get(self, request, uidb64, token, format=None):
        user = self.get_user(uidb64)
        if user is not None and password_reset_token.check_token(user, token):
            auth_token = Token.objects.get_or_create(user=user)[0]
            self.message = '?auth_token={}'.format(auth_token)
            self.url_extension = 'user/password_reset_confirm'
            return self.predict_http_response()

        self.message = '?level=error&message=' + _('Link is invalid or has been already used')
        return self.predict_http_response()
