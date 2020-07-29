from django.shortcuts import (
    get_object_or_404,
    redirect,
    Http404,
    reverse,
    render
    )
from django.conf import settings
from .models import ShortUrl

def ads_view(request, url_obj):
    return render(request, 'shorturls/ads_view.html', context={'instance':url_obj})


def nonads_view(request, url_obj):
    url_obj.click()
    return redirect(url_obj.original_url)


def shortener_view(request, hashed_url):
    url = get_object_or_404(ShortUrl, hashed_url=hashed_url)

    if url.ads:
        return ads_view(request, url)

    if not url.public and not request.user.is_authenticated:
        return redirect(settings.LOGIN_URL + '?next=%s' % url.get_absolute_url())

    return nonads_view(request, url)
    
