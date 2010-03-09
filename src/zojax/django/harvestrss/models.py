from django.db import models
from django.utils.translation import ugettext_lazy as _
from zojax.django.categories import register
import BeautifulSoup
import datetime
import feedparser


class HarvestedFeed(models.Model):
    
    url = models.URLField(max_length=300, unique=True)
    
    title = models.CharField(max_length=150, null=True, blank=True)
    
    source_url = models.URLField(max_length=300, null=True, blank=True) 
    
    harvested = models.BooleanField(default=False)
    
    harvested_on = models.DateTimeField(null=True, blank=True)
    
    def __unicode__(self):
        return self.title or self.url

    class Meta:
        verbose_name = _(u"Harvested RSS feed")
        verbose_name_plural = _(u"Harvested RSS feeds")
    
    def harvest(self):
        parsed = feedparser.parse(self.url)
        now = datetime.datetime.now()
        cnt = 0
        for entry in parsed.entries:
            identifier = entry.id
            if HarvestedItemIdentifier.objects.filter(feed=self, identifier=identifier).count() or \
               HarvestedItem.objects.filter(feed=self, identifier=identifier).count():
                continue
                
            url = entry.link
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
            published_on = getattr(entry, "published_parsed", getattr(entry, "created_parsed", getattr(entry, "updated_parsed", None)))
            if published_on:
                published_on = datetime.datetime(*published_on[:6])

            item = HarvestedItem(feed=self, identifier=identifier, harvested_on=now, url=url)
            item.title = title
            item.author = author
            item.summary = summary
            item.published_on = published_on
            item.save()
            HarvestedItemIdentifier(feed=self, identifier=identifier).save()
            cnt += 1
        self.harvested_on = now
        self.harvested = True
        self.save()
        return cnt


class HarvestedItemIdentifier(models.Model):
    
    feed = models.ForeignKey(HarvestedFeed)

    identifier = models.CharField(max_length=300, db_index=True) 
    
    def __unicode__(self):
        return self.identifier

    class Meta:
        unique_together = (("feed", "identifier"),)
        verbose_name = _(u"Harvested RSS item identifier")
        verbose_name_plural = _(u"Harvested RSS item identifiers")
    
    
class HarvestedItem(models.Model):

    feed = models.ForeignKey(HarvestedFeed)

    identifier = models.CharField(max_length=300, db_index=True)
    
    harvested_on = models.DateTimeField()  

    url = models.URLField(max_length=300)
    
    title = models.CharField(max_length=150, null=True, blank=True)
     
    author = models.CharField(max_length=150, null=True, blank=True) 
     
    summary = models.TextField(null=True, blank=True)
    
    published_on = models.DateTimeField(null=True, blank=True)
    
    published = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.title or self.url

    class Meta:
        ordering = ('-harvested_on',)
        verbose_name = _(u"Harvested RSS item")
        verbose_name_plural = _(u"Harvested RSS items")


register(HarvestedItem)

