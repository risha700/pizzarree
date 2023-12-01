import sys
from decimal import Decimal


from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.dispatch import Signal
from django.shortcuts import render
from rest_framework.response import Response
from shop.models import UserVault, PaymentLog
import stripe

payment_received = Signal()


stripe.api_key = settings.STRIPE_API_SECRET


class PaymentGateway:
    def __init__(self, *args, **kwargs):
        self.gateway = stripe
        super(PaymentGateway, self).__init__(*args, **kwargs)

    def process_payment(self, request, order):
        customer_id = None
        if not request.user.is_anonymous:
            """
            we have user
            get vault_id or create a new one
            """
            user_vault, _ = UserVault.objects.get_or_create(user=request.user)
            if not user_vault.vault_id:
                """"""
                new_customer = self.gateway.Customer.create(email=request.user.email)
                user_vault.vault_id = new_customer.id
                user_vault.save()

            customer_id = user_vault.vault_id

        intent = self.gateway.PaymentIntent.create(
            confirm=True,
            return_url='https' if request.is_secure() else 'http' + '://' + get_current_site(request).domain,
            amount=int(order.total_cost*100),
            currency="nzd",
            automatic_payment_methods={"enabled": True, 'allow_redirects': 'always'},
            payment_method=request.data.get('paymentMethodId'),
            use_stripe_sdk=True,
            customer=customer_id,
            # setup_future_usage="off_session",
            statement_descriptor="My Order",
            metadata={
                'order_id': order.id,
                'order_email': order.email
            },
        )
        payment_log = PaymentLog.objects.create(user_id=request.user.id, order=order, amount=intent.amount,
                                                transaction_id=intent.id, info={'type': intent.payment_method})
        payment_received.send_robust(sender=self.__class__, order=order, payment=payment_log, transaction=intent)
        return intent

    def create_intent(self, **kwargs):
        order_id = kwargs.get('order_id')
        request = kwargs.get('request')
        amount = kwargs.get('amount')
        currency = kwargs.get('currency')
        self.gateway.PaymentIntent.create(
            amount=2000,
            currency="nzd",
            automatic_payment_methods={"enabled": True},
            metadata={
                "order_id": "6735",
                'customer_acceptance': {
                    type: "online",
                    'online': {
                        # 'ip_address': req.ip,
                        # 'user_agent': req.get("user-agent"),
                    },
                }
            },
        )

    def create_checkout_session(self):
        self.gateway.checkout.Session.create(
            # success_url="https://example.com/success",
            line_items=[
                {
                    "price": "price_H5ggYwtDq4fbrJ",
                    "quantity": 2,
                },
            ],
            mode="payment",

        )
# class PaymentGatewayMixin:
#     SUCCESS_STATUSES = TRANSACTION_SUCCESS_STATUSES
#
#     def __init__(self, *args, **kwargs):
#         self.gateway = gateway
#         super(PaymentGatewayMixin, self).__init__(*args, **kwargs)
#
#     def generate_client_token(self, kwargs={}):
#         return self.gateway.client_token.generate(kwargs)
#
#     def charge(self, options):
#         return self.gateway.transaction.sale(options)
#
#     def find_transaction(self, identification):
#         return self.gateway.transaction.find(identification)
#
#     def subscribe(self, plan_id, user_id):
#         result = self.gateway.subscription.create({
#             "payment_method_token": "the_token",
#             "plan_id": plan_id,
#             # "merchant_account_id": "gbp_account"
#         })
#         return result
#
#     def unsubscribe(self, plan_id, user_id):
#         raise NotImplemented()
#
#     def refund(self, charge_id, customer_id):
#         raise NotImplemented()
#
#     def find_customer_by_email(self, email):
#         results = self.gateway.customer.search([braintree.CustomerSearch.email == email])
#         if len(results.ids):
#             return results.first
#         return None
#
#     def add_payment_details(self, customer_id, customer_nonce, **kwargs):
#         return self.gateway.payment_method.create({
#             "customer_id": customer_id,
#             "payment_method_nonce": customer_nonce,
#             "options": {
#                 "make_default": kwargs.get('make_default', False),
#                 "verify_card": True,
#                 "fail_on_duplicate_payment_method": True
#             }
#         })
#
#     def process_checkout(self, request, order):
#         customer_id = None
#         token = self.generate_client_token()
#         opts = {
#             'amount': Decimal(order.total_cost),
#             'options': {
#                 "submit_for_settlement": True
#             }
#         }
#         # sign in or continue as guest
#         if not request.user.is_anonymous:
#             """
#             we have user
#             get vault_id or create a new one
#             """
#             user_vault, _ = UserVault.objects.get_or_create(user=request.user)
#             if not user_vault.vault_id:
#                 """"""
#                 new_customer = self.gateway.customer.create({'email': request.user.email})
#                 user_vault.vault_id = new_customer.customer.id
#                 user_vault.save()
#             customer_id = user_vault.vault_id
#
#             opts['customer_id'] = customer_id
#             token = self.generate_client_token({'customer_id': customer_id})
#
#         if request.method == 'POST':
#             """get nonce and pay"""
#             payment_method_nonce = request.data.get('payment_method_nonce')
#             opts['payment_method_nonce'] = payment_method_nonce
#             # opts['store_in_vault_on_success'] =  True
#             # process payment
#             result = self.charge(opts)
#             # result.transaction.credit_card_details.last_4
#             if result.is_success or (result.transaction and result.transaction.status in self.SUCCESS_STATUSES):
#                 user = request.user if not request.user.is_anonymous else None
#                 payment_log = PaymentLog.objects.create(user=user, order=order, amount=result.transaction.amount,
#                                                         transaction_id=result.transaction.id)
#
#                 payment_received.send_robust(sender=self.__class__, order=order, payment=payment_log)
#
#                 return Response({'ok'})
#             else:
#                 errors = [{e.code: e.message} for e in result.errors.deep_errors]
#                 # result.transaction.processor_response_text
#                 return Response({'message': errors if len(errors) else str(result.message)})
#
#         # return render(request, 'sudo_checkout.html', context={'client_token': token, 'customer_id': customer_id})
#         return Response({'client_token': token, 'customer_id': customer_id})
