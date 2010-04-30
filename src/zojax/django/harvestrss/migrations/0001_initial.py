# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'HarvestedFeed'
        db.create_table('harvestrss_harvestedfeed', (
            ('title', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=300, unique=True)),
            ('auto_publish', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('source_url', self.gf('django.db.models.fields.URLField')(max_length=300, null=True, blank=True)),
            ('harvested', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('harvested_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('harvestrss', ['HarvestedFeed'])

        # Adding model 'ArticleIdentifier'
        db.create_table('harvestrss_articleidentifier', (
            ('feed', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['harvestrss.HarvestedFeed'])),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=300, db_index=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('harvestrss', ['ArticleIdentifier'])

        # Adding unique constraint on 'ArticleIdentifier', fields ['feed', 'identifier']
        db.create_unique('harvestrss_articleidentifier', ['feed_id', 'identifier'])

        # Adding model 'Article'
        db.create_table('harvestrss_article', (
            ('feed', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['harvestrss.HarvestedFeed'])),
            ('published_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=300)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('summary', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=300, db_index=True)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique_with=(), max_length=50, populate_from=None, db_index=True)),
            ('article_published_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('harvestrss', ['Article'])

        # Adding M2M table for field sites on 'Article'
        db.create_table('harvestrss_article_sites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('article', models.ForeignKey(orm['harvestrss.article'], null=False)),
            ('site', models.ForeignKey(orm['sites.site'], null=False))
        ))
        db.create_unique('harvestrss_article_sites', ['article_id', 'site_id'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'HarvestedFeed'
        db.delete_table('harvestrss_harvestedfeed')

        # Deleting model 'ArticleIdentifier'
        db.delete_table('harvestrss_articleidentifier')

        # Removing unique constraint on 'ArticleIdentifier', fields ['feed', 'identifier']
        db.delete_unique('harvestrss_articleidentifier', ['feed_id', 'identifier'])

        # Deleting model 'Article'
        db.delete_table('harvestrss_article')

        # Removing M2M table for field sites on 'Article'
        db.delete_table('harvestrss_article_sites')
    
    
    models = {
        'harvestrss.article': {
            'Meta': {'object_name': 'Article'},
            'article_published_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
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
            'harvested': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'harvested_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
