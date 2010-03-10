from django.forms.models import ModelForm
from django.forms.util import ErrorList
from django.utils.translation import ugettext_lazy as _
from zojax.django.categories.forms import CategoriesField
from zojax.django.categories.models import Category
from zojax.django.harvestrss.models import HarvestedFeed, HarvestedItem
import feedparser
from django import forms


class HarvestedFeedAdminForm(ModelForm):
    
    error_messages = {
        'invalid_feed_url': _(u"This URL does not point to a valid RSS feed."), 
    } 

    def __init__(self, *args, **kwargs):
        super(HarvestedFeedAdminForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.url:
            self.fields['url'].widget.attrs['disabled'] = "disabled"
        self.fields['source_url'].widget.attrs['disabled'] = "disabled"
        
    def clean_url(self):
        data = self.cleaned_data['url']
        try:
            HarvestedFeed.objects.get(url=data)
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
        instance.source_url = parsed.feed.link
        if commit:
            instance.save()
        return instance
        
    class Meta:
        model = HarvestedFeed
        fields = ('url', 'title', 'source_url')        
        

class HarvestedItemAdminForm(ModelForm):
    
    categories = CategoriesField(required=True)

    def __init__(self, *args, **kwargs):
        super(HarvestedItemAdminForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and not self.fields['categories'].initial:
            self.fields['categories'].initial = Category.objects.get_for_object(instance)
        self.fields['url'].widget.attrs['readonly'] = "readonly"

    def save(self, commit=True):
        instance = super(HarvestedItemAdminForm, self).save(commit)
        Category.objects.update_categories(instance, self.cleaned_data['categories'])
        return instance
    
    class Meta:
        model = HarvestedItem
        fields = ('categories', 'title', 'author', 'summary', 'published', 'url')                