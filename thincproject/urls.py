from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import (
    TemplateView,
    RedirectView,
    )
from thinc import views
from django.contrib.auth.views import (
    password_reset,
    password_reset_done,
    password_reset_confirm,
    password_reset_complete
    )
from thinc.backends import MyRegistrationView
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^accounts/register/$', views.register, name='registration_register'),
    url(r'^accounts/create_idea/$', views.create_idea, name='registration_create_idea'),
    url(r'^$', views.index, name='home'),
    url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^ideas/$', RedirectView.as_view(pattern_name='home', permanent=True)),
    url(r'^ideas/(?P<slug>[-\w]+)/$', views.idea_detail, name='idea_detail'),
    url(r'^ideas/(?P<slug>[-\w]+)/edit/$', views.edit_idea, name='edit_idea'),
    url(r'^my_ideas/$', views.my_ideas, name='my_ideas'),
    url(r'^create_idea/$', views.create_idea, name='create_idea'),

    # user page
    url(r'^users/(?P<username>\w+)/$', views.user_info, name='user_info'),

    # browse
    url(r'^browse/$', RedirectView.as_view(pattern_name='browse_by_votes', permanent=True)),
    url(r'^browse/name/$',
        views.browse_by_name, name='browse_by_name'),
    url(r'^browse/name/(?P<initial>[-\w]+)/$',
        views.browse_by_name, name='browse_by_name'),
    url(r'^browse/votes/$', views.browse_by_votes, name='browse_by_votes'),

    # password reset
    url(r'^accounts/password/reset/$', 
        password_reset,
        {'template_name':
        'registration/password_reset_form.html'},
        name="password_reset"),
    url(r'^accounts/password/reset/done/$',
        password_reset_done,
        {'template_name':
        'registration/password_reset_done.html'},
        name="password_reset_done"),
    url(r'^accounts/password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 
        password_reset_confirm,
        {'template_name':
        'registration/password_reset_confirm.html'},
        name="password_reset_confirm"),
    url(r'^accounts/password/done/$', 
        password_reset_complete,
        {'template_name':
        'registration/password_reset_complete.html'},
        name="password_reset_complete"),

    # login/logout
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),

    url(r'^accounts/', 
        include('registration.backends.simple.urls')),
    url(r'^admin/', admin.site.urls),
]
