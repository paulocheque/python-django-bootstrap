from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="static/index.html")),

    url(r'showcase$', '{{ project_name }}_site.views.showcase', name='showcase'),

    url(r'demo$', TemplateView.as_view(template_name="static/info/demo.html")),
    url(r'features$', TemplateView.as_view(template_name="static/info/features.html")),
    url(r'pricing$', TemplateView.as_view(template_name="static/info/pricing.html")),
    url(r'careers$', TemplateView.as_view(template_name="static/info/careers.html")),
    url(r'about$', TemplateView.as_view(template_name="static/info/about.html")),
    url(r'team$', TemplateView.as_view(template_name="static/info/team.html")),
    url(r'legal$', TemplateView.as_view(template_name="static/info/legal.html")),

    url(r'help$', TemplateView.as_view(template_name="static/help/help.html")),
    url(r'help/dev$', TemplateView.as_view(template_name="static/help/help-dev.html")),
    url(r'contact$', TemplateView.as_view(template_name="static/help/contact.html")),
    url(r'performance$', TemplateView.as_view(template_name="static/help/performance.html")),
    url(r'security$', TemplateView.as_view(template_name="static/help/security.html")),
    url(r'quality$', TemplateView.as_view(template_name="static/help/quality.html")),
)
