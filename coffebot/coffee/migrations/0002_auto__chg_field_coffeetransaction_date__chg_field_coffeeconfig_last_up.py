# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'CoffeeTransaction.date'
        db.alter_column('coffee_coffeetransaction', 'date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

        # Changing field 'CoffeeConfig.last_updated'
        db.alter_column('coffee_coffeeconfig', 'last_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))

    def backwards(self, orm):

        # Changing field 'CoffeeTransaction.date'
        db.alter_column('coffee_coffeetransaction', 'date', self.gf('django.db.models.fields.DateField')(auto_now_add=True))

        # Changing field 'CoffeeConfig.last_updated'
        db.alter_column('coffee_coffeeconfig', 'last_updated', self.gf('django.db.models.fields.DateField')(auto_now=True))

    models = {
        'coffee.coffeeconfig': {
            'Meta': {'object_name': 'CoffeeConfig'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_processed_tweet': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'coffee.coffeetransaction': {
            'Meta': {'object_name': 'CoffeeTransaction'},
            'amount': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'coffee_user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coffee.CoffeeUser']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
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