from django import forms
from django.forms.models import ModelForm
from django.forms.util import ErrorList
from django.utils.translation import ugettext_lazy as _
from zojax.django.categories.forms import CategoriesAdminField
from zojax.django.categories.models import Category
from zojax.django.harvestrss.models import HarvestedFeed, Article
from zojax.django.location.forms import LocationChoiceField
from zojax.django.location.models import LocatedItem
import feedparser


class HarvestedFeedAdminForm(ModelForm):

    categories = CategoriesAdminField(required=False)
    
    error_messages = {
        'invalid_feed_url': _(u"This URL does not point to a valid RSS feed."), 
    } 

    def __init__(self, *args, **kwargs):
        super(HarvestedFeedAdminForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and not self.fields['categories'].initial:
            self.fields['categories'].initial = Category.objects.get_for_object(instance)
        self.fields['source_url'].widget.attrs['disabled'] = "disabled"
        
    def clean_url(self):
        data = self.cleaned_data['url']
        try:
            instance = getattr(self, 'instance', None)
            if HarvestedFeed.objects.get(url=data) != instance:
                raise forms.ValidationError(_("The feed with this URL is registered already."))
        except HarvestedFeed.DoesNotExist:
            pass

        return data
                    
    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')
        if url:
            try:
                parsed = feedparser.parse(url)
            except:
                self._errors["url"] = ErrorList([self.error_messages['invalid_feed_url']])
                del cleaned_data["url"]
                return cleaned_data
            if not parsed.version:
                self._errors["url"] = ErrorList([self.error_messages['invalid_feed_url']])
                del cleaned_data["url"]
                return cleaned_data

        return cleaned_data
    
    def save(self, commit=True):
        old_url = self.instance.url
        instance = super(HarvestedFeedAdminForm, self).save(commit)
        parsed = feedparser.parse(instance.url)
        if not instance.title or instance.url != old_url:
            instance.title = parsed.feed.title
        instance.source_url = getattr(parsed.feed, 'link', instance.url)
        if commit:
            instance.save()
        return instance
        
    class Meta:
        model = HarvestedFeed
        fields = ('categories', 'url', 'title', 'source_url', 'feed_type', 'auto_publish', 'active', 'harvest_begin_time', 'harvest_interval', )        
        

class ArticleAdminForm(ModelForm):
    
    categories = CategoriesAdminField(required=True)
    location = LocationChoiceField(required=False)

    def __init__(self, *args, **kwargs):
        super(ArticleAdminForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and not self.fields['categories'].initial:
            self.fields['categories'].initial = Category.objects.get_for_object(instance)
        if instance and not self.fields['location'].initial:
            self.fields['location'].initial = LocatedItem.objects.get_for_object(instance)
        self.fields['url'].widget.attrs['readonly'] = "readonly"
    
    class Meta:
        model = Article
        fields = ('categories', 'title', 'author', 'summary', 'location', 'published', 'url', 'featured', )                