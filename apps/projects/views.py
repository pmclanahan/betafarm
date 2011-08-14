from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

import jingo

from tower import ugettext as _

from activity.models import Activity
from projects.models import Project


def all(request):
    """Display a list of all projects."""
    projects = Project.objects.exclude(tags__name='program').order_by('name')
    return jingo.render(request, 'projects/all.html', {
        'projects': projects,
        'view': 'all'
    })


def programs(request):
    """Display a list of all programs."""
    programs = Project.objects.filter(tags__name='program').order_by('-name')
    return jingo.render(request, 'projects/programs.html', {
        'programs': programs,
    })


def show(request, slug):
    """Display information about a single project, specified by ``slug``."""
    project = get_object_or_404(Project, slug=slug)
    topic = request.session.get('topic', None) or project.topics.all()[0].name
    return jingo.render(request, 'projects/show.html', {
        'project': project,
        'topic': topic
    })


@login_required
@require_POST
def follow(request, slug):
    """
    Add the currently logged in user as a follower of the project specified
    by ``slug``.
    """
    project = get_object_or_404(Project, slug=slug)
    project.followers.add(request.user.get_profile())
    project.save()
    msg = _('Updates from <em>%s</em> will now appear in your dashboard.' % (
        project.name,))
    messages.success(request, msg)
    return HttpResponseRedirect(reverse('projects_show', kwargs={
        'slug': project.slug
    }))


@login_required
@require_POST
def unfollow(request, slug):
    """
    Remove the currently logged in user from the list of followers for
    the project specified by ``slug``.
    """
    project = get_object_or_404(Project, slug=slug)
    project.followers.remove(request.user.get_profile())
    project.save()
    msg = _('''Updates from <em>%s</em> will no longer appear in your
               dashboard''' % (project.name,))
    messages.success(request, msg)
    return HttpResponseRedirect(reverse('projects_show', kwargs={
        'slug': project.slug
    }))


def activity(request, slug):
    project = get_object_or_404(Project, slug=slug)
    activities = Activity.objects.filter(
        entry__project=project).select_related(
        'entry', 'entry__project').order_by('-published_on')
    paginator = Paginator(activities, 10)
    return jingo.render(request, 'projects/activity.html', {
        'project': project,
        'activities': paginator.page(1)
    })


def active(request):
    """Display a list of the most active projects."""
    # TODO - We don't have anything with which to measure activity yet.
    projects = Project.objects.exclude(tags__name='program').order_by('-name')
    return jingo.render(request, 'projects/all.html', {
        'projects': projects,
        'view': 'active'
    })


def recent(request):
    """Display a list of the most recent projects."""
    projects = Project.objects.exclude(tags__name='program').order_by('-id')
    return jingo.render(request, 'projects/all.html', {
        'projects': projects,
        'view': 'recent'
    })
