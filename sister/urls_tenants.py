"""
Sister Tenant URL Configuration

"""
from django.conf import settings
from django.urls import path, include

from sister.admin.sites import tenant_admin

urlpatterns = [
    path('', include((tenant_admin.get_urls(), 'admin'))),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    # import debug_toolbar

    # Serve static and media files from development server
    urlpatterns += [
        # path('__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # specific serving mechanism. This should be the last pattern in
    # the list:
]