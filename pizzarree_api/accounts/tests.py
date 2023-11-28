import re

from django.core import mail
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from accounts.models import Profile

User = get_user_model()


class UserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient(enforce_csrf_checks=False)
        User.objects.create(username="test", email="test@local.test", phone="+13157951115")
        user = User.objects.get(username='test')
        user.set_password('test')
        user.profile.email_verified = True
        user.save()
        self.test_user = user

    def test_profile_created_on_signal_received(self):
        user = User.objects.get(username="test")
        self.assertIsInstance(user.profile, Profile)

    def test_api_register(self):
        new_user = {'username': 'new_test', 'password': 'new_test', 'password2': 'new_test',
                    'email': 'test2@public.test', 'phone': '+33333333333'}
        response = self.client.post(reverse('api-auth:register'), new_user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

        self.assertIsNotNone(mail.outbox[0].message())
        # request verification link
        activation_response = self.client.post(reverse('api-auth:login'),
                                    {'username': 'new_test', 'password': 'new_test'})
        self.assertTrue(activation_response.exception)
        self.assertIn('Please verify your email', str(activation_response.json()))

    def test_api_login(self):
        not_allowed_response = self.client.get(reverse('api-auth:login'))
        self.assertEqual(not_allowed_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.post(reverse('api-auth:login'), {'username': 'test', 'password': 'test'})
        # self.assertIsNotNone(mail.outbox[0].message()) # tracking activity
        self.assertContains(response, 'token')

    def test_api_user_can_change_password(self):
        user_token = self.client.post(reverse('api-auth:login'),
                                      {'username': 'test', 'password': 'test'}).json().get('token')
        response = self.client.post(reverse('api-auth:password_change'),{
                                    'old_password': 'test',
                                    'password': 'secret@123',
                                    'password2': 'secret@123'},
                                    **{'HTTP_AUTHORIZATION': 'Token %s' % user_token})
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_api_user_can_crud_profile(self):
        user_token = self.client.post(reverse('api-auth:login'),
                                      {'username': 'test', 'password': 'test'}).json().get('token')
        response_get = self.client.get(reverse('api-auth:profile'), **{'HTTP_AUTHORIZATION': 'Token %s' % user_token})
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)

        response_post = self.client.post(reverse('api-auth:profile'),
                                         data={'username': 'test2',
                                               'phone': '+16469061933',
                                               'email': 'test@public.test',
                                               'profile.clear_photo': True
                                               },
                                         **{'HTTP_AUTHORIZATION': 'Token %s' % user_token})
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.filter(email='test@public.test')[0].username, 'test2')

    def test_api_user_password_reset(self):
        # request password rest
        referer_header = "https://custom.net"

        response = self.client.post(reverse('api-auth:password_reset'), {'email': 'test@local.test'},
                                    **{"HTTP_REFERER": referer_header})
        # print(response.__dict__)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        url = re.findall('https?://[/-/_A-Za-z0-9/{4}].+', mail.outbox[0].body)
        # visit the link to confirm
        reset_response = self.client.get(url[1][:-2], follow=True)
        self.assertIn(referer_header, reset_response.redirect_chain[0][0])
        self.assertEqual(reset_response.redirect_chain[0][1], status.HTTP_302_FOUND)
        # assume redirected to the frontend form and submitted
        token = re.findall('(?<=auth_token=).*$', reset_response.redirect_chain[0][0])
        password_reset_response = self.client.patch(reverse('api-auth:password_change'),
                                                    {'email': 'test@public.test',
                                                     'password': 'secret@123',
                                                     'password2': 'secret@123'},
                                                    **{'HTTP_AUTHORIZATION': 'Token %s' % token[0]})
        # print(password_reset_response.content)
        self.assertEqual(password_reset_response.status_code, status.HTTP_202_ACCEPTED)

    def test_activate_account_redirects(self):
        user = User.objects.get(username='test')
        user.profile.email_verified = False
        user.save()
        referer_header = "https://custom.net"
        response_redirect = self.client.get(reverse('api-auth:verification_request', kwargs={'pk': user.pk}),
                                            **{"HTTP_REFERER":  referer_header})
        self.assertEqual(response_redirect.status_code, status.HTTP_302_FOUND)
        self.assertIn(response_redirect.request.get('HTTP_REFERER'), response_redirect.url)
        url = re.findall('https?://[/-/_A-Za-z0-9/{4}].+', mail.outbox[0].body)
        self.assertIn('referer={}'.format(referer_header), url[1][:-2].split('"')[0])
        activate_response_ref = self.client.get(url[1][:-2].split('"')[0], follow=True)
        # test redirection to frontendurl
        self.assertIn(activate_response_ref.wsgi_request.environ.get('SERVER_NAME'), referer_header)
        self.assertIn(referer_header, activate_response_ref.redirect_chain[0][0])
        self.assertEqual(activate_response_ref.redirect_chain[0][1], status.HTTP_302_FOUND)
        user.refresh_from_db()
        self.assertTrue(user.profile.email_verified)
        user.profile.email_verified = False

    def test_api_login_steps(self):
        response = self.client.post(reverse('api-auth:login_step'), {'username': 'test'})
        self.assertEqual(response.status_code, status.HTTP_207_MULTI_STATUS)
        self.assertEqual(response.json(), {'checks': 'true', 'username': 'test'})

        failed_response = self.client.post(reverse('api-auth:login_step'), {'username': 'tet'})
        self.assertEqual(failed_response.status_code, status.HTTP_400_BAD_REQUEST)
        failed_response = self.client.post(reverse('api-auth:login_step'), {'username': 'r'})
        self.assertEqual(failed_response.status_code, status.HTTP_403_FORBIDDEN)
