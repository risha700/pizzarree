import os

from django.views.generic import TemplateView
from django.conf import settings
from django.utils.functional import classproperty


class JsApp(TemplateView):
    """
    basically this is misplaced
    Receives filtered 404 catch all non ending in slash and
    serve it as JS
    Note: It doesn't work with PWA as for the caching features disables
    fallback to django URLS
    """
    # content_type = 'application/html'
    template_name = 'index.html'  # to be copied after docker-build as a volume

    @classproperty
    def settings(cls):
        """Just changing STATIC_ROOT to js folder to keep it separate"""
        DIST_ROOT = os.path.join(settings.BASE_DIR, 'dist')
        changed_settings = settings
        changed_settings.STATIC_ROOT = DIST_ROOT
        return changed_settings

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
