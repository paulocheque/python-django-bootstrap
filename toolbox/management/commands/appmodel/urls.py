from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

from tastypie.api import Api

from .api import *

admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(UserResource())

urlpatterns += patterns('',
    (r'^', include(v1_api.urls)),
)

urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
)

urlpatterns = += patterns('',
    url(r'^$', 'appmodel_site.views.showcase', name='showcase'),
    url(r'demo$', TemplateView.as_view(template_name="static/info/demo.html")),
)
