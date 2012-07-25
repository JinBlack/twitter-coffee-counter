# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CoffeeUser'
        db.create_table('coffee_coffeeuser', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('twitter_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('total_coffees', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('balance', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('coffee', ['CoffeeUser'])

        # Adding model 'CoffeeTransaction'
        db.create_table('coffee_coffeetransaction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('coffee_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['coffee.CoffeeUser'], null=True, on_delete=models.SET_NULL)),
            ('date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('operation', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('amount', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
        ))
        db.send_create_signal('coffee', ['CoffeeTransaction'])

        # Adding model 'CoffeeConfig'
        db.create_table('coffee_coffeeconfig', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_processed_tweet', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
            ('last_updated', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2012, 7, 24, 0, 0), auto_now=True, blank=True)),
        ))
        db.send_create_signal('coffee', ['CoffeeConfig'])


    def backwards(self, orm):
        # Deleting model 'CoffeeUser'
        db.delete_table('coffee_coffeeuser')

        # Deleting model 'CoffeeTransaction'
        db.delete_table('coffee_coffeetransaction')

        # Deleting model 'CoffeeConfig'
        db.delete_table('coffee_coffeeconfig')


    models = {
        'coffee.coffeeconfig': {
            'Meta': {'object_name': 'CoffeeConfig'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_processed_tweet': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'last_updated': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 7, 24, 0, 0)', 'auto_now': 'True', 'blank': 'True'})
        },
        'coffee.coffeetransaction': {
            'Meta': {'object_name': 'CoffeeTransaction'},
            'amount': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'coffee_user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coffee.CoffeeUser']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            'date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'operation': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        },
        'coffee.coffeeuser': {
            'Meta': {'object_name': 'CoffeeUser'},
            'balance': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'total_coffees': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'twitter_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'user_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        }
    }

    complete_apps = ['coffee']