from django.core.urlresolvers import resolve
from django.http import Http404

from jingo import register
from jinja2 import contextfunction

URL_NAV_NAMES = {
    'innovate_splash': 'home',
    'innovate_about': 'about',
    'projects_': 'projects',
    'users_': 'users',
}


@register.function
def active_name(request):
    # strip locale
    path = u'/%s' % ('/'.join(request.path.split('/')[2:]),)
    try:
        match = resolve(path)
    except Http404:
        return ''
    for name in URL_NAV_NAMES:
        if match.url_name.startswith(name):
            return URL_NAV_NAMES[name]
    return ''


@register.function
@contextfunction
def moz_url(ctx, url, locale=True):
    """Return a link to mozilla.org with the locale."""
    parts = ['http://www.mozilla.org']
    # Not all Mozilla static pages have a link that is attached to a locale
    locale = ''
    if locale:
        locale = getattr(ctx['request'], 'locale', None)
    url = url.lstrip('/')

    if locale:
        parts.append(locale)
    parts.append(url)
    return '/'.join(parts)
