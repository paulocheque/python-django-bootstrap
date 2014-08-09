import requests
import dicttoxml
import simplejson as json

from django.conf.urls import url
from django.http import HttpResponse, StreamingHttpResponse

from tastypie import fields
from tastypie.authentication import MultiAuthentication, ApiKeyAuthentication, SessionAuthentication
from tastypie.authorization import DjangoAuthorization, Authorization
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpUnauthorized, HttpForbidden, HttpNotFound
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash
from tastycrust.authentication import AnonymousAuthentication
from tastycrust.resources import ActionResourceMixin, action
from tastycrust.utils import owned


from .models import *

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        include_resource_uri = False
        fields = ['username', 'first_name', 'last_name',]
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']


class UserAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        return object_list.filter(user=bundle.request.user)

    def read_detail(self, object_list, bundle):
        return bundle.request.user.is_superuser or (bundle.obj.user == bundle.request.user)

    def create_list(self, object_list, bundle):
        return object_list

    def create_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

    def update_list(self, object_list, bundle):
        allowed = []
        for obj in object_list:
            if obj.user == bundle.request.user:
                allowed.append(obj)
        return allowed

    def update_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

    def delete_list(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

    def delete_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user


# class DashboardResource(ModelResource):
#     user = fields.ForeignKey(UserResource, 'user', full=True)

#     widgets = fields.ToManyField('dashboard_api.api.WidgetResource', 'widget_set', related_name='dashboard', full=True)

#     class Meta:
#         queryset = Dashboard.objects.all()
#         resource_name = 'dashboard'
#         include_resource_uri = False
#         authentication = MultiAuthentication(SessionAuthentication(), ApiKeyAuthentication())
#         authorization = UserAuthorization()

#     def prepend_urls(self):
#         return [
#             url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/children%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_widgets'), name="api_get_widgets"),
#         ]


# class WidgetResource(ActionResourceMixin, ModelResource):
#     # dashboard = fields.ToOneField(DashboardResource, 'dashboard')
#     refresh_url = fields.CharField(attribute='refresh_url', readonly=True, null=True)

#     class Meta:
#         queryset = Widget.objects.all()
#         resource_name = 'widget'
#         exclude = ('dashboard',)
#         include_resource_uri = True
#         authentication = MultiAuthentication(SessionAuthentication(), ApiKeyAuthentication())
#         # authorization = UserAuthorization()

#     def dehydrate(self, bundle):
#         bundle.data['refresh_url'] = bundle.data['resource_uri'] + '/refresh'
#         return bundle
