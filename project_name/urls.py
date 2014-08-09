from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.site.site_header = '{{ project_name }} Admin'
admin.site.site_title = '{{ project_name }} Admin'
admin.site.index_title = ''

urlpatterns = patterns('',
    (r'^accounts/login/$', 'django_cas.views.login'),
    (r'^accounts/logout/$', 'django_cas.views.logout'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts2/', include('allauth.urls')),

    url(r'^api/', include('{{ project_name }}_api.urls')),
    url(r'^', include('{{ project_name }}_site.urls')),
)

# urlpatterns += patterns('',
#     (r'^static/(?P.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
# )