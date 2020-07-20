"""
Simpellab URL Configuration

"""
from django.conf import settings
from django.urls import path, include
from django.contrib import admin

from simpellab.admin.sites import admin_site

urlpatterns = [
    path('go/', include('simpellab.modules.shorturls.urls')),
    # path('api/', include('simpellab.api.urls')),
    path('admin/', admin.site.urls),
    path('_nested_admin/', include('nested_admin.urls'))
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    # import debug_toolbar

    # Serve static and media files from development server
    urlpatterns += [
        # path('__debug__/', include(debug_toolbar.urls)),
        # path('admin/docs/', include(admindocs_urls)),
        path('admin/queues/', include('django_rq.urls'))
    ]
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # specific serving mechanism. This should be the last pattern in
    # the list:
]