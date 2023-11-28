from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db.models import Q
from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.exceptions import ValidationError, NotAuthenticated
from rest_framework.reverse import reverse
from rest_framework.validators import UniqueValidator
from django.utils.translation import gettext_lazy as _

from accounts.models import Profile

User = get_user_model()


class LoginFirstStep(serializers.Serializer):
    def validate(self, attrs):
        data = str(self.instance.data.get('username'))
        if len(data) < 2 or len(data) > 64:
            raise NotAuthenticated(_('Unable to find the provided credentials.'), code="unauthorized")
        user = User.objects.filter(Q(username=data.lower()) | Q(phone=data.lower()) | Q(email=data.lower()))
        if not user.exists():
            raise ValidationError(_('Unable to find the provided credentials.'), code="unauthorized")
        return data


class LoginSerializer(AuthTokenSerializer):
    def validate(self, attrs):
        data = super(LoginSerializer, self).validate(attrs)
        user = data.get('user')
        if not user.profile.email_verified:
            verification_url = self.context.get('request').build_absolute_uri(reverse('api-auth:verification_request',
                                                                                      kwargs={'pk': user.pk}))
            link_text = '<a href={}>{}</a>'.format(verification_url, _("Request a verification Link here."))
            raise ValidationError(_('Please verify your email - {} ').format(link_text, code='unverified'))

        if not user.is_active and user.profile.email_verified:
            raise ValidationError(_("Your account is locked out - please contact support."), code="suspended")
        return data


class RegisterUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True,)
    username = serializers.CharField(validators=[UniqueValidator(queryset=User.objects.all(),
                                                                 lookup='iexact', message=_('Username already exists.'))])
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all(), lookup='iexact',
                                                               message=_('Email already exists.'))])

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'password2', 'email', 'phone',)
        write_only_fields = ('password', )
        read_only_fields = ('id',)

    def validate(self, attrs):
        data = super(RegisterUserSerializer, self).validate(attrs)
        password = data.get('password')
        password_confirm = data.get('password2')
        user = self.instance
        validate_password(password, user)

        if password != password_confirm:
            raise ValidationError({'password': _('The two password fields didn’t match.')})
        return data

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            phone=validated_data['phone'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

class ProfileSerializer(serializers.ModelSerializer):
    clear_photo = serializers.BooleanField(allow_null=True, write_only=True)

    class Meta:
        model = Profile
        fields = ('date_of_birth', 'email_verified', 'phone_verified', 'photo', 'clear_photo', )

class ProfileUserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone',  'first_name', 'last_name', 'profile', )

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        profile = instance.profile
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()

        photo_cleanup = profile_data.get('photo', False) or profile_data.get('clear_photo', False)
        if photo_cleanup:
            profile.photo.delete()
        profile.photo = profile_data.get('photo', profile.photo)
        # profile.photo.name = '{}-{}'.format(instance.username, profile.photo.name)
        profile.date_of_birth = profile_data.get('date_of_birth', profile.date_of_birth)
        profile.save()
        return instance



class UserPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'password', 'password2',)
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def validate(self, attrs):
        data = super(UserPasswordSerializer, self).validate(attrs)
        user = self.instance
        new_password = data.get('password')
        new_password2 = data.get('password2')

        validate_password(new_password, user)

        if new_password != new_password2:
            raise ValidationError({'password': _('The two password fields didn’t match.')})
        return data

    def update(self, instance, validated_data):
        password = validated_data.get('password')
        instance.set_password(password)
        instance.save()
        return instance


class UserPasswordChangeSerializer(UserPasswordSerializer):
    old_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'password', 'password2', 'old_password',)
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def validate(self, attrs):
        data = super(UserPasswordChangeSerializer, self).validate(attrs)
        user = self.instance
        password = data.get('old_password')
        if not user.check_password(password):
            raise ValidationError({'old_password': _("Your old password was entered incorrectly."
                                                     " Please enter it again.")})
        new_password = data.get('password')
        new_password2 = data.get('password2')
        if new_password != new_password2:
            raise ValidationError({'password': _('The two password fields did not match.')})
        return data

    def update(self, instance, validated_data):
        password = validated_data.get('password')
        instance.set_password(password)
        instance.save()
        return instance

