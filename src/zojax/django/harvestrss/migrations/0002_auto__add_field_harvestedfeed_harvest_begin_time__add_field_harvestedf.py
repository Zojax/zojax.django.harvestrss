# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding field 'HarvestedFeed.harvest_begin_time'
        db.add_column('harvestrss_harvestedfeed', 'harvest_begin_time', self.gf('django.db.models.fields.TimeField')(default=datetime.time(8, 0)), keep_default=False)

        # Adding field 'HarvestedFeed.harvest_interval'
        db.add_column('harvestrss_harvestedfeed', 'harvest_interval', self.gf('django.db.models.fields.IntegerField')(default=4), keep_default=False)

        # Adding field 'HarvestedFeed.active'
        db.add_column('harvestrss_harvestedfeed', 'active', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True), keep_default=False)
    
    
    def backwards(self, orm):
        
        # Deleting field 'HarvestedFeed.harvest_begin_time'
        db.delete_column('harvestrss_harvestedfeed', 'harvest_begin_time')

        # Deleting field 'HarvestedFeed.harvest_interval'
        db.delete_column('harvestrss_harvestedfeed', 'harvest_interval')

        # Deleting field 'HarvestedFeed.active'
        db.delete_column('harvestrss_harvestedfeed', 'active')
    
    
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
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'auto_publish': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'feed_type': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'harvest_begin_time': ('django.db.models.fields.TimeField', [], {'default': 'datetime.time(8, 0)'}),
            'harvest_interval': ('django.db.models.fields.IntegerField', [], {'default': '4'}),
            'harvested': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'harvested_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source_url': ('django.db.models.fields.URLField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '300', 'unique': 'True'})
        }
    }
    
    complete_apps = ['harvestrss']
