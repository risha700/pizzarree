from rest_framework.permissions import BasePermission
from rest_framework.request import Request


class IsAuthorized(BasePermission):
    def has_permission(self, *args):
        # is_active and verified and premium
        if isinstance(args[0], Request):
            request = args[0]
        else:
            request = args[0].request
        return request.user and request.user.is_authenticated and \
            (request.user.is_staff or request.user.is_superuser or request.user.get_all_permissions())

    def has_object_permission(self, view, obj, **kwargs):
        return view.request.user == view.request.user.is_staff or view.request.user.is_superuser


class IsOrderOwner(BasePermission):
    def has_permission(self, view, **kwargs):
        qs = view.queryset
        order_email = view.request.query_params.get('order_email', False)
        request_user_email = getattr(view.request.user, 'email', False)
        if view.request.user.is_anonymous and not order_email:
            return False
        if order_email:
            view.queryset = qs.filter(email=order_email)
        else:
            view.queryset = qs.filter(email=request_user_email)
        return True

    def has_object_permission(self, view, obj, **kwargs):
        order_email = view.request.query_params.get('order_email', None)
        request_user_email = getattr(view.request.user, 'email', False)
        return request_user_email == obj.email or order_email == obj.email
