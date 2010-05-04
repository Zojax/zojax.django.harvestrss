# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding field 'Article.featured'
        db.add_column('harvestrss_article', 'featured', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True), keep_default=False)

        # Adding field 'HarvestedFeed.feed_type'
        db.add_column('harvestrss_harvestedfeed', 'feed_type', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True), keep_default=False)
    
    
    def backwards(self, orm):
        
        # Deleting field 'Article.featured'
        db.delete_column('harvestrss_article', 'featured')

        # Deleting field 'HarvestedFeed.feed_type'
        db.delete_column('harvestrss_harvestedfeed', 'feed_type')
    
    
    models = {
        'harvestrss.article': {
            'Meta': {'object_name': 'Article'},
            'article_published_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['harvestrss.HarvestedFeed']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '300', 'db_index': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'published_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'harvestrss_article_related'", 'blank': 'True', 'to': "orm['sites.Site']"}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': 'None', 'db_index': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '300'})
        },
        'harvestrss.articleidentifier': {
            'Meta': {'unique_together': "(('feed', 'identifier'),)", 'object_name': 'ArticleIdentifier'},
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['harvestrss.HarvestedFeed']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '300', 'db_index': 'True'})
        },
        'harvestrss.harvestedfeed': {
            'Meta': {'object_name': 'HarvestedFeed'},
            'auto_publish': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'feed_type': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'harvested': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'harvested_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'harvestrss_harvestedfeed_related'", 'blank': 'True', 'to': "orm['sites.Site']"}),
            'source_url': ('django.db.models.fields.URLField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '300', 'unique': 'True'})
        },
        'sites.site': {
            'Meta': {'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }
    
    complete_apps = ['harvestrss']
