from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _
from django_future import schedule_job
from django_future.models import ScheduledJob
from zojax.django.categories import register
from zojax.django.categories.models import Category
from zojax.django.contentitem.models import ContentItem, CurrentSiteManager, \
    CurrentSiteModelMixin
from zojax.django.location import register as location_register
import BeautifulSoup
import datetime
import feedparser


BLOG_TYPE = u"blog"


FEED_TYPES = (
    (BLOG_TYPE, _(u"Blog")),
)


def harvest_feed(feed):
    try:
        feed.harvest()
    finally:
        feed.schedule_harvest()


class HarvestedFeed(CurrentSiteModelMixin):
    
    url = models.URLField(max_length=300, unique=True)
    
    title = models.CharField(max_length=150, null=True, blank=True)
    
    source_url = models.URLField(max_length=300, null=True, blank=True) 
    
    harvested = models.BooleanField(default=False)
    
    harvested_on = models.DateTimeField(null=True, blank=True)
    
    auto_publish = models.BooleanField(default=False)
    
    objects = CurrentSiteManager()
    
    feed_type = models.CharField(max_length=30, null=True, blank=True, choices=FEED_TYPES)

    active = models.BooleanField(default=True)
    harvest_begin_time = models.TimeField(default=datetime.time(8))
    harvest_interval = models.IntegerField(choices=((4, "4"), (12, "12"), (24, "24"), ), default=4)
    
    job_callable_name = "zojax.django.harvestrss.models.harvest_feed"
    
    def __unicode__(self):
        return self.title or self.url

    class Meta:
        verbose_name = _(u"Harvested RSS feed")
        verbose_name_plural = _(u"Harvested RSS feeds")

    def schedule_harvest(self):
        # Try to find the scheduled jobs for this object
        jobs = ScheduledJob.objects.filter(callable_name=self.job_callable_name,
                                 object_id=self.id,
                                 content_type__pk=ContentType.objects.get_for_model(self.__class__).id,
                                 status="scheduled")
        jobs.delete()
        
        # The harvesting is disabled, do not schedule a job
        if not self.active:
            return

        now = datetime.datetime.now()
        next_harvest_datetime = datetime.datetime.combine(now.date(), self.harvest_begin_time)
        if next_harvest_datetime < now:
            next_harvest_datetime += datetime.timedelta(days=1)
        harvest_interval = datetime.timedelta(hours=self.harvest_interval)
        while (next_harvest_datetime - now) > harvest_interval:
            next_harvest_datetime -= harvest_interval
        schedule_job(next_harvest_datetime, self.job_callable_name, content_object=self)

    def save(self, *args, **kwargs):
        super(HarvestedFeed, self).save(*args, **kwargs)
        self.schedule_harvest()
    
    def harvest(self):
        parsed = feedparser.parse(self.url)
        now = datetime.datetime.now()
        cnt = 0
        for entry in parsed.entries:
            url = getattr(entry, 'link', None)
            if not url:
                continue
            identifier = getattr(entry, 'id', url)
            if ArticleIdentifier.objects.filter(feed=self, identifier=identifier).count() or \
               Article.objects.filter(feed=self, identifier=identifier).count():
                continue
                
            title = entry.title
            summary = getattr(entry, "summary", None)
            if not summary:
                try:
                    summary = entry.content[0].value 
                except:
                    pass
            if summary:
                soup = BeautifulSoup.BeautifulSoup(summary)
                for feedflare in soup.findAll("div", {"class": "feedflare"}): 
                    feedflare.extract()
                for image in soup.findAll("img"):
                    image.extract()
                summary = unicode(soup)
            
            author = getattr(entry, "author", None)
            article_published_on = getattr(entry, "published_parsed", getattr(entry, "created_parsed", getattr(entry, "updated_parsed", None)))
            if article_published_on:
                article_published_on = datetime.datetime(*article_published_on[:6])

            item = Article(feed=self, identifier=identifier, title=title, url=url)
            item.author = author
            item.summary = summary
            item.article_published_on = article_published_on
            if self.auto_publish:
                item.published = True
            item.save()
            Category.objects.update_categories(item, self.categories)
            ArticleIdentifier(feed=self, identifier=identifier).save()
            cnt += 1
        self.harvested_on = now
        self.harvested = True
        self.save()
        return cnt


register(HarvestedFeed)


class ArticleIdentifier(models.Model):
    
    feed = models.ForeignKey(HarvestedFeed)

    identifier = models.CharField(max_length=300, db_index=True) 
    
    def __unicode__(self):
        return self.identifier

    class Meta:
        unique_together = (("feed", "identifier"),)
        verbose_name = _(u"Article identifier")
        verbose_name_plural = _(u"Article identifiers")
    

class Article(ContentItem):

    feed = models.ForeignKey(HarvestedFeed)

    identifier = models.CharField(max_length=300, db_index=True)
    
    url = models.URLField(max_length=300)
    
    author = models.CharField(max_length=150, null=True, blank=True) 
     
    summary = models.TextField(null=True, blank=True)
    
    article_published_on = models.DateTimeField(null=True, blank=True)
    
    featured = models.BooleanField(default=False)
    
    class Meta:
        ordering = ('-created_on',)
        verbose_name = _(u"Article")
        verbose_name_plural = _(u"Articles")

    @permalink
    def get_absolute_url(self):
        return ('view_article', (self.id, self.slug)) 


register(Article)
location_register(Article)
