from django.conf import settings
from django.contrib import admin
from django.utils import dateformat
from django.utils.translation import ugettext_lazy as _, ungettext_lazy
from zojax.django.harvestrss.forms import HarvestedFeedAdminForm,\
    HarvestedItemAdminForm
from zojax.django.harvestrss.models import HarvestedFeed, HarvestedItem


def display_harvested_on(obj):
    if not obj.harvested_on:
        return _(u"Not harvested yet")
    return dateformat.format(obj.harvested_on, settings.DATETIME_FORMAT)
display_harvested_on.short_description = _(u"Harvested on")    


class HarvestedFeedAdmin(admin.ModelAdmin):


    form = HarvestedFeedAdminForm
    
    list_display = ('title', 'url', 'harvested', display_harvested_on)
    list_display_links = ('title', )

    search_fields = ('title', 'url')
    list_filter = ('harvested',)
    
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


class HarvestedItemAdmin(admin.ModelAdmin):

    form = HarvestedItemAdminForm
    
    list_display = ('title', 'feed', display_harvested_on, 'published')
    list_editable = ('published',)
    list_filter = ('published', 'feed', 'harvested_on')
    
    search_fields = ('title', 'feed__title')
    
    fieldsets = (
            (None, {
                'classes': ('categories',),
                'fields': ('categories', )
            }),
            (None, {
                'fields': ('title', 'author', 'summary', 'published', 'url')
            }),
        )

    def publish(self, request, queryset):
        count = queryset.count()
        queryset.update(published=True)
        self.message_user(request,
                          ungettext_lazy(u"%(count)d item was published",
                                         u"%(count)d items were published", count) 
                          % {'count': count})
    publish.short_description = _(u"Publish selected items")

    actions = ['publish']
    
    def has_add_permission(self, request):
        return False

    
admin.site.register(HarvestedItem, HarvestedItemAdmin)        