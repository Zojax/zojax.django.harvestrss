from django.conf import settings
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils import dateformat
from django.utils.translation import ugettext_lazy as _, ungettext_lazy
from zojax.django.categories.models import Category
from zojax.django.harvestrss.forms import HarvestedFeedAdminForm, \
    ArticleAdminForm
from zojax.django.harvestrss.models import HarvestedFeed, Article
from zojax.django.location.models import LocatedItem


def display_categories(obj):
    return ", ".join(sorted([cat.title for cat in obj.categories]))
display_categories.short_description = _(u"Categories")    


def display_harvested_items_number(obj):
    number = Article.objects.filter(feed=obj).count()
    if number:
        return '<a href="%s">%i</a>' % (reverse("admin:harvestrss_article_changelist") + "?feed__id__exact=%i" % obj.id, number)
    else:
        return str(number) 
display_harvested_items_number.short_description = _("Articles")
display_harvested_items_number.allow_tags = True


class HarvestedFeedAdmin(admin.ModelAdmin):

    form = HarvestedFeedAdminForm
    
    list_display = ('title', 'url', display_harvested_items_number, "active", "harvest_begin_time", "harvest_interval", display_categories)
    list_display_links = ('title', )
    list_editable = ("active", "harvest_begin_time", "harvest_interval", )

    search_fields = ('title', 'url')
    list_filter = ('feed_type' ,)

    fieldsets = (
            (None, {
                'classes': ('categories',),
                'fields': ('categories', )
            }),
            (None, {
                'fields': ('url', 'title', 'source_url', 'feed_type', 'auto_publish',  'active', 'harvest_begin_time', 'harvest_interval', )
            }),
        )
    
    def save_model(self, request, obj, form, change):
        super(HarvestedFeedAdmin, self).save_model(request, obj, form, change)
        if "categories" in form.cleaned_data:
            Category.objects.update_categories(obj, form.cleaned_data['categories'])
    
    def harvest(self, request, queryset):
        feeds_count = queryset.count()
        if not feeds_count:
            return
        count = 0
        for feed in queryset:
            count += feed.harvest()
        message = ungettext_lazy(u"%(count)d item was harvested", u"%(count)d items were harvested", count) % {'count': count}
        message += ungettext_lazy(u" from %(count)d feed.", u" from %(count)d feeds.", feeds_count) % {'count': feeds_count}
        self.message_user(request, message)
    harvest.short_description = _(u"Harvest selected feeds")

    actions = ['harvest']
    
    
admin.site.register(HarvestedFeed, HarvestedFeedAdmin)


def display_created_on(obj):
    return dateformat.format(obj.created_on, settings.DATETIME_FORMAT)
display_created_on.short_description = _(u"Created on")    


class ArticleAdmin(admin.ModelAdmin):

    form = ArticleAdminForm
    
    list_display = ('title', 'feed', display_created_on, 'published', 'featured',)
    list_editable = ('published', 'featured', )
    list_filter = ('published', 'feed', 'created_on', 'featured', )
    
    search_fields = ('title', 'feed__title')
    
    def save_model(self, request, obj, form, change):
        super(ArticleAdmin, self).save_model(request, obj, form, change)
        if 'categories' in form.cleaned_data:
            Category.objects.update_categories(obj, form.cleaned_data['categories'])
        if 'location' in form.cleaned_data:
            LocatedItem.objects.update(obj, form.cleaned_data['location'])
    
    fieldsets = (
            (None, {
                'classes': ('categories',),
                'fields': ('categories', )
            }),
            (None, {
                'classes': ('location',),
                'fields': ('location', )
            }),
            (None, {
                'fields': ('title', 'author', 'summary', 'published', 'url', 'featured', )
            }),
        )

    def publish(self, request, queryset):
        count = 0
        for item in queryset:
            item.published = True
            item.save()
            count += 1
        self.message_user(request,
                          ungettext_lazy(u"%(count)d item was published",
                                         u"%(count)d items were published", count) 
                          % {'count': count})
    publish.short_description = _(u"Publish selected items")

    actions = ['publish']
    
    def has_add_permission(self, request):
        return False

    
admin.site.register(Article, ArticleAdmin)