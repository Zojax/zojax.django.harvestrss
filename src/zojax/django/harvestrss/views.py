from django.http import HttpResponsePermanentRedirect, Http404
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from zojax.django.harvestrss.models import Article


def view_article(request, id, slug):
    try:
        article = Article.objects.get(pk=int(id))
    except Article.DoesNotExist:
        raise Http404()
    if not article.published:
        raise Http404()
    if article.slug != slug:
        return HttpResponsePermanentRedirect(article.get_absolute_url())
    return render_to_response("harvestrss/article.html", {'article': article},
                              context_instance=RequestContext(request))