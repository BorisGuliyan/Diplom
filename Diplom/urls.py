from django.conf.urls import patterns, include, url

from django.contrib import admin
from suggesting_system import views
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Diplom.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    #url(r'^suggesting_system/', include('suggesting_system.urls')),
    url(r'info/', views.info),
    url(r'form/', views.form),
    url(r'user/(\d{1})', views.user),
    url(r'^$', views.index),
)
